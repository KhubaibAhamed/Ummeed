import { useState } from 'react';
import { sendQuery } from '../api/client';
import { getTranslations } from '../i18n';

let nextId = 1;
function generateId() {
  return `msg-${nextId++}`;
}

/**
 * Manages the chat conversation: message history, in-flight loading state, and
 * the API call itself. The bot message shape directly mirrors the backend's
 * QueryResponse — grounded/citations/liveData flow straight through so the UI
 * can render the "trust made visible" distinction from Phase 5 without any
 * translation layer in between.
 */
export function useChat({ language, location }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const t = getTranslations(language);

  async function sendMessage(text) {
    const userMessage = { id: generateId(), role: 'user', text };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendQuery({ text, language, location });
      const botMessage = {
        id: generateId(),
        role: 'bot',
        text: response.answer,
        citations: response.citations || [],
        liveData: response.live_data || [],
        grounded: response.grounded,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch {
      const errorMessage = {
        id: generateId(),
        role: 'bot',
        text: t.chat.connectionError,
        citations: [],
        liveData: [],
        grounded: false,
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  return { messages, isLoading, sendMessage };
}
