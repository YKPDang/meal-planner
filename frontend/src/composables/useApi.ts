const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function fetchJson<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }

  if (response.status === 204) {
    return null as T
  }

  return response.json()
}
