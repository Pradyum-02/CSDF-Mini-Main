import React from 'react';

const ReportActions = ({ analysisData }) => {
  if (!analysisData) {
    return (
      <div className="report-actions">
        <h4>Generate Report</h4>
        <p>No analysis data available for report generation.</p>
      </div>
    );
  }

  const handleDownloadReport = async (format) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...analysisData,
          format
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate report');
      }

      if (format === 'json') {
        const data = await response.json();
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `csdf_report_${analysisData.analysis_id || 'unknown'}.json`;
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        const text = await response.text();
        const blob = new Blob([text], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `csdf_report_${analysisData.analysis_id || 'unknown'}.txt`;
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      alert('Failed to generate report: ' + error.message);
    }
  };

  return (
    <div className="report-actions">
      <h4>Generate Report</h4>
      <div>
        <button
          className="report-button"
          onClick={() => handleDownloadReport('txt')}
        >
          Download TXT Report
        </button>
        <button
          className="report-button"
          onClick={() => handleDownloadReport('json')}
        >
          Download JSON Report
        </button>
      </div>
    </div>
  );
};

export default ReportActions;