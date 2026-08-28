const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface SessionResponse {
  session_id: string
  state: string
}

export interface ChatMessageResponse {
  session_id: string
  state: string
  response: string
}

export interface LeadCaptureRequest {
  session_id: string
  field_name: string
  value: string
}

export interface LeadCaptureResponse {
  session_id: string
  next_required_field: string | null
  lead_complete: boolean
}

async function request<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
      ...options,
    },
  )

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'Request failed.',
    }))

    throw new Error(
      error.detail || 'Request failed.',
    )
  }

  return response.json() as Promise<T>
}

export function createSession(): Promise<SessionResponse> {
  return request<SessionResponse>('/sessions', {
    method: 'POST',
  })
}

export function sendMessage(
  sessionId: string,
  message: string,
): Promise<ChatMessageResponse> {
  return request<ChatMessageResponse>(
    '/chat/messages',
    {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        message,
      }),
    },
  )
}

export function captureLead(
  data: LeadCaptureRequest,
): Promise<LeadCaptureResponse> {
  return request<LeadCaptureResponse>(
    '/lead-capture',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
  )
}