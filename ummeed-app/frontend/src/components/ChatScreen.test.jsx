import { act, fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ChatScreen } from './ChatScreen';
import * as apiClient from '../api/client';

vi.mock('../api/client');

class MockMediaRecorder {
  constructor(stream) {
    this.stream = stream;
    this.ondataavailable = null;
    this.onstop = null;
  }
  start() {}
  stop() {
    this.ondataavailable?.({ data: new Blob(['fake-chunk']) });
    this.onstop?.();
  }
}

beforeEach(() => {
  global.MediaRecorder = MockMediaRecorder;
  global.navigator.mediaDevices = {
    getUserMedia: vi.fn().mockResolvedValue({ id: 'fake-stream' }),
  };
});

afterEach(() => {
  vi.resetAllMocks();
});

describe('ChatScreen', () => {
  it('sends a typed question and displays the grounded answer with a citation', async () => {
    const user = userEvent.setup();
    apiClient.sendQuery.mockResolvedValue({
      answer: 'Remove affected leaves and monitor humidity.',
      citations: [{ document_title: 'ICAR Cotton Advisory 2025', snippet: 'text', page_ref: null }],
      live_data: [],
      grounded: true,
    });

    render(<ChatScreen language="en" />);

    const input = screen.getByPlaceholderText(/ask about your crop/i);
    await user.type(input, 'Why are my cotton leaves yellow?');
    await user.click(screen.getByRole('button', { name: /send/i }));

    expect(screen.getByText('Why are my cotton leaves yellow?')).toBeInTheDocument();

    await waitFor(() =>
      expect(
        screen.getByText('Remove affected leaves and monitor humidity.')
      ).toBeInTheDocument()
    );
    expect(screen.getByText('ICAR Cotton Advisory 2025')).toBeInTheDocument();
  });

  it('opens the citation sheet when a citation chip is tapped, and closes it', async () => {
    const user = userEvent.setup();
    apiClient.sendQuery.mockResolvedValue({
      answer: 'Remove affected leaves.',
      citations: [
        {
          document_title: 'ICAR Cotton Advisory 2025',
          snippet: 'Cercospora leaf spot appears during high humidity.',
          page_ref: 'p. 34',
        },
      ],
      live_data: [],
      grounded: true,
    });

    render(<ChatScreen language="en" />);
    await user.type(screen.getByPlaceholderText(/ask about your crop/i), 'test question');
    await user.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => screen.getByText('ICAR Cotton Advisory 2025'));
    await user.click(screen.getByText('ICAR Cotton Advisory 2025'));

    expect(
      screen.getByText('Cercospora leaf spot appears during high humidity.')
    ).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: /close/i }));

    expect(
      screen.queryByText('Cercospora leaf spot appears during high humidity.')
    ).not.toBeInTheDocument();
  });

  it('shows a thinking indicator while waiting for the response', async () => {
    let resolveQuery;
    apiClient.sendQuery.mockReturnValue(new Promise((resolve) => (resolveQuery = resolve)));
    const user = userEvent.setup();

    render(<ChatScreen language="en" />);
    await user.type(screen.getByPlaceholderText(/ask about your crop/i), 'test');
    await user.click(screen.getByRole('button', { name: /send/i }));

    expect(screen.getByText(/checking/i)).toBeInTheDocument();

    await waitFor(async () => {
      resolveQuery({ answer: 'ok', citations: [], live_data: [], grounded: true });
    });
  });

  it('does not send an empty message', async () => {
    const user = userEvent.setup();
    render(<ChatScreen language="en" />);

    await user.click(screen.getByRole('button', { name: /send/i }));

    expect(apiClient.sendQuery).not.toHaveBeenCalled();
  });

  it('records, transcribes, and auto-sends a voice question on mic release', async () => {
    apiClient.transcribeAudio.mockResolvedValue({
      text: 'Why are my cotton leaves yellow?',
      detected_language: 'en-IN',
    });
    apiClient.sendQuery.mockResolvedValue({
      answer: 'Remove affected leaves.',
      citations: [],
      live_data: [],
      grounded: true,
    });

    render(<ChatScreen language="en" />);
    const micButton = screen.getByRole('button', { name: /hold to speak/i });

    await act(async () => {
      fireEvent.mouseDown(micButton);
    });
    await act(async () => {
      fireEvent.mouseUp(micButton);
    });

    await waitFor(() => expect(apiClient.transcribeAudio).toHaveBeenCalled());
    await waitFor(() =>
      expect(screen.getByText('Why are my cotton leaves yellow?')).toBeInTheDocument()
    );
    await waitFor(() => expect(screen.getByText('Remove affected leaves.')).toBeInTheDocument());
  });

  it('shows a friendly error when transcription fails, without crashing', async () => {
    apiClient.transcribeAudio.mockRejectedValue(new Error('Sarvam API error'));

    render(<ChatScreen language="en" />);
    const micButton = screen.getByRole('button', { name: /hold to speak/i });

    await act(async () => {
      fireEvent.mouseDown(micButton);
    });
    await act(async () => {
      fireEvent.mouseUp(micButton);
    });

    await waitFor(() =>
      expect(screen.getByText(/couldn't hear that clearly/i)).toBeInTheDocument()
    );
    expect(apiClient.sendQuery).not.toHaveBeenCalled();
  });
});
