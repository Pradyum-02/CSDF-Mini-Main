import React from 'react';

const ImagePreview = ({ imageData, elaData }) => {
  return (
    <div className="ela-container">
      <div className="ela-image-container">
        <h4>Original Image</h4>
        {imageData ? (
          <img src={`data:image/${imageData.format.toLowerCase()};base64,${imageData.data}`} alt="Original" />
        ) : (
          <div>No image available</div>
        )}
      </div>

      <div className="ela-image-container">
        <h4>ELA Analysis</h4>
        {elaData ? (
          <img src={`data:image/png;base64,${elaData}`} alt="ELA Result" />
        ) : (
          <div>ELA not available for this image format</div>
        )}
      </div>
    </div>
  );
};

export default ImagePreview;