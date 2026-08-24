import React from "react";
import { useTranslation } from "react-i18next";
import "./About.css";
import aboutImage from "../assets/about.jpg";

const About = () => {
  const { t } = useTranslation();

  return (
    <section id="about" className="about-section">
      <div className="about-container">

        {/* Left Content */}
        <div className="about-content">

          <div className="about-label">
            <span className="about-line"></span>
            <span>{t("about.label")}</span>
          </div>

          <h2>
            {t("about.title")}
          </h2>

          <p>
            {t("about.p1")}
          </p>

          <p>
            {t("about.p2")}
          </p>

        </div>

        {/* Right Image */}
        <div className="about-image-wrapper">
          <img
            src={aboutImage}
            alt="Cattle and buffalo"
            className="about-image"
          />
        </div>

      </div>
    </section>
  );
};

export default About;