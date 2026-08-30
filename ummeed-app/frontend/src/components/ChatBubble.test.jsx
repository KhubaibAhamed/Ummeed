import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ChatBubble } from './ChatBubble';

const groundedBotMessage = {
  id: 'msg-2',
  role: 'bot',
  text: 'Remove affected leaves and monitor humidity.',
  citations: [{ document_title: 'ICAR Cotton Advisory 2025', snippet: 'text', page_ref: null }],
  liveData: [{ label: 'Weather', value: '68% humidity, falling', source: 'OpenWeatherMap' }],
  grounded: true,
};

const ungroundedBotMessage = {
  id: 'msg-3',
  role: 'bot',
  text: "I don't have reliable information on that.",
  citations: [],
  liveData: [],
  grounded: false,
};

const userMessage = {
  id: 'msg-1',
  role: 'user',
  text: 'Why are my cotton leaves yellow?',
};

describe('ChatBubble', () => {
  it('renders a user message', () => {
    render(<ChatBubble message={userMessage} onCitationSelect={() => {}} />);
    expect(screen.getByText('Why are my cotton leaves yellow?')).toBeInTheDocument();
  });

  it('renders a grounded bot message with citation chips and live data cards', () => {
    render(<ChatBubble message={groundedBotMessage} onCitationSelect={() => {}} />);

    expect(screen.getByText('Remove affected leaves and monitor humidity.')).toBeInTheDocument();
    expect(screen.getByText('ICAR Cotton Advisory 2025')).toBeInTheDocument();
    expect(screen.getByText('Weather')).toBeInTheDocument();
  });

  it('renders an ungrounded message without any citation chips or live data cards', () => {
    render(<ChatBubble message={ungroundedBotMessage} onCitationSelect={() => {}} />);

    expect(screen.getByText("I don't have reliable information on that.")).toBeInTheDocument();
    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('calls onCitationSelect with the clicked citation', () => {
    const onCitationSelect = vi.fn();
    render(<ChatBubble message={groundedBotMessage} onCitationSelect={onCitationSelect} />);

    fireEvent.click(screen.getByText('ICAR Cotton Advisory 2025'));

    expect(onCitationSelect).toHaveBeenCalledWith(groundedBotMessage.citations[0]);
  });
});
