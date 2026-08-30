export function CitationSheet({ citation, onClose }) {
  if (!citation) return null;

  return (
    <div className="sheet-backdrop" onClick={onClose}>
      <div className="sheet" onClick={(e) => e.stopPropagation()}>
        <div className="sheet-handle" />
        <div className="sheet-header">
          <span className="sheet-source-tag">Source document</span>
          <button className="sheet-close" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>
        <p className="sheet-title">{citation.document_title}</p>
        <div className="sheet-snippet">{citation.snippet}</div>
        {citation.page_ref && <p className="sheet-meta">{citation.page_ref}</p>}
      </div>
    </div>
  );
}
