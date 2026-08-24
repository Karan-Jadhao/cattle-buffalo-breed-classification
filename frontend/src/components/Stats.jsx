import { useTranslation } from "react-i18next";
import {
  Beef,
  Target,
  Database,
  ShieldCheck
} from "lucide-react";

import "./Stats.css";

function Stats() {
  const { t } = useTranslation();

  const stats = [
    {
      icon: Beef,
      number: "25+",
      title: t("stats.cattleTitle"),
      subtitle: t("stats.supported")
    },
    {
      icon: Beef,
      number: "15+",
      title: t("stats.buffaloTitle"),
      subtitle: t("stats.supported")
    },
    {
      icon: Target,
      number: "95%+",
      title: t("stats.accuracy"),
      subtitle: t("stats.prediction")
    },
    {
      icon: Database,
      number: "10K+",
      title: t("stats.images"),
      subtitle: t("stats.trained")
    },
    {
      icon: ShieldCheck,
      number: "100%",
      title: t("stats.secure"),
      subtitle: t("stats.predictions")
    }
  ];

  return (
    <section className="stats">

      {stats.map((stat, index) => {

        const Icon = stat.icon;

        return (
          <div className="stat-item" key={index}>

            <div className="stat-icon">
              <Icon size={27} />
            </div>

            <div>
              <strong>{stat.number}</strong>

              <p>{stat.title}</p>

              <small>{stat.subtitle}</small>
            </div>

          </div>
        );
      })}

    </section>
  );
}

export default Stats;