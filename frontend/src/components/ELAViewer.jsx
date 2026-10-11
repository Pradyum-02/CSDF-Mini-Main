import React from 'react';

const ELAViewer = ({ elaAvailable, elaResult }) => {
  if (!elaAvailable) {
    return (
      <div className="ela-info">
        <h4>ELA Analysis</h4>
        <p>Error Level Analysis is only available for JPEG images.</p>
        <p><em>This image format does not support ELA analysis.</em></p>
      </div>
    );
  }

  if (!elaResult) {
    return (
      <div className="ela-info">
        <h4>ELA Analysis</h4>
        <p>ELA analysis not performed or failed.</p>
      </div>
    );
  }

  return (
    <div>
      <h4>Error Level Analysis (ELA)</h4>
      <img
        src={`data:image/png;base64,${elaResult}`}
        alt="ELA Result"
        style={{ maxWidth: '100%', borderRadius: '6px' }}
      />
      <p className="mt-2" style={{ fontSize: '0.875rem', color: '#64748b' }}>
        <em>ELA highlights differences in JPEG recompression patterns. Bright regions are not proof of tampering. Results require expert interpretation.</em>
      </p>
    </div>
  );
};

export default ELAViewer;