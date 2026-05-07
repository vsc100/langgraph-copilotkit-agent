import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp?: string
}

interface ChatSession {
  id: string
  messages: Message[]
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [streamContent, setStreamContent] = useState('')

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (useStream = false) => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    if (useStream) {
      await handleStreamMessage(userMessage)
    } else {
      await handleRegularMessage(userMessage)
    }
  }

  const handleRegularMessage = async (userMessage: Message) => {
    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        messages: [...messages, userMessage],
        session_id: 'default'
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Error: Unable to connect to the AI agent. Make sure the backend is running.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleStreamMessage = async (userMessage: Message) => {
    setIsStreaming(true)
    setStreamContent('')

    const eventSource = new EventSource(
      `${API_BASE}/stream?messages=${encodeURIComponent(JSON.stringify([...messages, userMessage]))}`
    )

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'chunk') {
        setStreamContent(prev => prev + data.content)
      } else if (data.type === 'stage') {
        // Can show stage indicators
        console.log('Stage:', data.content)
      } else if (data.type === 'complete') {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.content,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, assistantMessage])
        setStreamContent('')
        eventSource.close()
        setIsStreaming(false)
        setIsLoading(false)
      } else if (data.type === 'error') {
        const errorMessage: Message = {
          role: 'assistant',
          content: `Error: ${data.content}`,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, errorMessage])
        eventSource.close()
        setIsStreaming(false)
        setIsLoading(false)
      }
    }

    eventSource.onerror = () => {
      eventSource.close()
      setIsStreaming(false)
      setIsLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>LangGraph CopilotKit Agent</h1>
          <p>A multi-step AI agent with streaming support</p>
        </div>
      </header>

      {/* Messages Area */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>Welcome to LangGraph Agent</h2>
            <p>This AI agent uses LangGraph for multi-step reasoning with CopilotKit UI.</p>
            <div className="feature-list">
              <span>✓ Multi-step planning</span>
              <span>✓ Real-time streaming</span>
              <span>✓ Context-aware responses</span>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? 'U' : 'AI'}
                </div>
                <div className="message-content">
                  <div className="message-role">
                    {msg.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div className="message-text">{msg.content}</div>
                  {msg.timestamp && (
                    <div className="message-time">
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isStreaming && (
              <div className="message assistant streaming">
                <div className="message-avatar">AI</div>
                <div className="message-content">
                  <div className="message-role">Assistant</div>
                  <div className="message-text">{streamContent}</div>
                </div>
              </div>
            )}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            className="message-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                e.preventDefault()
                handleSendMessage(false)
              }
            }}
            placeholder="Type your message... (Shift+Enter for new line, Enter to send)"
            disabled={isLoading}
          />
          <div className="input-actions">
            <button
              className="btn btn-clear"
              onClick={clearChat}
              disabled={isLoading || messages.length === 0}
            >
              Clear
            </button>
            <button
              className="btn btn-stream"
              onClick={() => handleSendMessage(true)}
              disabled={isLoading || !input.trim()}
            >
              {isStreaming ? 'Streaming...' : 'Stream'}
            </button>
            <button
              className="btn btn-send"
              onClick={() => handleSendMessage(false)}
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <div className="status-bar">
        <span>Backend: {API_BASE}</span>
        <span>Status: {isLoading ? 'Processing...' : 'Ready'}</span>
      </div>
    </div>
  )
}

export default App
