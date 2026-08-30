import { CitationChip } from './CitationChip';
import { LiveDataCard } from './LiveDataCard';

export function ChatBubble({ message, onCitationSelect }) {
  if (message.role === 'user') {
    return (
      <div className="bubble-row user">
        <div className="bubble user">{message.text}</div>
      </div>
    );
  }

  return (
    <div className="bubble-row">
      <div className="answer-stack">
        <div className={`bubble bot${message.isError ? ' error' : ''}`}>{message.text}</div>

        {message.citations?.length > 0 && (
          <div className="citation-row">
            {message.citations.map((citation, index) => (
              <CitationChip
                key={index}
                documentTitle={citation.document_title}
                onSelect={() => onCitationSelect(citation)}
              />
            ))}
          </div>
        )}

        {message.liveData?.map((item, index) => (
          <LiveDataCard key={index} label={item.label} value={item.value} />
        ))}
      </div>
    </div>
  );
}
