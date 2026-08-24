import { useTranslation } from "react-i18next";
import { Mail, Phone } from "lucide-react";
import "./Footer.css";

function Footer({ onOpenContact }) {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        
        {/* Brand Info */}
        <div className="footer-brand">
          <a href="#home" className="footer-brand-logo">
            <span className="footer-emoji">🐄</span>
            <span className="footer-brand-name">
              Breed<span>Vision</span>
            </span>
          </a>
          <p className="footer-tagline">
            {t("footer.tagline")}
          </p>
        </div>

        {/* Quick Links */}
        <div className="footer-links">
          <h3>{t("footer.quickLinks")}</h3>
          <ul>
            <li>
              <a href="#home">{t("common.home")}</a>
            </li>
            <li>
              <a href="#about">{t("common.about")}</a>
            </li>
            <li>
              <a href="#breeds">{t("common.breeds")}</a>
            </li>
            <li>
              <a href="#how-it-works">{t("common.howItWorks")}</a>
            </li>
            <li>
              <a 
                href="#contact" 
                onClick={(e) => {
                  e.preventDefault();
                  onOpenContact();
                }}
              >
                {t("common.contact")}
              </a>
            </li>
          </ul>
        </div>

        {/* Contact & Socials */}
        <div className="footer-connect">
          <h3>{t("footer.connect")}</h3>
          <div className="footer-contact-info">
            <div className="contact-item">
              <Mail size={16} />
              <a href="mailto:info@breedvision.com">info@breedvision.com</a>
            </div>
            <div className="contact-item">
              <Phone size={16} />
              <a href="tel:+911234567890">+91 12345 67890</a>
            </div>
          </div>
          <div className="footer-social-icons">
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
              </svg>
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"/>
              </svg>
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>
              </svg>
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>
                <rect x="2" y="9" width="4" height="12"/>
                <circle cx="4" cy="4" r="2"/>
              </svg>
            </a>
          </div>
        </div>

      </div>

      <div className="footer-bottom">
        <p>© {currentYear} BreedVision. {t("footer.rights")}</p>
      </div>
    </footer>
  );
}

export default Footer;
