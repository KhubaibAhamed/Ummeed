import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { LanguageSelect } from './LanguageSelect';

describe('LanguageSelect', () => {
  it('renders the brand name', () => {
    render(<LanguageSelect onSelect={() => {}} />);
    expect(screen.getByText('Ummeed')).toBeInTheDocument();
  });

  it('renders all four language options', () => {
    render(<LanguageSelect onSelect={() => {}} />);
    expect(screen.getByText('English')).toBeInTheDocument();
    expect(screen.getByText('हिंदी')).toBeInTheDocument();
    expect(screen.getByText('తెలుగు')).toBeInTheDocument();
    expect(screen.getByText('ಕನ್ನಡ')).toBeInTheDocument();
  });

  it('highlights a language chip when tapped, without navigating yet', () => {
    render(<LanguageSelect onSelect={() => {}} />);

    fireEvent.click(screen.getByText('తెలుగు'));

    expect(screen.getByText('తెలుగు')).toHaveClass('active');
  });

  it('the Start button is disabled until a language is chosen', () => {
    render(<LanguageSelect onSelect={() => {}} />);
    expect(screen.getByRole('button', { name: /start/i })).toBeDisabled();
  });

  it('calls onSelect with language and location when Start is tapped', () => {
    const onSelect = vi.fn();
    render(<LanguageSelect onSelect={onSelect} />);

    fireEvent.click(screen.getByText('తెలుగు'));
    fireEvent.change(screen.getByPlaceholderText(/your area/i), {
      target: { value: 'Guntur' },
    });
    fireEvent.click(screen.getByRole('button', { name: /start/i }));

    expect(onSelect).toHaveBeenCalledWith({ language: 'te', location: 'Guntur' });
  });

  it('calls onSelect with an empty location when none is entered — live data degrades gracefully', () => {
    const onSelect = vi.fn();
    render(<LanguageSelect onSelect={onSelect} />);

    fireEvent.click(screen.getByText('English'));
    fireEvent.click(screen.getByRole('button', { name: /start/i }));

    expect(onSelect).toHaveBeenCalledWith({ language: 'en', location: '' });
  });
});
