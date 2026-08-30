import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CitationSheet } from './CitationSheet';

describe('CitationSheet', () => {
  it('renders nothing when no citation is provided', () => {
    const { container } = render(<CitationSheet citation={null} onClose={() => {}} />);
    expect(container).toBeEmptyDOMElement();
  });

  it('renders the document title, snippet, and page reference when a citation is provided', () => {
    render(
      <CitationSheet
        citation={{
          document_title: 'ICAR Cotton Advisory 2025',
          snippet: 'Cercospora leaf spot appears during high humidity.',
          page_ref: 'p. 34',
        }}
        onClose={() => {}}
      />
    );

    expect(screen.getByText('ICAR Cotton Advisory 2025')).toBeInTheDocument();
    expect(
      screen.getByText('Cercospora leaf spot appears during high humidity.')
    ).toBeInTheDocument();
    expect(screen.getByText(/p\. 34/)).toBeInTheDocument();
  });

  it('calls onClose when the close control is activated', () => {
    const onClose = vi.fn();
    render(
      <CitationSheet
        citation={{ document_title: 'Doc', snippet: 'text', page_ref: null }}
        onClose={onClose}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /close/i }));

    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
