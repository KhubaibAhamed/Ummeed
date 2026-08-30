import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useChat } from './useChat';
import * as apiClient from '../api/client';

vi.mock('../api/client');

afterEach(() => {
  vi.restoreAllMocks();
});

describe('useChat', () => {
  it('starts with no messages and not loading', () => {
    const { result } = renderHook(() => useChat({ language: 'en' }));

    expect(result.current.messages).toEqual([]);
    expect(result.current.isLoading).toBe(false);
  });

  it('immediately appends the user message before the API call resolves', async () => {
    let resolveQuery;
    apiClient.sendQuery.mockReturnValue(new Promise((resolve) => (resolveQuery = resolve)));

    const { result } = renderHook(() => useChat({ language: 'en' }));

    act(() => {
      result.current.sendMessage('Why are my leaves yellow?');
    });

    expect(result.current.messages).toHaveLength(1);
    expect(result.current.messages[0]).toMatchObject({
      role: 'user',
      text: 'Why are my leaves yellow?',
    });
    expect(result.current.isLoading).toBe(true);

    // clean up the pending promise
    await act(async () => {
      resolveQuery({ answer: 'ok', citations: [], live_data: [], grounded: true });
    });
  });

  it('appends a grounded bot message with citations and live data on success', async () => {
    apiClient.sendQuery.mockResolvedValue({
      answer: 'Remove affected leaves and monitor humidity.',
      citations: [{ document_title: 'ICAR Cotton Advisory', snippet: 'text', page_ref: null }],
      live_data: [{ label: 'Weather', value: '68% humidity, falling', source: 'OpenWeatherMap' }],
      grounded: true,
      response_time_ms: 1200,
    });

    const { result } = renderHook(() => useChat({ language: 'en' }));

    await act(async () => {
      await result.current.sendMessage('Why are my leaves yellow?');
    });

    expect(result.current.messages).toHaveLength(2);
    const botMessage = result.current.messages[1];
    expect(botMessage.role).toBe('bot');
    expect(botMessage.text).toBe('Remove affected leaves and monitor humidity.');
    expect(botMessage.grounded).toBe(true);
    expect(botMessage.citations).toHaveLength(1);
    expect(botMessage.liveData).toHaveLength(1);
    expect(result.current.isLoading).toBe(false);
  });

  it('appends an honest ungrounded message when the backend has no confident match', async () => {
    apiClient.sendQuery.mockResolvedValue({
      answer: "I don't have reliable information on that.",
      citations: [],
      live_data: [],
      grounded: false,
      response_time_ms: 400,
    });

    const { result } = renderHook(() => useChat({ language: 'en' }));

    await act(async () => {
      await result.current.sendMessage('What is the meaning of life?');
    });

    const botMessage = result.current.messages[1];
    expect(botMessage.grounded).toBe(false);
    expect(botMessage.citations).toEqual([]);
  });

  it('appends a friendly error message and stops loading when the API call fails', async () => {
    apiClient.sendQuery.mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useChat({ language: 'en' }));

    await act(async () => {
      await result.current.sendMessage('test question');
    });

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[1].isError).toBe(true);
  });

  it('passes the current language and location through to sendQuery', async () => {
    apiClient.sendQuery.mockResolvedValue({
      answer: 'ok', citations: [], live_data: [], grounded: true,
    });

    const { result } = renderHook(() => useChat({ language: 'hi', location: 'Guntur' }));

    await act(async () => {
      await result.current.sendMessage('test');
    });

    expect(apiClient.sendQuery).toHaveBeenCalledWith({
      text: 'test',
      language: 'hi',
      location: 'Guntur',
    });
  });
});
