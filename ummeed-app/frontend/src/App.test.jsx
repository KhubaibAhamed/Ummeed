import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import App from './App';

describe('App navigation', () => {
  it('shows the language select screen first', () => {
    render(<App />);
    expect(screen.getByText('Ummeed')).toBeInTheDocument();
    expect(screen.getByText('English')).toBeInTheDocument();
  });

  it('shows the chat screen after a language is selected and Start is tapped', () => {
    render(<App />);

    fireEvent.click(screen.getByText('English'));
    fireEvent.click(screen.getByRole('button', { name: /start/i }));

    expect(screen.getByPlaceholderText(/ask about your crop/i)).toBeInTheDocument();
    expect(screen.queryByText('Speak or type in')).not.toBeInTheDocument();
  });
});
