import React, { useState } from 'react';

const ImageUploader = ({ onImageProcessed }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.target.closest('.upload-section')?.classList.add('dragover');
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.target.closest('.upload-section')?.classList.remove('dragover');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.target.closest('.upload-section')?.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleFileSelect = (file) => {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/tiff', 'image/bmp', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a valid image file (JPEG, PNG, TIFF, BMP, or WebP)');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
    setError(null);

    // Create preview URL
    const previewUrl = URL.createObjectURL(file);
    setPreviewUrl(previewUrl);

    // Process the image
    processImage(file);
  };

  const processImage = async (file) => {
    setIsProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const result = await response.json();
      onImageProcessed(result, file);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    // Reset analysis results by calling onImageProcessed with null
    onImageProcessed(null);
  };

  if (isProcessing) {
    return (
      <div className="upload-section">
        <h3>Analyzing Image...</h3>
        <p>Please wait while we process your image.</p>
        <div className="loading-spinner" />
      </div>
    );
  }

  return (
    <div className="upload-section"
         onDragOver={handleDragOver}
         onDragLeave={handleDragLeave}
         onDrop={handleDrop}>
      {!selectedFile ? (
        <>
          <h3>Upload Image for Analysis</h3>
          <p>Drag & drop an image here, or click to select</p>
          <input
            type="file"
            accept="image/jpeg,image/png,image/tiff,image/bmp,image/webp"
            onChange={(e) => {
              if (e.target.files[0]) {
                handleFileSelect(e.target.files[0]);
              }
            }}
            className="hidden"
          />
          <button
            type="button"
            onClick={() => document.querySelector('input[type="file"]').click()}
            disabled={isProcessing}
          >
            Choose File
          </button>
        </>
      ) : (
        <>
          <div className="file-info">
            <h4>Selected File</h4>
            <p><strong>Name:</strong> {selectedFile.name}</p>
            <p><strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
            <p><strong>Type:</strong> {selectedFile.type}</p>
          </div>

          {previewUrl && (
            <div className="mt-4">
              <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', borderRadius: '6px' }} />
            </div>
          )}

          <div className="mt-4">
            <button
              type="button"
              onClick={handleRemoveFile}
              className="report-button"
              style={{ backgroundColor: '#ef4444' }}
            >
              Remove Image
            </button>

            {!isProcessing && (
              <button
                type="button"
                onClick={() => {
                  const fileInput = document.createElement('input');
                  fileInput.type = 'file';
                  fileInput.accept = 'image/jpeg,image/png,image/tiff,image/bmp,image/webp';
                  fileInput.onchange = (e) => {
                    if (e.target.files[0]) {
                      handleFileSelect(e.target.files[0]);
                    }
                  };
                  fileInput.click();
                }}
                disabled={isProcessing}
              >
                Change Image
              </button>
            )}
          </div>

          {error && (
            <div className="error mt-4">
              <strong>Error:</strong> {error}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ImageUploader;