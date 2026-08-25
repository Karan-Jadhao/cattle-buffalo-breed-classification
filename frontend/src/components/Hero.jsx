import { useTranslation } from "react-i18next";
import { ArrowRight, CheckCircle2, ScanLine, Sparkles, ShieldCheck } from "lucide-react";

import heroShowcase from "../assets/hero_showcase.png";
import "./Hero.css";

function Hero() {
  const { t } = useTranslation();

  return (
    <section className="hero" id="home">
      <div className="hero-container">
        {/* Left Column */}
        <div className="hero-left">
          <div className="ai-badge">
            <Sparkles size={14} className="badge-icon" />
            <span>AI-POWERED BREED PREDICTION</span>
          </div>

          <h1 className="hero-headline">
            Identify Cattle &amp; Buffalo <br className="hero-br" />
            Breeds with AI
          </h1>

          <p className="hero-description">
            {t("hero.description") ||
              "Upload a clear photograph of your cattle or buffalo and let our deep learning model analyze physical traits to identify the breed with high precision."}
          </p>

          <div className="hero-actions">
            <a className="hero-primary-btn" href="#predict">
              <ScanLine size={18} />
              <span>Identify a Breed</span>
            </a>
            <a className="hero-secondary-btn" href="#how-it-works">
              <span>How it works</span>
              <ArrowRight size={16} />
            </a>
          </div>

          <div className="hero-trust-bar">
            <div className="trust-item">
              <CheckCircle2 size={16} className="trust-icon" />
              <span>95%+ Classification Accuracy</span>
            </div>
            <div className="trust-divider" aria-hidden="true" />
            <div className="trust-item">
              <ShieldCheck size={16} className="trust-icon" />
              <span>40+ Breeds Supported</span>
            </div>
          </div>
        </div>

        {/* Right Column Visual Showcase */}
        <div className="hero-right">
          <div className="hero-image-frame">
            <img
              src={heroShowcase}
              alt="Indian Gir cow breed showcase"
              className="hero-image"
            />

            {/* Floating AI Prediction Widget */}
            <div className="floating-card">
              <div className="floating-card-header">
                <span className="card-label">AI PREDICTION</span>
                <span className="live-dot" />
              </div>
              <div className="floating-card-body">
                <strong className="breed-title">Gir Cow</strong>
                <div className="confidence-chip">
                  <span>Confidence 98.4%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
