import React, { useState, useEffect } from 'react';

// WhisperWand Logo Component
const WhisperWandLogo = () => (
  <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M24 4L28 44"
      stroke="#8b5cf6"
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M18 8C18 8 24 12 30 8"
      stroke="#8b5cf6"
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M32 16C32 16 24 20 16 16"
      stroke="#8b5cf6"
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M34 24C34 24 24 28 14 24"
      stroke="#8b5cf6"
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M36 32C36 32 24 36 12 32"
      stroke="#8b5cf6"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

const INDUSTRY_PRESETS = {
  custom: [],
  medical: [
    "Extract patient symptoms and conditions",
    "Identify prescribed medications and dosages",
    "Note any allergies or contraindications",
    "Highlight follow-up instructions"
  ],
  legal: [
    "Identify key dates and deadlines",
    "Extract case citations and references",
    "Note any legal obligations or requirements",
    "Highlight action items and next steps"
  ],
  business: [
    "Extract action items and deadlines",
    "Identify key stakeholders",
    "Note financial figures and metrics",
    "Highlight decisions and agreements made"
  ],
  academic: [
    "Extract key research findings",
    "Identify methodology details",
    "Note citations and references",
    "Highlight conclusions and future work"
  ]
};

function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [topics, setTopics] = useState([]);
  const [inputTopic, setInputTopic] = useState('');
  const [transcription, setTranscription] = useState('');
  const [summary, setSummary] = useState('');
  const [topicSummaries, setTopicSummaries] = useState({});
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);
  const [useOptimizer, setUseOptimizer] = useState(false);
  const [selectedPreset, setSelectedPreset] = useState('custom');
  const [customTopics, setCustomTopics] = useState([]);

  useEffect(() => {
    document.body.className = isDarkMode ? 'dark-theme' : 'light-theme';
  }, [isDarkMode]);

  useEffect(() => {
    if (selectedPreset === 'custom') {
      setTopics(customTopics);
    } else {
      setTopics(INDUSTRY_PRESETS[selectedPreset] || []);
    }
  }, [selectedPreset, customTopics]);

  const handleAddTopic = () => {
    if (inputTopic.trim()) {
      const newTopics = [...(topics || []), inputTopic.trim()];
      setTopics(newTopics);
      if (selectedPreset === 'custom') {
        setCustomTopics(newTopics);
      } else {
        setSelectedPreset('custom');
        setCustomTopics(newTopics);
      }
      setInputTopic('');
    }
  };

  const handleDeleteTopic = (indexToDelete) => {
    const newTopics = topics.filter((_, index) => index !== indexToDelete);
    setTopics(newTopics);
    if (selectedPreset === 'custom') {
      setCustomTopics(newTopics);
    }
    if (selectedTopic === topics[indexToDelete]) {
      setSelectedTopic(null);
    }
  };

  const handleToggleMic = () => {
    setIsMicActive(!isMicActive);
  };

  const handleDownload = (content, filename) => {
    const element = document.createElement('a');
    const file = new Blob([content], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handlePresetChange = (e) => {
    const newPreset = e.target.value;
    if (selectedPreset === 'custom') {
      setCustomTopics(topics || []); // Save custom topics
    }
    setSelectedPreset(newPreset);
  };

  return (
    <div className={`app ${isDarkMode ? 'dark-theme' : 'light-theme'}`}>
      <div className="brand-header">
        <div className="brand-container">
          <div className="logo-container">
            <div className="logo">
              <WhisperWandLogo />
            </div>
            <div className="brand-text">
              <p className="company-name">MAGIC UNICORN</p>
              <h1 className="product-name">WhisperWand</h1>
            </div>
          </div>
          <p className="tagline">Transforming sound into wisdom</p>
        </div>
        <button 
          className="theme-toggle" 
          onClick={() => setIsDarkMode(!isDarkMode)}
        >
          {isDarkMode ? '☀️' : '🌙'}
        </button>
      </div>
      
      <div className="controls">
        <button className="file-button">
          Select Audio File
        </button>
        <button 
          className={`mic-button ${isMicActive ? 'active' : ''}`} 
          onClick={handleToggleMic}
        >
          🎤 {isMicActive ? 'Stop Mic' : 'Live Listen'}
        </button>
        <div className="optimizer-toggle">
          <label>
            <input 
              type="checkbox" 
              checked={useOptimizer}
              onChange={(e) => setUseOptimizer(e.target.checked)}
            />
            Use Prompt Optimizer
          </label>
        </div>
      </div>

      <div className="main-content">
        <div className="left-column">
          <div className="window transcription-window">
            <div className="window-header">
              <h2>Transcription</h2>
              <button onClick={() => handleDownload(transcription, 'transcription.txt')}>
                💾 Download
              </button>
            </div>
            <textarea readOnly value={transcription} />
          </div>

          <div className="window summary-window">
            <div className="window-header">
              <h2>{selectedPreset === 'summarize' ? 'Summary' : 'Analysis'}</h2>
              <button onClick={() => handleDownload(summary, 'analysis.txt')}>
                💾 Download
              </button>
            </div>
            <textarea readOnly value={summary} />
          </div>
        </div>

        <div className="right-column">
          <div className="window topics-window">
            <h2>Analysis Instructions</h2>
            <div className="preset-topics">
              <select 
                className="preset-select"
                value={selectedPreset}
                onChange={handlePresetChange}
              >
                <option value="custom">Custom Instructions</option>
                <option value="medical">Medical Preset</option>
                <option value="legal">Legal Preset</option>
                <option value="business">Business Preset</option>
                <option value="academic">Academic Preset</option>
              </select>
            </div>
            <textarea
              value={inputTopic}
              onChange={(e) => setInputTopic(e.target.value)}
              placeholder="Enter what information you want to extract..."
              rows={3}
            />
            <button onClick={handleAddTopic}>Add Analysis Instruction</button>
            <div className="topics-list">
              {(topics || []).map((topic, index) => (
                <div key={index} className="topic-item">
                  <p>{topic}</p>
                  <button 
                    className="delete-button"
                    onClick={() => handleDeleteTopic(index)}
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
