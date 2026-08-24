import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  UserRound,
  ChevronDown,
  Menu,
  X
} from "lucide-react";

import "./Navbar.css";


function Navbar({ onOpenLogin, onOpenContact }) {
  const { t, i18n } = useTranslation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [languageOpen, setLanguageOpen] = useState(false);

  // Map language codes to labels
  const languageLabels = {
    en: "English",
    hi: "हिंदी",
    mr: "मराठी",
    gu: "ગુજરાતી"
  };

  const currentLanguageLabel = languageLabels[i18n.language] || "English";

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    localStorage.setItem("language", lng);
    setLanguageOpen(false);
  };

  return (
    <header className="navbar">

      <a href="/" className="brand">
        <div className="brand-icon">
          🐄
        </div>

        <span className="brand-name">
          Breed<span>Vision</span>
        </span>
      </a>

      <nav className={`nav-links ${menuOpen ? "open" : ""}`}>
        <a href="#home" className="active">
          {t("common.home")}
        </a>

        <a href="#about">{t("common.about")}</a>

        <a href="#breeds">
          {t("common.breeds")}
          <ChevronDown size={15} />
        </a>

        <a href="#how-it-works">
          {t("common.howItWorks")}
        </a>

        <div className="language-dropdown">
          <button
            className="language-button"
            onClick={() => setLanguageOpen(!languageOpen)}
          >
            {currentLanguageLabel}
            <ChevronDown
              size={16}
              className={languageOpen ? "rotate-icon" : ""}
            />
          </button>

          {languageOpen && (
            <div className="language-menu">
              <button
                className={i18n.language === "en" ? "active-lang" : ""}
                onClick={() => changeLanguage("en")}
              >
                English
              </button>

              <button
                className={i18n.language === "hi" ? "active-lang" : ""}
                onClick={() => changeLanguage("hi")}
              >
                हिंदी
              </button>

              <button
                className={i18n.language === "mr" ? "active-lang" : ""}
                onClick={() => changeLanguage("mr")}
              >
                मराठी
              </button>

              <button
                className={i18n.language === "gu" ? "active-lang" : ""}
                onClick={() => changeLanguage("gu")}
              >
                ગુજરાતી
              </button>
            </div>
          )}
        </div>

        <a
        
  href="#contact"
  onClick={(e) => {
    e.preventDefault();
    onOpenContact();
  }}
>
  {t("common.contact")} Us
</a>
      </nav>

      <div className="nav-actions">

        <button className="login-btn" onClick={onOpenLogin}>
          <UserRound size={17} />
          {t("common.login")}
        </button>

        <button className="get-started-btn">
          {t("common.getStarted")}
        </button>

      </div>

      <button
        className="mobile-menu-btn"
        onClick={() => setMenuOpen(!menuOpen)}
      >
        {menuOpen ? <X /> : <Menu />}
      </button>

    </header>
  );
}

export default Navbar;