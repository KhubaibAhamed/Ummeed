import { useState } from 'react';

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'te', label: 'తెలుగు' },
  { code: 'kn', label: 'ಕನ್ನಡ' },
];

export function LanguageSelect({ onSelect }) {
  const [language, setLanguage] = useState(null);
  const [location, setLocation] = useState('');

  function handleStart() {
    onSelect({ language, location });
  }

  return (
    <div className="splash">
      <svg className="logo-mark" viewBox="0 0 240 240" width="60" height="60">
        <path
          d="M 46 150 A 74 74 0 0 1 194 150"
          fill="none"
          stroke="#E8A33D"
          strokeWidth="6"
          strokeLinecap="round"
        />
        <path
          d="M120 150 C 120 128, 120 112, 120 96"
          fill="none"
          stroke="#2F6B3A"
          strokeWidth="7"
          strokeLinecap="round"
        />
        <path
          d="M120 118 C 100 108, 84 112, 72 128 C 92 134, 108 130, 120 118 Z"
          fill="#2F6B3A"
        />
        <path
          d="M120 100 C 138 88, 156 90, 170 104 C 150 112, 132 110, 120 100 Z"
          fill="#2F6B3A"
        />
        <circle cx="120" cy="150" r="9" fill="#E8A33D" />
      </svg>

      <p className="brand-name">Ummeed</p>
      <p className="brand-tag">"Talk to the field. Hear back with proof."</p>

      <p className="lang-label">Speak or type in</p>
      <div className="lang-chips">
        {LANGUAGES.map(({ code, label }) => (
          <button
            key={code}
            className={`chip${language === code ? ' active' : ''}`}
            onClick={() => setLanguage(code)}
          >
            {label}
          </button>
        ))}
      </div>

      <input
        className="location-input"
        type="text"
        placeholder="Your area, e.g. Guntur (optional)"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      <button className="start-btn" onClick={handleStart} disabled={!language}>
        Start
      </button>
    </div>
  );
}
