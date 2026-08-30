import { useRef, useState } from 'react';

/**
 * Wraps the browser's MediaRecorder API for click-to-toggle voice input.
 *
 * Deliberately click-to-start / click-to-stop rather than press-and-hold:
 * press-and-hold caused a race where a quick tap could call stopRecording()
 * before the async getUserMedia() call had resolved and set up the
 * recorder, silently doing nothing. Toggling avoids that entirely.
 *
 * Returns an `errorType` ('denied' | 'unsupported' | null) instead of a
 * pre-formatted message so the caller can render a translated string.
 */
export function useVoiceRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [errorType, setErrorType] = useState(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);

  function isSupported() {
    return (
      typeof navigator !== 'undefined' &&
      navigator.mediaDevices &&
      typeof navigator.mediaDevices.getUserMedia === 'function' &&
      typeof window.MediaRecorder !== 'undefined'
    );
  }

  async function startRecording() {
    setErrorType(null);

    if (!isSupported()) {
      // getUserMedia is only exposed in secure contexts (https, or
      // http://localhost). If this app is opened via a LAN IP like
      // http://192.168.x.x:5173 instead of http://localhost:5173, the
      // browser hides the API entirely and this is what fires.
      setErrorType('unsupported');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      streamRef.current = stream;

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
    } catch {
      setErrorType('denied');
      setIsRecording(false);
    }
  }

  function stopRecording() {
    return new Promise((resolve) => {
      const recorder = mediaRecorderRef.current;
      if (!recorder) {
        setIsRecording(false);
        resolve(null);
        return;
      }

      recorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        mediaRecorderRef.current = null;
        setIsRecording(false);
        resolve(audioBlob);
      };

      recorder.stop();
    });
  }

  async function toggleRecording() {
    if (isRecording) {
      return stopRecording();
    }
    await startRecording();
    return null;
  }

  return { isRecording, errorType, startRecording, stopRecording, toggleRecording };
}
