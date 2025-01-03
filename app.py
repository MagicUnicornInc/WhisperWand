import customtkinter as ctk
from tkinter import filedialog, ttk
import threading
import time
import json
import os

INDUSTRY_PRESETS = {
    "custom": [],
    "medical": [
        "Extract patient symptoms and conditions",
        "Identify prescribed medications and dosages",
        "Note any allergies or contraindications",
        "Highlight follow-up instructions"
    ],
    "legal": [
        "Identify key dates and deadlines",
        "Extract case citations and references",
        "Note any legal obligations or requirements",
        "Highlight action items and next steps"
    ],
    "business": [
        "Extract action items and deadlines",
        "Identify key stakeholders",
        "Note financial figures and metrics",
        "Highlight decisions and agreements made"
    ],
    "academic": [
        "Extract key research findings",
        "Identify methodology details",
        "Note citations and references",
        "Highlight conclusions and future work"
    ]
}

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhisperWand")
        self.root.geometry("1000x800")

        # Default to dark theme
        self.is_dark_theme = True
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.is_recording = False
        self.is_mic_active = False
        self.topics = []
        self.custom_topics = []
        self.transcription_text = ""
        self.summary_text = ""
        self.selected_topic = None
        self.use_prompt_optimizer = ctk.BooleanVar(value=False)
        self.selected_preset = ctk.StringVar(value="summarize")

        self.create_main_layout()

    def create_main_layout(self):
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.create_header()

        # Top Control Panel
        self.create_control_panel()

        # Content Area
        self.content_area = ctk.CTkFrame(self.main_container)
        self.content_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Create two columns
        self.left_column = ctk.CTkFrame(self.content_area)
        self.left_column.pack(side="left", fill="both", expand=True, padx=5)

        self.right_column = ctk.CTkFrame(self.content_area)
        self.right_column.pack(side="right", fill="both", expand=True, padx=5)

        self.create_transcription_section()
        self.create_topic_section()
        self.create_summary_section()

    def create_header(self):
        header = ctk.CTkFrame(self.main_container)
        header.pack(fill="x", padx=5, pady=5)

        # Branding
        brand_label = ctk.CTkLabel(
            header,
            text="Magic Unicorn presents...",
            font=ctk.CTkFont(size=14)
        )
        brand_label.pack(side="left", padx=10)

        title = ctk.CTkLabel(
            header,
            text="WhisperWand",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left", padx=10)

        # Tagline
        tagline = ctk.CTkLabel(
            header,
            text="Transforming sound into wisdom.",
            font=ctk.CTkFont(size=14, slant="italic")
        )
        tagline.pack(side="left", padx=10)

        self.theme_button = ctk.CTkButton(
            header,
            text="🌙" if self.is_dark_theme else "☀️",
            width=40,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="right", padx=10)

    def create_control_panel(self):
        control_panel = ctk.CTkFrame(self.main_container)
        control_panel.pack(fill="x", padx=5, pady=5)

        # Recording controls
        self.file_button = ctk.CTkButton(
            control_panel,
            text="Select Audio File",
            command=self.select_audio_file
        )
        self.file_button.pack(side="left", padx=5)

        self.mic_button = ctk.CTkButton(
            control_panel,
            text="🎤 Live Listen",
            command=self.toggle_mic
        )
        self.mic_button.pack(side="left", padx=5)

        # Prompt Optimizer Toggle
        self.optimizer_toggle = ctk.CTkCheckBox(
            control_panel,
            text="Use Prompt Optimizer",
            variable=self.use_prompt_optimizer,
            command=self.toggle_optimizer
        )
        self.optimizer_toggle.pack(side="right", padx=5)

    def create_transcription_section(self):
        frame = ctk.CTkFrame(self.left_column)
        frame.pack(fill="both", expand=True, pady=5)

        header = ctk.CTkFrame(frame)
        header.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(header, text="Transcription").pack(side="left")
        
        download_btn = ctk.CTkButton(
            header,
            text="💾 Download",
            command=lambda: self.download_content("transcription"),
            width=100
        )
        download_btn.pack(side="right", padx=5)

        self.transcription_text = ctk.CTkTextbox(frame, wrap="word")
        self.transcription_text.pack(fill="both", expand=True, padx=5, pady=5)

    def create_topic_section(self):
        frame = ctk.CTkFrame(self.right_column)
        frame.pack(fill="both", pady=5)

        # Preset Selection
        preset_frame = ctk.CTkFrame(frame)
        preset_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(preset_frame, text="Select Preset:").pack(side="left", padx=5)
        
        preset_menu = ctk.CTkOptionMenu(
            preset_frame,
            values=["Summarize", "Custom Instructions", "Medical Preset", "Legal Preset", 
                   "Business Preset", "Academic Preset"],
            variable=self.selected_preset,
            command=self.handle_preset_change
        )
        preset_menu.pack(fill="x", padx=5, pady=5)

        # Topic Input Area
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=5, pady=5)

        self.topic_entry = ctk.CTkTextbox(input_frame, height=60, wrap="word")
        self.topic_entry.pack(fill="x", padx=5, pady=5)
        self.topic_entry.insert("1.0", "Enter what information you want to extract...")

        add_btn = ctk.CTkButton(
            input_frame,
            text="Add Analysis Instruction",
            command=self.add_topic,
            fg_color=self.get_button_color()
        )
        add_btn.pack(pady=5)

        # Topics List
        self.topics_frame = ctk.CTkScrollableFrame(frame, label_text="Analysis Instructions")
        self.topics_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def create_summary_section(self):
        frame = ctk.CTkFrame(self.left_column)
        frame.pack(fill="both", expand=True, pady=5)

        header = ctk.CTkFrame(frame)
        header.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(header, text="Analysis").pack(side="left")
        
        download_btn = ctk.CTkButton(
            header,
            text="💾 Download",
            command=lambda: self.download_content("summary"),
            width=100
        )
        download_btn.pack(side="right", padx=5)

        self.summary_text = ctk.CTkTextbox(frame, wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=5, pady=5)

    def handle_preset_change(self, choice):
        preset_key = choice.lower().replace(" preset", "").replace(" instructions", "")
        if preset_key == "custom":
            self.topics = self.custom_topics.copy()
        elif preset_key == "summarize":
            self.topics = []
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", "Summarizing...")
        else:
            self.topics = INDUSTRY_PRESETS[preset_key].copy()
        self.update_topics_display()

    def add_topic(self):
        topic = self.topic_entry.get("1.0", "end-1c").strip()
        if topic and topic != "Enter what information you want to extract...":
            if self.selected_preset.get().lower() == "custom":
                self.custom_topics.append(topic)
            else:
                self.selected_preset.set("Custom Instructions")
                self.custom_topics = [topic]
            self.topics = self.custom_topics.copy()
            self.update_topics_display()
            self.topic_entry.delete("1.0", "end")
            self.topic_entry.insert("1.0", "Enter what information you want to extract...")

    def update_topics_display(self):
        # Clear existing topics
        for widget in self.topics_frame.winfo_children():
            widget.destroy()

        # Add new topics
        for topic in self.topics:
            topic_frame = ctk.CTkFrame(self.topics_frame)
            topic_frame.pack(fill="x", padx=5, pady=2)

            topic_label = ctk.CTkLabel(
                topic_frame,
                text=topic,
                wraplength=300
            )
            topic_label.pack(side="left", padx=5, fill="x", expand=True)

            delete_btn = ctk.CTkButton(
                topic_frame,
                text="🗑️",
                width=40,
                command=lambda t=topic: self.delete_topic(t)
            )
            delete_btn.pack(side="right", padx=5)

    def delete_topic(self, topic_to_delete):
        if topic_to_delete in self.custom_topics:
            self.custom_topics.remove(topic_to_delete)
        if topic_to_delete in self.topics:
            self.topics.remove(topic_to_delete)
        self.update_topics_display()

    def get_button_color(self):
        start = "#7e57c2" if not self.is_dark_theme else None
        end = "#673ab7" if not self.is_dark_theme else None
        return (start, end)

    def update_button_colors(self):
        button_color = self.get_button_color()
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=button_color)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        new_mode = "dark" if self.is_dark_theme else "light"
        ctk.set_appearance_mode(new_mode)
        self.theme_button.configure(
            text="🌙" if self.is_dark_theme else "☀️",
            fg_color=self.get_button_color()
        )
        self.update_button_colors()

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.m4a *.ogg"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.process_audio_file(file_path)

    def process_audio_file(self, file_path):
        # Placeholder for audio processing
        self.transcription_text.insert("end", f"Processing audio file: {file_path}\n")

    def toggle_mic(self):
        self.is_mic_active = not self.is_mic_active
        if self.is_mic_active:
            self.mic_button.configure(text="🎤 Stop Mic", fg_color="#d9534f")
            self.start_mic_recording()
        else:
            self.mic_button.configure(text="🎤 Live Listen", fg_color=self.get_button_color())
            self.stop_mic_recording()

    def start_mic_recording(self):
        # Placeholder for mic recording
        self.transcription_text.insert("end", "Starting live transcription...\n")

    def stop_mic_recording(self):
        # Placeholder for stopping mic recording
        self.transcription_text.insert("end", "Stopping live transcription.\n")

    def toggle_optimizer(self):
        # Placeholder for prompt optimizer logic
        is_enabled = self.use_prompt_optimizer.get()
        print(f"Prompt optimizer {'enabled' if is_enabled else 'disabled'}")

    def download_content(self, content_type):
        content = ""
        default_filename = ""

        if content_type == "transcription":
            content = self.transcription_text.get("1.0", "end-1c")
            default_filename = "transcription.txt"
        elif content_type == "summary":
            content = self.summary_text.get("1.0", "end-1c")
            default_filename = "analysis.txt"

        if content:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=default_filename,
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

if __name__ == "__main__":
    root = ctk.CTk()
    app = TranscriptionApp(root)
    root.mainloop()
