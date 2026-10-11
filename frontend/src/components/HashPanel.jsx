import React from 'react';

const HashPanel = ({ hashes }) => {
  if (!hashes) {
    return (
      <div className="hash-panel">
        <h4>Cryptographic Hashes</h4>
        <p>Hashes not calculated</p>
      </div>
    );
  }

  return (
    <div className="hash-panel">
      <h4>Cryptographic Hashes</h4>
      <div className="hash-content">
        <div className="hash-item">
          <span className="hash-label">MD5:</span>
          <span className="hash-value">{hashes.md5 || 'N/A'}</span>
          <button
            className="copy-button"
            onClick={() => navigator.clipboard.writeText(hashes.md5 || '')}
            disabled={!hashes.md5}
          >
            Copy
          </button>
        </div>
        <div className="hash-item">
          <span className="hash-label">SHA-1:</span>
          <span className="hash-value">{hashes.sha1 || 'N/A'}</span>
          <button
            className="copy-button"
            onClick={() => navigator.clipboard.writeText(hashes.sha1 || '')}
            disabled={!hashes.sha1}
          >
            Copy
          </button>
        </div>
        <div className="hash-item">
          <span className="hash-label">SHA-256:</span>
          <span className="hash-value">{hashes.sha256 || 'N/A'}</span>
          <button
            className="copy-button"
            onClick={() => navigator.clipboard.writeText(hashes.sha256 || '')}
            disabled={!hashes.sha256}
          >
            Copy
          </button>
        </div>
      </div>
    </div>
  );
};

export default HashPanel;