import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Mail, Lock, UserRound } from "lucide-react";
import Modal from "./Modal";
import "./LoginModal.css";

function LoginModal({ isOpen, onClose }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate login for UI purposes
    alert(`Logged in as: ${email}`);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="login-modal-header">
        <div className="login-logo-icon">
          <UserRound size={24} />
        </div>
        <h2>{t("login.title")}</h2>
      </div>

      <form className="login-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="login-email">{t("common.email")}</label>
          <div className="input-field-wrapper">
            <Mail size={18} className="input-icon" />
            <input
              id="login-email"
              type="email"
              placeholder={t("login.emailPlaceholder")}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="login-password">{t("common.password")}</label>
          <div className="input-field-wrapper">
            <Lock size={18} className="input-icon" />
            <input
              id="login-password"
              type="password"
              placeholder={t("login.passwordPlaceholder")}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="login-actions">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            />
            <span>{t("login.rememberMe")}</span>
          </label>
          <a href="#forgot" className="forgot-link" onClick={(e) => e.preventDefault()}>
            {t("login.forgotPassword")}
          </a>
        </div>

        <button type="submit" className="login-submit-btn">
          {t("common.login")}
        </button>

        <div className="signup-prompt">
          <span>{t("login.dontHaveAccount")} </span>
          <a href="#signup" className="signup-link" onClick={(e) => e.preventDefault()}>
            {t("login.signUp")}
          </a>
        </div>
      </form>
    </Modal>
  );
}

export default LoginModal;
