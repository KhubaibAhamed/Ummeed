import { useState } from 'react';
import { ChatBubble } from './ChatBubble';
import { CitationSheet } from './CitationSheet';
import { Header } from './Header';
import { useChat } from '../hooks/useChat';
import { useVoiceRecorder } from '../hooks/useVoiceRecorder';
import { transcribeAudio } from '../api/client';
import { getTranslations } from '../i18n';

export function ChatScreen({ language, location }) {
  const t = getTranslations(language);
  const { messages, isLoading, sendMessage } = useChat({ language, location });
  const { isRecording, errorType: recordingErrorType, toggleRecording } = useVoiceRecorder();
  const [inputValue, setInputValue] = useState('');
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [voiceError, setVoiceError] = useState(null);

  function handleSend() {
    const trimmed = inputValue.trim();
    if (!trimmed) return;
    sendMessage(trimmed);
    setInputValue('');
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleSend();
  }

  async function handleMicClick() {
    setVoiceError(null);
    const audioBlob = await toggleRecording();
    if (!audioBlob) return; // either just started recording, or nothing captured

    setIsTranscribing(true);
    try {
      const { text } = await transcribeAudio(audioBlob);
      sendMessage(text);
    } catch {
      setVoiceError(t.chat.transcribeError);
    } finally {
      setIsTranscribing(false);
    }
  }

  const recordingErrorMessage =
    recordingErrorType === 'denied'
      ? t.chat.micDenied
      : recordingErrorType === 'unsupported'
      ? t.chat.micUnsupported
      : null;

  return (
    <div className="chat-screen">
      <Header t={t} showNav={false} />

      <div className="chat-layout">
        <div className="chat-main">
          <div className="chat-body">
            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                message={message}
                onCitationSelect={setSelectedCitation}
              />
            ))}

            {isLoading && (
              <div className="thinking-row">
                <svg className="dawn-motif" viewBox="0 0 60 34" width="34" height="20">
                  <path
                    d="M 6 26 A 24 24 0 0 1 54 26"
                    fill="none"
                    stroke="#E8A33D"
                    strokeWidth="3.5"
                    strokeLinecap="round"
                  />
                  <circle cx="30" cy="26" r="4" fill="#E8A33D" />
                </svg>
                <span className="thinking-text">{t.chat.thinking}</span>
              </div>
            )}

            {isTranscribing && (
              <div className="thinking-row">
                <span className="thinking-text">{t.chat.listening}</span>
              </div>
            )}

            {(recordingErrorMessage || voiceError) && (
              <div className="voice-error-row">{recordingErrorMessage || voiceError}</div>
            )}
          </div>

          <div className="chat-inputbar">
            <input
              className="text-input"
              type="text"
              placeholder={t.chat.inputPlaceholder}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button className="send-btn" onClick={handleSend} aria-label={t.chat.sendAria}>
              {/* Paper-plane send icon — visually distinct from the mic icon */}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path
                  d="M3 11.5L20.5 3.5L14.5 21L11.5 13.5L3 11.5Z"
                  fill="#1F3D24"
                  stroke="#1F3D24"
                  strokeWidth="1.2"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <button
              className={`mic-btn${isRecording ? ' recording' : ''}`}
              aria-label={isRecording ? t.chat.micStopAria : t.chat.micStartAria}
              onClick={handleMicClick}
            >
              {/* Microphone icon — visually distinct from the send icon */}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <rect x="9" y="2" width="6" height="12" rx="3" fill="#1F3D24" />
                <path
                  d="M5 11a7 7 0 0 0 14 0"
                  stroke="#1F3D24"
                  strokeWidth="2"
                  strokeLinecap="round"
                  fill="none"
                />
                <line x1="12" y1="18" x2="12" y2="22" stroke="#1F3D24" strokeWidth="2" strokeLinecap="round" />
                <line x1="8" y1="22" x2="16" y2="22" stroke="#1F3D24" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </button>
          </div>
        </div>

        <CitationSheet citation={selectedCitation} onClose={() => setSelectedCitation(null)} />
      </div>
    </div>
  );
}
