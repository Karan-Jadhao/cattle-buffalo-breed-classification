import { useEffect } from "react";
import ReactDOM from "react-dom";
import { X } from "lucide-react";
import "./Modal.css";

function Modal({ isOpen, onClose, children }) {
  useEffect(() => {
    if (!isOpen) return;
    document.body.style.overflow = "hidden";
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay show" onClick={onClose} role="presentation">
      <div
        className="modal-container show"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Dialog"
      >
        <button className="modal-close-btn" onClick={onClose} aria-label="Close modal">
          <X size={20} />
        </button>
        <div className="modal-content">
          {children}
        </div>
      </div>
    </div>,
    document.getElementById("modal-root")
  );
}

export default Modal;
