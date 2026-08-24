import { useEffect, useState } from "react";
import { AlertCircle, ArrowRight, CheckCircle2, LoaderCircle, ScanLine, Sparkles } from "lucide-react";

import ImageUploader from "./ImageUploader";
import { predictBreed } from "../services/predictionApi";
import "./PredictionCard.css";

function confidenceLabel(confidence) {
  return `${(confidence * 100).toFixed(1)}%`;
}

function PredictionCard() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  const handleFileChange = (selectedFile) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
    setError("");
  };

  const removeImage = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(null);
    setPreviewUrl("");
    setResult(null);
    setError("");
  };

  const requestPrediction = async () => {
    if (!file) {
      setError("Please select a cattle or buffalo photograph before starting analysis.");
      return;
    }

    setIsLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await predictBreed(file));
    } catch (requestError) {
      setError(requestError.message || "Unable to analyze the image right now. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="prediction-workspace" id="predict" aria-labelledby="predict-heading">
      <div className="prediction-workspace__intro">
        <div className="section-badge">
          <ScanLine size={15} />
          <span>AI BREED ANALYSIS ENGINE</span>
        </div>
        <h2 id="predict-heading">Upload a photo. Get a instant breed prediction.</h2>
        <p>Our deep learning vision model detects distinct anatomical features of indigenous and exotic cattle and buffalo breeds.</p>
      </div>

      <div className="prediction-layout">
        {/* Upload Panel */}
        <div className="upload-panel">
          <div className="panel-heading">
            <span className="panel-number">01</span>
            <div>
              <h3>Choose an image</h3>
              <p>Your uploaded photo is processed privately for this analysis.</p>
            </div>
          </div>
          <ImageUploader
            file={file}
            previewUrl={previewUrl}
            disabled={isLoading}
            onFileChange={handleFileChange}
            onError={setError}
            onRemove={removeImage}
          />
          <button
            className="prediction-submit-btn"
            type="button"
            onClick={requestPrediction}
            disabled={isLoading || !file}
          >
            {isLoading ? (
              <>
                <LoaderCircle className="spin" size={18} />
                <span>Analyzing image features…</span>
              </>
            ) : (
              <>
                <span>Analyze Breed Now</span>
                <ArrowRight size={18} />
              </>
            )}
          </button>
          {error && (
            <p className="inline-error" role="alert">
              <AlertCircle size={17} />
              <span>{error}</span>
            </p>
          )}
        </div>

        {/* Results Panel */}
        <div className="result-panel" aria-live="polite">
          {isLoading && <LoadingState />}
          {!isLoading && !result && <EmptyResult />}
          {result && <PredictionResult result={result} />}
        </div>
      </div>
    </section>
  );
}

function LoadingState() {
  return (
    <div className="analysis-state">
      <div className="spinner-wrapper">
        <LoaderCircle className="spin" size={32} />
      </div>
      <h3>Analyzing livestock traits…</h3>
      <p>Running neural network feature extraction and matching top breed probabilities.</p>
      <div className="analysis-progress-bar">
        <span />
      </div>
    </div>
  );
}

function EmptyResult() {
  return (
    <div className="empty-result">
      <div className="empty-icon-circle">
        <ScanLine size={32} />
      </div>
      <h3>Your Prediction Dashboard</h3>
      <p>Upload a clear photo on the left and click "Analyze Breed Now" to inspect top breed predictions and confidence scores.</p>
    </div>
  );
}

function PredictionResult({ result }) {
  const { prediction, top_5: topPredictions } = result;
  const confidence = Math.round(prediction.confidence * 100);

  return (
    <div className="prediction-result-card">
      <div className="result-header">
        <span className="result-eyebrow">
          <CheckCircle2 size={15} />
          <span>PRIMARY BREED IDENTIFIED</span>
        </span>
        <span className="confidence-pill">{confidenceLabel(prediction.confidence)} Confidence</span>
      </div>

      <div className="result-summary">
        <div>
          <h3>{prediction.breed}</h3>
          <p>Highest probability breed match based on model features</p>
        </div>
      </div>

      <div className="confidence-meter-track" aria-label={`${confidence}% confidence`}>
        <span className="confidence-meter-bar" style={{ width: `${confidence}%` }} />
      </div>

      <div className="top-predictions-header">
        <h4>Top 5 Probability Ranking</h4>
      </div>

      <ol className="top-predictions">
        {topPredictions.map((item, index) => {
          const percentage = Math.max(0, Math.min(100, item.confidence * 100));
          return (
            <li key={item.class_index || index}>
              <span className="rank-badge">{index + 1}</span>
              <div className="top-predictions__breed">
                <div className="breed-name-row">
                  <span className="breed-name-text">{item.breed}</span>
                  <strong className="breed-percent">{confidenceLabel(item.confidence)}</strong>
                </div>
                <div className="bar-track">
                  <i style={{ width: `${percentage}%` }} />
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </div>
  );
}

export default PredictionCard;

