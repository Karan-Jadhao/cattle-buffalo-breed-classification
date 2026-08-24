import { useState } from "react";
import { useTranslation } from "react-i18next";
import { User, Mail, FileText, MessageSquare, Send } from "lucide-react";
import Modal from "./Modal";
import "./ContactModal.css";

function ContactModal({ isOpen, onClose }) {
  const { t } = useTranslation();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate contact form submission
    alert(`Thank you ${name}, your message has been simulated to be sent!`);
    setName("");
    setEmail("");
    setSubject("");
    setMessage("");
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <div className="contact-modal-header">
        <div className="contact-logo-icon">
          <Mail size={24} />
        </div>
        <h2>{t("contact.title")}</h2>
      </div>

      <form className="contact-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="contact-name">{t("contact.name")}</label>
          <div className="input-field-wrapper">
            <User size={18} className="input-icon" />
            <input
              id="contact-name"
              type="text"
              placeholder={t("contact.namePlaceholder")}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="contact-email">{t("common.email")}</label>
          <div className="input-field-wrapper">
            <Mail size={18} className="input-icon" />
            <input
              id="contact-email"
              type="email"
              placeholder={t("contact.emailPlaceholder")}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="contact-subject">{t("contact.subject")}</label>
          <div className="input-field-wrapper">
            <FileText size={18} className="input-icon" />
            <input
              id="contact-subject"
              type="text"
              placeholder={t("contact.subjectPlaceholder")}
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label htmlFor="contact-message">{t("contact.message")}</label>
          <div className="input-field-wrapper textarea-wrapper">
            <MessageSquare size={18} className="input-icon textarea-icon" />
            <textarea
              id="contact-message"
              placeholder={t("contact.messagePlaceholder")}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={4}
              required
            />
          </div>
        </div>

        <button type="submit" className="contact-submit-btn">
          <Send size={16} />
          {t("contact.sendBtn")}
        </button>
      </form>
    </Modal>
  );
}

export default ContactModal;
