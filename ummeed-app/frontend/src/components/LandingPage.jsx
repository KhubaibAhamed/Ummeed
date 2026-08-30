import { useRef, useState } from 'react';
import { Header } from './Header';
import { LANGUAGES, getTranslations } from '../i18n';
import logo from '../assets/ummeed-logo.svg';

export function LandingPage({ onSelect }) {
  const [language, setLanguage] = useState('en');
  const [location, setLocation] = useState('');
  const [contactName, setContactName] = useState('');
  const [contactMessage, setContactMessage] = useState('');
  const [contactSent, setContactSent] = useState(false);

  const heroRef = useRef(null);
  const aboutRef = useRef(null);
  const contactRef = useRef(null);

  const t = getTranslations(language);

  const sectionRefs = { home: heroRef, about: aboutRef, contact: contactRef };
  function scrollTo(section) {
    sectionRefs[section]?.current?.scrollIntoView({ behavior: 'smooth' });
  }

  function handleGetStarted() {
    onSelect({ language, location });
  }

  function handleContactSubmit(e) {
    e.preventDefault();
    // No backend endpoint exists yet for contact messages — this simply
    // acknowledges the submission in the UI. Wire this up to a real
    // endpoint (e.g. POST /contact) when one is available.
    setContactSent(true);
    setContactName('');
    setContactMessage('');
  }

  return (
    <div className="landing-page">
      <Header t={t} onNavClick={scrollTo} />

      <section className="hero" ref={heroRef}>
        <img src={logo} alt="" className="hero-logo" />
        <p className="brand-name">{t.hero.title}</p>
        <p className="brand-tag">{t.hero.subtitle}</p>

        <p className="lang-label">{t.hero.langLabel}</p>
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
          placeholder={t.hero.locationPlaceholder}
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <button className="start-btn" onClick={handleGetStarted}>
          {t.hero.getStarted}
        </button>
      </section>

      <section className="about-section" ref={aboutRef}>
        <h2 className="section-title">{t.about.title}</h2>
        <p className="section-body">{t.about.body}</p>
      </section>

      <section className="contact-section" ref={contactRef}>
        <h2 className="section-title">{t.contact.title}</h2>
        <p className="section-body">{t.contact.body}</p>

        {contactSent ? (
          <p className="contact-thanks">✓</p>
        ) : (
          <form className="contact-form" onSubmit={handleContactSubmit}>
            <input
              className="contact-input"
              type="text"
              placeholder={t.contact.namePlaceholder}
              value={contactName}
              onChange={(e) => setContactName(e.target.value)}
              required
            />
            <textarea
              className="contact-textarea"
              placeholder={t.contact.messagePlaceholder}
              value={contactMessage}
              onChange={(e) => setContactMessage(e.target.value)}
              rows={4}
              required
            />
            <button className="contact-submit-btn" type="submit">
              {t.contact.send}
            </button>
          </form>
        )}
      </section>

      <footer className="site-footer">
        <img src={logo} alt="" className="footer-logo" />
        <span>
          {t.brandName} · {new Date().getFullYear()} · {t.footer.rights}
        </span>
      </footer>
    </div>
  );
}
