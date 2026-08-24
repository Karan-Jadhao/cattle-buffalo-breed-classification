import { useTranslation } from "react-i18next";
import {
  UploadCloud,
  Cpu,
  Search,
  FileText,
  ArrowRight
} from "lucide-react";

import "./HowItWorks.css";

function HowItWorks() {
  const { t } = useTranslation();

  const steps = [
    {
      icon: UploadCloud,
      title: t("howItWorks.step1Title"),
      description: t("howItWorks.step1Desc")
    },
    {
      icon: Cpu,
      title: t("howItWorks.step2Title"),
      description: t("howItWorks.step2Desc")
    },
    {
      icon: Search,
      title: t("howItWorks.step3Title"),
      description: t("howItWorks.step3Desc")
    },
    {
      icon: FileText,
      title: t("howItWorks.step4Title"),
      description: t("howItWorks.step4Desc")
    }
  ];

  return (
    <section className="how-it-works" id="how-it-works">

      <div className="section-label">
        <span></span>
        {t("howItWorks.label")}
      </div>

      <h2>
        {t("howItWorks.title")}
      </h2>

      <div className="steps">

        {steps.map((step, index) => {

          const Icon = step.icon;

          return (
            <div className="step-wrapper" key={step.title}>

              <div className="step">

                <div className="step-icon">
                  <Icon size={27} />
                </div>

                <h3>{step.title}</h3>

                <p>{step.description}</p>

              </div>

              {index !== steps.length - 1 && (
                <ArrowRight
                  className="step-arrow"
                  size={24}
                />
              )}

            </div>
          );
        })}

      </div>

    </section>
  );
}

export default HowItWorks;