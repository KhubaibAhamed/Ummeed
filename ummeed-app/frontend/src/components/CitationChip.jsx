export function CitationChip({ documentTitle, onSelect }) {
  return (
    <button className="citation-chip" onClick={onSelect}>
      {documentTitle}
    </button>
  );
}
