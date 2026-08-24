import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Beef, ChevronDown, Globe, Menu, UserRound, X, Sparkles } from "lucide-react";

import "./Navbar.css";

const languageLabels = { en: "English", hi: "हिंदी", mr: "मराठी", gu: "ગુજરાતી" };

function Navbar({ onOpenLogin, onOpenContact }) {
  const { t, i18n } = useTranslation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [languageOpen, setLanguageOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("home");

  const closeMenu = () => setMenuOpen(false);

  const handleNavClick = (tabId) => {
    setActiveTab(tabId);
    closeMenu();
  };

  const changeLanguage = (language) => {
    i18n.changeLanguage(language);
    localStorage.setItem("language", language);
    setLanguageOpen(false);
  };

  return (
    <header className="navbar">
      <div className="navbar-container">
        <a href="#home" className="brand" onClick={() => handleNavClick("home")}>
          <span className="brand-icon">
            <Beef size={20} aria-hidden="true" />
          </span>
          <span className="brand-name">
            Breed<span>Vision</span>
          </span>
        </a>

        <nav className={`nav-links ${menuOpen ? "open" : ""}`} aria-label="Main navigation">
          <a
            href="#home"
            className={activeTab === "home" ? "active" : ""}
            onClick={() => handleNavClick("home")}
          >
            {t("common.home")}
          </a>
          <a
            href="#about"
            className={activeTab === "about" ? "active" : ""}
            onClick={() => handleNavClick("about")}
          >
            {t("common.about")}
          </a>
          <a
            href="#predict"
            className={activeTab === "predict" ? "active" : ""}
            onClick={() => handleNavClick("predict")}
          >
            {t("common.breeds")}
          </a>
          <a
            href="#how-it-works"
            className={activeTab === "how-it-works" ? "active" : ""}
            onClick={() => handleNavClick("how-it-works")}
          >
            {t("common.howItWorks")}
          </a>

          <div className="language-dropdown">
            <button
              className="language-button"
              type="button"
              onClick={() => setLanguageOpen(!languageOpen)}
              aria-expanded={languageOpen}
              aria-label="Select language"
            >
              <Globe size={15} />
              <span>{languageLabels[i18n.language] || "English"}</span>
              <ChevronDown size={14} className={languageOpen ? "rotate-icon" : ""} />
            </button>
            {languageOpen && (
              <div className="language-menu">
                {Object.entries(languageLabels).map(([code, label]) => (
                  <button
                    key={code}
                    className={i18n.language === code ? "active-lang" : ""}
                    type="button"
                    onClick={() => changeLanguage(code)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            )}
          </div>

          <a
            href="#contact"
            onClick={(event) => {
              event.preventDefault();
              closeMenu();
              onOpenContact();
            }}
          >
            {t("common.contact")}
          </a>
        </nav>

        <div className="nav-actions">
          <button className="login-btn" type="button" onClick={onOpenLogin}>
            <UserRound size={16} />
            <span>{t("common.login")}</span>
          </button>
          <a className="get-started-btn" href="#predict">
            <Sparkles size={15} />
            <span>{t("common.getStarted")}</span>
          </a>
        </div>

        <button
          className="mobile-menu-btn"
          type="button"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label={menuOpen ? "Close navigation" : "Open navigation"}
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
    </header>
  );
}

export default Navbar;

