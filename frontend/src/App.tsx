import { useEffect, useState } from 'react'
import './App.css'
import {
  createSession,
  sendMessage,
} from './api/client'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
}

const SESSION_STORAGE_KEY = 'moin_chat_session_id'

function App() {
  const [isOpen, setIsOpen] = useState(true)
  const [message, setMessage] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: 'assistant',
      content:
        '👋 Hello! Welcome to MoinSystems AI. How can I help you today?',
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const existingSessionId = sessionStorage.getItem(
      SESSION_STORAGE_KEY,
    )

    if (existingSessionId) {
      setSessionId(existingSessionId)
      return
    }

    createSession()
      .then((session) => {
        sessionStorage.setItem(
          SESSION_STORAGE_KEY,
          session.session_id,
        )

        setSessionId(session.session_id)
      })
      .catch(() => {
        setError(
          'Unable to start the chat. Please refresh and try again.',
        )
      })
  }, [])

  const handleSend = async () => {
    const trimmedMessage = message.trim()

    if (!trimmedMessage || !sessionId || isLoading) {
      return
    }

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: trimmedMessage,
    }

    setMessages((current) => [
      ...current,
      userMessage,
    ])

    setMessage('')
    setError(null)
    setIsLoading(true)

    try {
      const response = await sendMessage(
        sessionId,
        trimmedMessage,
      )

      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
      }

      setMessages((current) => [
        ...current,
        assistantMessage,
      ])
    } catch {
      setError(
        'Sorry, something went wrong. Please try again.',
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      {!isOpen && (
        <button
          className="chat-launcher"
          onClick={() => setIsOpen(true)}
          aria-label="Open MoinSystems AI chatbot"
        >
          💬
        </button>
      )}

      {isOpen && (
        <section
          className="chat-widget"
          aria-label="MoinSystems AI chatbot"
        >
          <header className="chat-header">
            <div>
              <h1>MoinSystems AI</h1>
              <span>AI Assistant</span>
            </div>

            <button
              className="close-button"
              onClick={() => setIsOpen(false)}
              aria-label="Minimize chatbot"
            >
              −
            </button>
          </header>

          <main className="chat-messages">
            {messages.map((item) => (
              <div
                key={item.id}
                className={`message ${
                  item.role === 'user'
                    ? 'user-message'
                    : 'assistant-message'
                }`}
              >
                {item.content}
              </div>
            ))}

            {isLoading && (
              <div className="message assistant-message">
                Thinking...
              </div>
            )}

            {error && (
              <div
                className="chat-error"
                role="alert"
              >
                {error}
              </div>
            )}
          </main>

          <form
            className="chat-composer"
            onSubmit={(event) => {
              event.preventDefault()
              handleSend()
            }}
          >
            <input
              type="text"
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              placeholder="Type your message..."
              aria-label="Type your message"
              disabled={!sessionId || isLoading}
            />

            <button
              type="submit"
              disabled={!sessionId || isLoading}
            >
              {isLoading ? '...' : 'Send'}
            </button>
          </form>
        </section>
      )}
    </div>
  )
}

export default App