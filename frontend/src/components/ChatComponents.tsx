import React from 'react'

interface ChatMessageProps {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ role, content, timestamp }) => {
  return (
    <div className={`message ${role}`}>
      <div className="message-avatar">
        {role === 'user' ? 'U' : 'AI'}
      </div>
      <div className="message-content">
        <div className="message-role">
          {role === 'user' ? 'You' : 'Assistant'}
        </div>
        <div className="message-text">{content}</div>
        {timestamp && (
          <div className="message-time">
            {new Date(timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  )
}

interface TypingIndicatorProps {
  show?: boolean
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ show = false }) => {
  if (!show) return null

  return (
    <div className="typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  )
}

interface ChatInputProps {
  value: string
  onChange: (value: string) => void
  onSend: () => void
  onStream: () => void
  disabled?: boolean
  isStreaming?: boolean
}

export const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChange,
  onSend,
  onStream,
  disabled = false,
  isStreaming = false
}) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !disabled) {
      e.preventDefault()
      onSend()
    }
  }

  return (
    <div className="input-container">
      <div className="input-wrapper">
        <textarea
          className="message-input"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Shift+Enter for new line, Enter to send)"
          disabled={disabled}
        />
        <div className="input-actions">
          <button
            className="btn btn-clear"
            onClick={() => {}}
            disabled={disabled}
          >
            Clear
          </button>
          <button
            className="btn btn-stream"
            onClick={onStream}
            disabled={disabled || isStreaming || !value.trim()}
          >
            {isStreaming ? 'Streaming...' : 'Stream'}
          </button>
          <button
            className="btn btn-send"
            onClick={onSend}
            disabled={disabled || !value.trim()}
          >
            {disabled ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  )
}

interface WelcomeMessageProps {
  onExampleClick?: (example: string) => void
}

export const WelcomeMessage: React.FC<WelcomeMessageProps> = ({ onExampleClick }) => {
  const examples = [
    'Explain LangGraph and its benefits',
    'Help me plan a multi-step project',
    'What are best practices for AI agent development?'
  ]

  return (
    <div className="welcome-message">
      <h2>Welcome to LangGraph Agent</h2>
      <p>This AI agent uses LangGraph for multi-step reasoning with CopilotKit UI.</p>
      <div className="feature-list">
        <span>✓ Multi-step planning</span>
        <span>✓ Real-time streaming</span>
        <span>✓ Context-aware responses</span>
      </div>
      <div style={{ marginTop: '2rem' }}>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>Try an example:</p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          {examples.map((example, idx) => (
            <button
              key={idx}
              className="btn btn-stream"
              onClick={() => onExampleClick?.(example)}
              style={{ maxWidth: '300px' }}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
