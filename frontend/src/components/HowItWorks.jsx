import { useTranslation } from "react-i18next";
import { UploadCloud, Cpu, Search, FileText, ChevronRight } from "lucide-react";

import "./HowItWorks.css";

function HowItWorks() {
  const { t } = useTranslation();

  const steps = [
    {
      num: "01",
      icon: UploadCloud,
      title: t("howItWorks.step1Title"),
      description: t("howItWorks.step1Desc")
    },
    {
      num: "02",
      icon: Cpu,
      title: t("howItWorks.step2Title"),
      description: t("howItWorks.step2Desc")
    },
    {
      num: "03",
      icon: Search,
      title: t("howItWorks.step3Title"),
      description: t("howItWorks.step3Desc")
    },
    {
      num: "04",
      icon: FileText,
      title: t("howItWorks.step4Title"),
      description: t("howItWorks.step4Desc")
    }
  ];

  return (
    <section className="how-it-works" id="how-it-works">
      <div className="section-label">
        <span className="section-line" />
        <span>{t("howItWorks.label")}</span>
      </div>

      <h2>{t("howItWorks.title")}</h2>

      <div className="steps-grid">
        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <div className="step-card-wrapper" key={step.num}>
              <div className="step-card">
                <div className="step-card-header">
                  <div className="step-icon">
                    <Icon size={24} />
                  </div>
                  <span className="step-number">{step.num}</span>
                </div>

                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </div>

              {index !== steps.length - 1 && (
                <div className="step-connector" aria-hidden="true">
                  <ChevronRight size={20} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default HowItWorks;