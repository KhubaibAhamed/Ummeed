import logo from '../assets/ummeed-logo.svg';

/**
 * Shared header for both the landing page and the chat screen.
 * On the landing page it shows nav links that scroll to sections;
 * on the chat screen `nav` is omitted and it just shows the brand.
 */
export function Header({ t, onNavClick, showNav = true }) {
  return (
    <header className="site-header">
      <div className="site-header-brand">
        <img src={logo} alt={`${t.brandName} logo`} className="site-logo" />
        <span className="site-brand-name">{t.brandName}</span>
      </div>

      {showNav && (
        <nav className="site-nav">
          <button className="nav-link" onClick={() => onNavClick?.('home')}>
            {t.nav.home}
          </button>
          <button className="nav-link" onClick={() => onNavClick?.('about')}>
            {t.nav.about}
          </button>
          <button className="nav-link" onClick={() => onNavClick?.('contact')}>
            {t.nav.contact}
          </button>
        </nav>
      )}
    </header>
  );
}
