import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { sendQuery, transcribeAudio } from './client';

describe('sendQuery', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('posts to /query with text, language, and location', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        answer: 'Remove affected leaves.',
        citations: [],
        live_data: [],
        response_time_ms: 1200,
        grounded: true,
      }),
    });

    await sendQuery({ text: 'Why are my leaves yellow?', language: 'en', location: 'Guntur' });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/query'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({
          text: 'Why are my leaves yellow?',
          language: 'en',
          location: 'Guntur',
        }),
      })
    );
  });

  it('returns the parsed response body on success', async () => {
    const mockResponse = {
      answer: 'Remove affected leaves.',
      citations: [{ document_title: 'ICAR Cotton Advisory', snippet: 'text', page_ref: null }],
      live_data: [],
      response_time_ms: 1200,
      grounded: true,
    };
    global.fetch.mockResolvedValueOnce({ ok: true, json: async () => mockResponse });

    const result = await sendQuery({ text: 'test', language: 'en' });

    expect(result).toEqual(mockResponse);
  });

  it('throws a readable error when the response is not ok', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Internal error' }),
    });

    await expect(sendQuery({ text: 'test', language: 'en' })).rejects.toThrow();
  });
});

describe('transcribeAudio', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('posts audio as multipart form data to /transcribe', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ text: 'transcribed text', detected_language: 'te-IN' }),
    });

    const fakeBlob = new Blob(['fake audio'], { type: 'audio/wav' });
    await transcribeAudio(fakeBlob);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/transcribe'),
      expect.objectContaining({ method: 'POST' })
    );
    // FormData bodies aren't directly comparable, but we can confirm one was sent
    const callArgs = global.fetch.mock.calls[0][1];
    expect(callArgs.body).toBeInstanceOf(FormData);
  });

  it('returns transcribed text and detected language on success', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ text: 'transcribed text', detected_language: 'te-IN' }),
    });

    const result = await transcribeAudio(new Blob(['audio']));

    expect(result).toEqual({ text: 'transcribed text', detected_language: 'te-IN' });
  });

  it('throws a readable error when transcription fails', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Couldn't understand that audio clearly" }),
    });

    await expect(transcribeAudio(new Blob(['audio']))).rejects.toThrow();
  });
});
