import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useVoiceRecorder } from './useVoiceRecorder';

class MockMediaRecorder {
  constructor(stream) {
    this.stream = stream;
    this.state = 'inactive';
    this.ondataavailable = null;
    this.onstop = null;
  }
  start() {
    this.state = 'recording';
  }
  stop() {
    this.state = 'inactive';
    // simulate one chunk of data arriving, then the recorder stopping
    this.ondataavailable?.({ data: new Blob(['fake-audio-chunk']) });
    this.onstop?.();
  }
}

describe('useVoiceRecorder', () => {
  beforeEach(() => {
    global.MediaRecorder = MockMediaRecorder;
    global.navigator.mediaDevices = {
      getUserMedia: vi.fn().mockResolvedValue({ id: 'fake-stream' }),
    };
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('starts not recording', () => {
    const { result } = renderHook(() => useVoiceRecorder());
    expect(result.current.isRecording).toBe(false);
  });

  it('requests microphone access and sets isRecording true on start', async () => {
    const { result } = renderHook(() => useVoiceRecorder());

    await act(async () => {
      await result.current.startRecording();
    });

    expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ audio: true });
    expect(result.current.isRecording).toBe(true);
  });

  it('resolves stopRecording with an audio blob and sets isRecording false', async () => {
    const { result } = renderHook(() => useVoiceRecorder());

    await act(async () => {
      await result.current.startRecording();
    });

    let blob;
    await act(async () => {
      blob = await result.current.stopRecording();
    });

    expect(blob).toBeInstanceOf(Blob);
    expect(result.current.isRecording).toBe(false);
  });

  it('sets an error and does not start recording when microphone access is denied', async () => {
    global.navigator.mediaDevices.getUserMedia = vi
      .fn()
      .mockRejectedValue(new Error('Permission denied'));

    const { result } = renderHook(() => useVoiceRecorder());

    await act(async () => {
      await result.current.startRecording();
    });

    expect(result.current.isRecording).toBe(false);
    expect(result.current.error).toBeTruthy();
  });

  it('resolves stopRecording with null if recording was never started', async () => {
    const { result } = renderHook(() => useVoiceRecorder());

    let blob;
    await act(async () => {
      blob = await result.current.stopRecording();
    });

    expect(blob).toBeNull();
  });
});
