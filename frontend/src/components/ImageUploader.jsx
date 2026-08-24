import { useRef, useState } from "react";
import { ImagePlus, Upload, X } from "lucide-react";

import "./ImageUploader.css";

const ACCEPTED_TYPES = new Set(["image/jpeg", "image/png"]);
const MAX_FILE_SIZE = 5 * 1024 * 1024;

function ImageUploader({ file, previewUrl, disabled, onFileChange, onError, onRemove }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const chooseFile = (candidate) => {
    if (!candidate) return;
    if (!ACCEPTED_TYPES.has(candidate.type)) {
      onError("Please choose a JPEG or PNG image.");
      return;
    }
    if (candidate.size > MAX_FILE_SIZE) {
      onError("Please choose an image smaller than 5 MB.");
      return;
    }
    onFileChange(candidate);
  };

  const onDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    if (!disabled) chooseFile(event.dataTransfer.files?.[0]);
  };

  if (file && previewUrl) {
    return (
      <div className="selected-image">
        <img src={previewUrl} alt={`Preview of ${file.name}`} />
        <div className="selected-image__details">
          <span className="selected-image__eyebrow">Ready for AI Analysis</span>
          <strong>{file.name}</strong>
          <span>{Math.ceil(file.size / 1024)} KB · JPEG / PNG</span>
        </div>
        <button
          className="icon-button"
          type="button"
          onClick={onRemove}
          disabled={disabled}
          aria-label="Remove selected image"
        >
          <X size={18} />
        </button>
      </div>
    );
  }

  return (
    <div
      className={`image-uploader ${isDragging ? "is-dragging" : ""}`}
      onDragEnter={(event) => {
        event.preventDefault();
        if (!disabled) setIsDragging(true);
      }}
      onDragOver={(event) => event.preventDefault()}
      onDragLeave={() => setIsDragging(false)}
      onDrop={onDrop}
      onClick={() => inputRef.current?.click()}
    >
      <div className="image-uploader-icon">
        <ImagePlus size={24} aria-hidden="true" />
      </div>
      <div>
        <strong>Drop an animal photo here</strong>
        <p>or click to browse from your device</p>
      </div>
      <button
        className="uploader-choose-btn"
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          inputRef.current?.click();
        }}
        disabled={disabled}
      >
        <Upload size={15} />
        <span>Choose Image</span>
      </button>
      <input
        ref={inputRef}
        className="visually-hidden"
        type="file"
        accept="image/jpeg,image/png"
        disabled={disabled}
        onChange={(event) => chooseFile(event.target.files?.[0])}
      />
      <span className="image-uploader__hint">Supports JPG, JPEG or PNG · Max file size 5MB</span>
    </div>
  );
}

export default ImageUploader;

