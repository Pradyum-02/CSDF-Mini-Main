import React from 'react';

const MetadataPanel = ({ metadata }) => {
  if (!metadata || Object.keys(metadata).length === 0) {
    return (
      <div className="metadata-panel">
        <h4>Metadata Information</h4>
        <p>No metadata available</p>
      </div>
    );
  }

  return (
    <div className="metadata-panel">
      <h4>Metadata Information</h4>
      <div className="metadata-content">
        {Object.entries(metadata).map(([key, value], index) => (
          <div key={index} className="metadata-item">
            <span className="metadata-label">{key}:</span>
            <span className="metadata-value">{value || 'Not Available'}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MetadataPanel;