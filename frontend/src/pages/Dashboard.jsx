import React, { useState } from 'react';
import ImageUploader from '../components/ImageUploader';
import ImagePreview from '../components/ImagePreview';
import MetadataPanel from '../components/MetadataPanel';
import HashPanel from '../components/HashPanel';
import ELAViewer from '../components/ELAViewer';
import AnalysisSummary from '../components/AnalysisSummary';
import ReportActions from '../components/ReportActions';

const Dashboard = () => {
  const [analysisData, setAnalysisData] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [elaData, setElaData] = useState(null);

  const handleImageProcessed = (data, file) => {
    if (data === null) {
      // Clear all data when image is removed
      setAnalysisData(null);
      setImagePreview(null);
      setElaData(null);
      return;
    }

    setAnalysisData(data);

    // Create preview for display
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }

    // Store ELA data if available
    if (data.ela_result) {
      setElaData(data.ela_result);
    } else {
      setElaData(null);
    }
  };

  return (
    <div className="dashboard">
      <ImageUploader onImageProcessed={handleImageProcessed} />

      {imagePreview && (
        <div className="mt-6">
          <h3>Image Preview</h3>
          <img src={imagePreview} alt="Selected" style={{ maxWidth: '100%', borderRadius: '6px' }} />
        </div>
      )}

      <AnalysisSummary analysisData={analysisData} />

      {analysisData && (
        <>
          <div className="mt-6">
            <ImagePreview
              imageData={{
                data: '',  // We'll use the preview for display
                format: analysisData.format
              }}
              elaData={elaData}
            />
          </div>

          <div className="mt-6">
            <MetadataPanel metadata={analysisData.metadata} />
          </div>

          <div className="mt-6">
            <HashPanel hashes={analysisData.hashes} />
          </div>

          <div className="mt-6">
            <ELAViewer
              elaAvailable={analysisData.ela_available}
              elaResult={elaData}
            />
          </div>

          <div className="mt-6">
            <ReportActions analysisData={analysisData} />
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;