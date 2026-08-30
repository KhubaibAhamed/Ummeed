import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CitationChip } from './CitationChip';
import { LiveDataCard } from './LiveDataCard';

describe('CitationChip', () => {
  it('renders the document title', () => {
    render(<CitationChip documentTitle="ICAR Cotton Advisory 2025" onSelect={() => {}} />);
    expect(screen.getByText(/ICAR Cotton Advisory 2025/)).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const onSelect = vi.fn();
    render(<CitationChip documentTitle="ICAR Cotton Advisory 2025" onSelect={onSelect} />);

    fireEvent.click(screen.getByRole('button'));

    expect(onSelect).toHaveBeenCalledTimes(1);
  });
});

describe('LiveDataCard', () => {
  it('renders label, value, and does not expose raw source as visible clutter by default', () => {
    render(<LiveDataCard label="Weather" value="68% humidity, falling" source="OpenWeatherMap" />);

    expect(screen.getByText('Weather')).toBeInTheDocument();
    expect(screen.getByText('68% humidity, falling')).toBeInTheDocument();
  });
});
