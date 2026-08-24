import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  Upload,
  Sparkles,
  ArrowRight
} from "lucide-react";

import heroImage from "../assets/Hero.JPG";
import { predictBreed } from "../services/predictionApi";

import "./Hero.css";

function Hero() {
  const { t } = useTranslation();

  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    return () => {
      if (image) {
        URL.revokeObjectURL(image);
      }
    };
  }, [image]);

  const handleUpload = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedTypes = [
      "image/jpeg",
      "image/jpg",
      "image/png"
    ];

    if (!allowedTypes.includes(file.type)) {
      alert(t("hero.errorType"));
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert(t("hero.errorSize"));
      return;
    }

    // Clear previous state
    setPrediction(null);
    setError(null);

    // Store the actual File object
    setSelectedFile(file);

    // Store preview URL
    setImage(URL.createObjectURL(file));
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setPrediction(null);

      const result = await predictBreed(selectedFile);

      console.log("Prediction response:", result);

      setPrediction(result);

    } catch (error) {
      console.error("Prediction failed:", error);

      setError(
        error.message || "Prediction failed."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      className="hero"
      id="home"
      style={{
        backgroundImage: `url(${heroImage})`
      }}
    >

      <div className="hero-overlay"></div>

      <div className="hero-content">

        <div className="ai-badge">
          <Sparkles size={16} />
        </div>

        <h1>
          {t("hero.title")}
        </h1>

        <h2>
          {t("hero.subtitle")}
        </h2>

        <p>
          {t("hero.description")}
        </p>

        <div className="hero-buttons">

          <label className="upload-button">

            <Upload size={18} />

            {t("hero.uploadBtn")}

            <input
              type="file"
              accept=".jpg,.jpeg,.png"
              onChange={handleUpload}
              hidden
            />

          </label>

          <button className="explore-button">
            {t("hero.exploreBtn")}
            <ArrowRight size={17} />
          </button>

        </div>

        {image && (

          <div className="image-preview">

            <img
              src={image}
              alt={t("hero.selected")}
            />

            <div>

              <strong>
                {t("hero.selected")}
              </strong>

              <span>
                {loading
                  ? "Analyzing image..."
                  : t("hero.ready")}
              </span>

              <button
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : t("hero.analyzeBtn")}
              </button>

            </div>

          </div>

        )}

        {error && (

          <div className="prediction-error">
            {error}
          </div>

        )}

        {prediction && (

          <div className="prediction-result">

            <h3>
              Prediction Result
            </h3>

            <p>
              <strong>
                Breed:
              </strong>{" "}
              {prediction.predicted_breed || "Pending"}
            </p>

            {prediction.confidence !== null &&
              prediction.confidence !== undefined && (
                <p>
                  <strong>
                    Confidence:
                  </strong>{" "}
                  {Number(prediction.confidence).toFixed(2)}%
                </p>
              )}

            <p>
              <strong>
                Status:
              </strong>{" "}
              {prediction.status}
            </p>

            {prediction.message && (
              <p>
                {prediction.message}
              </p>
            )}

          </div>

        )}

      </div>

    </section>
  );
}

export default Hero;