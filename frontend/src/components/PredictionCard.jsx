import { useTranslation } from "react-i18next";
import {
  MapPin,
  Info,
  ArrowRight,
  CircleDot,
  GlassWater
} from "lucide-react";

import girCow from "../assets/Gircow.png";

import "./PredictionCard.css";

function PredictionCard() {
  const { t } = useTranslation();

  return (
    <div
      className="prediction-card"
      style={{
        backgroundImage: `url(${girCow})`
      }}
    >
      <div className="prediction-overlay"></div>

      <div className="prediction-content">

        <p className="prediction-label">
          {t("predictionCard.label")}
        </p>

        <div className="prediction-heading">
          <h2>{t("predictionCard.girCow")}</h2>

          <span>
            92.4% {t("predictionCard.confidence")}
          </span>
        </div>

        <div className="breed-details">

          <Detail
            icon={CircleDot}
            label={t("predictionCard.species")}
            value={t("predictionCard.cattle")}
          />

          <Detail
            icon={MapPin}
            label={t("predictionCard.origin")}
            value={t("predictionCard.indiaGujarat")}
          />

          <Detail
            icon={GlassWater}
            label={t("predictionCard.purpose")}
            value={t("predictionCard.milk")}
          />

          <Detail
            icon={Info}
            label={t("predictionCard.characteristics")}
            value={t("predictionCard.girCharacteristics")}
          />

        </div>

        <button className="details-button">
          {t("predictionCard.viewDetails")}
          <ArrowRight size={15} />
        </button>

      </div>
    </div>
  );
}

function Detail({ icon: Icon, label, value }) {
  return (
    <div className="detail">

      <Icon size={14} />

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}

export default PredictionCard;