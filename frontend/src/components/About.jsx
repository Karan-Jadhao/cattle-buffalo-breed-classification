import { useTranslation } from "react-i18next";
import { CheckCircle, Cpu, Layers } from "lucide-react";
import aboutImage from "../assets/about.jpg";
import "./About.css";

const About = () => {
  const { t } = useTranslation();

  return (
    <section id="about" className="about-section">
      <div className="about-container">
        {/* Left Content */}
        <div className="about-content">
          <div className="about-label">
            <span className="about-line" />
            <span>{t("about.label")}</span>
          </div>

          <h2>{t("about.title")}</h2>

          <p>{t("about.p1")}</p>

          <p>{t("about.p2")}</p>

          <div className="about-highlights">
            <div className="highlight-item">
              <Cpu size={18} className="highlight-icon" />
              <span>Deep Convolutional AI</span>
            </div>
            <div className="highlight-item">
              <Layers size={18} className="highlight-icon" />
              <span>Multi-Breed Recognition</span>
            </div>
            <div className="highlight-item">
              <CheckCircle size={18} className="highlight-icon" />
              <span>Field-Ready Precision</span>
            </div>
          </div>
        </div>

        {/* Right Image */}
        <div className="about-image-wrapper">
          <img
            src={aboutImage}
            alt="Cattle and buffalo breed intelligence"
            className="about-image"
          />
          <div className="about-image-badge">
            <strong>BreedVision AI</strong>
            <span>Agricultural Intelligence</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
