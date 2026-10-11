import React from 'react';

const AnalysisSummary = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="analysis-results">
        <h3>Analysis Summary</h3>
        <div className="empty-state">
          <h3>No Analysis Available</h3>
          <p>Upload an image to see forensic analysis results here.</p>
        </div>
      </div>
    );
  }

  const { filename, file_size, format, width, height, mode, metadata, hashes, ela_available, notes } = analysisData;

  return (
    <div className="analysis-results">
      <h3>Analysis Summary</h3>
      <div className="results-grid">
        <div className="result-card">
          <h4>File Information</h4>
          <p><strong>Filename:</strong> {filename}</p>
          <p><strong>Size:</strong> {file_size} bytes ({(file_size / 1024).toFixed(2)} KB)</p>
          <p><strong>Format:</strong> {format}</p>
          <p><strong>Dimensions:</strong> {width} × {height} pixels</p>
          <p><strong>Aspect Ratio:</strong> {(width / height).toFixed(2)}</p>
          <p><strong>Color Mode:</strong> {mode}</p>
        </div>

        <div className="result-card">
          <h4>Metadata Status</h4>
          {metadata && Object.keys(metadata).length > 0 ? (
            <>
              <p><strong>Available:</strong> Yes</p>
              <p><strong>EXIF Data:</strong> {Object.keys(metadata).length} fields found</p>
              {metadata['Camera Make'] && (
                <p><strong>Camera:</strong> {metadata['Camera Make']} {metadata['Camera Model'] || ''}</p>
              )}
              {metadata['DateTime Original'] && (
                <p><strong>Date Taken:</strong> {metadata['DateTime Original']}</p>
              )}
              {metadata['GPS Coordinates'] && (
                <p><strong>GPS:</strong> {metadata['GPS Coordinates']}</p>
              )}
            </>
          ) : (
            <p><strong>Available:</strong> No EXIF metadata found</p>
          )}
        </div>

        <div className="result-card">
          <h4>Hash Values</h4>
          <p><strong>MD5:</strong> {hashes?.md5 || 'N/A'}</p>
          <p><strong>SHA-1:</strong> {hashes?.sha1 || 'N/A'}</p>
          <p><strong>SHA-256:</strong> {hashes?.sha256 || 'N/A'}</p>
        </div>

        <div className="result-card">
          <h4>ELA Analysis</h4>
          <p><strong>Available:</strong> {ela_available ? 'Yes' : 'No'}</p>
          {!ela_available && (
            <p>ELA analysis is only available for JPEG images.</p>
          )}
        </div>
      </div>

      {notes && (
        <div className="mt-4">
          <h4>Analysis Notes</h4>
          <p>{notes}</p>
        </div>
      )}
    </div>
  );
};

export default AnalysisSummary;