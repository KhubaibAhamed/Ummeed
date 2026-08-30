const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function parseErrorOrThrow(response) {
  let detail = `Request failed with status ${response.status}`;
  try {
    const body = await response.json();
    if (body?.detail) detail = body.detail;
  } catch {
    // response wasn't JSON — fall back to the generic message above
  }
  throw new Error(detail);
}

/**
 * Sends a farmer's question to the backend RAG pipeline.
 * @param {{text: string, language: string, location?: string}} params
 */
export async function sendQuery({ text, language, location }) {
  const response = await fetch(`${BASE_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language, location }),
  });

  if (!response.ok) {
    await parseErrorOrThrow(response);
  }

  return response.json();
}

/**
 * Sends a recorded audio blob to the backend for transcription.
 * @param {Blob} audioBlob
 */
export async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  const response = await fetch(`${BASE_URL}/transcribe`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    await parseErrorOrThrow(response);
  }

  return response.json();
}
