# CSDF - Digital Image Forensics and Analysis Tool

A comprehensive web application for digital image forensics analysis, built as a college project for Savitribai Phule Pune University (Subject Code: 410244).

## Features

- **Image Upload & Validation**: Secure drag-and-drop interface with file type and size validation
- **Metadata Extraction**: Extract EXIF data including camera info, GPS coordinates, timestamps, and technical details
- **Cryptographic Hashing**: Calculate MD5, SHA-1, and SHA-256 hashes of original image data
- **Error Level Analysis (ELA)**: Detect compression inconsistencies in JPEG images
- **Comprehensive Analysis**: File information, format detection, dimensions, and color mode analysis
- **Report Generation**: Downloadable TXT and JSON reports with all analysis results
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

### Frontend
- React 18 + Vite
- Plain CSS (no frameworks)
- Modern JavaScript (ES6+)

### Backend
- Python 3.x + Flask
- Pillow for image processing
- NumPy for numerical computations
- piexif for EXIF data extraction
- Gunicorn for production WSGI serving

## Project Structure

```
CSDF-Mini-Main/
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── ImagePreview.jsx
│   │   │   ├── MetadataPanel.jsx
│   │   │   ├── HashPanel.jsx
│   │   │   ├── ELAViewer.jsx
│   │   │   ├── AnalysisSummary.jsx
│   │   │   └── ReportActions.jsx
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── global.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   └── vercel.json
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forensic.py
│   │   ├── metadata.py
│   │   ├── hashing.py
│   │   ├── ela.py
│   │   └── reports.py
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_hashing.py
│   │   ├── test_metadata.py
│   │   └── test_analysis.py
│   ├── requirements.txt
│   ├── .env.example
│   └── wsgi.py
├── docs/
│   ├── USER_GUIDE.md
│   └── TECHNICAL_DOCUMENTATION.md
├── .gitignore
├── README.md
├── render.yaml
└── LICENSE
```

## Local Setup & Installation

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm 6+

### Backend Setup
```powershell
# Clone the repository
git clone https://github.com/Pradyum-02/CSDF-Mini-Main.git
cd CSDF-Mini-Main/backend

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
copy .env.example .env
# Edit .env to configure FRONTEND_ORIGIN if needed

# Run tests
python -m pytest tests/ -v

# Start development server
python wsgi.py
```

### Frontend Setup
```powershell
# In a separate terminal
cd frontend

# Install dependencies
npm install

# Set environment variables
copy .env.example .env
# Edit .env to configure VITE_API_BASE_URL if needed

# Start development server
npm run dev
```

### Production Build
```powershell
# Frontend
cd frontend
npm run build

# Backend (for production deployment)
# Uses Gunicorn as specified in render.yaml
```

## Environment Variables

### Backend (.env)
```
FRONTEND_ORIGIN=http://localhost:5173
FLASK_ENV=production
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:5000/api
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns service health status.

### Image Analysis
```
POST /api/analyze
```
Form-data: `image` (file)
Returns: JSON with analysis results including metadata, hashes, and ELA data.

### Report Generation
```
POST /api/report
```
Body: JSON with analysis data and format ('txt' or 'json')
Returns: Report file for download.

## Forensic Features Explained

### Metadata Extraction
Extracts embedded EXIF data from images including:
- Camera manufacturer and model
- Date and time of capture
- GPS coordinates (if available)
- Camera settings (aperture, shutter speed, ISO, focal length)
- Software used for processing

### Cryptographic Hashing
Calculates industry-standard cryptographic hashes from the exact original image bytes:
- **MD5**: 128-bit hash value
- **SHA-1**: 160-bit hash value  
- **SHA-256**: 256-bit hash value (recommended for security applications)

### Error Level Analysis (ELA)
Identifies compression inconsistencies in JPEG images by:
1. Saving the original image at a specified quality level (90%)
2. Comparing pixel differences between original and resaved image
3. Amplifying differences for visibility
4. **Important**: Bright areas indicate different compression levels, NOT definitive proof of tampering

## Limitations & Disclaimer

⚠️ **Forensic Limitations**: This tool is intended for educational purposes only. Results should be interpreted by qualified digital forensics experts.

- ELA analysis is only reliable for JPEG images
- Metadata absence does not indicate image manipulation
- Hash values verify file integrity, not authenticity
- No AI or machine learning components are used for automated verdicts
- Chain of custody features are not implemented in this version
- Tool should not be used as sole evidence in legal proceedings

## Deployment Instructions

### Frontend (Vercel)
1. Push code to GitHub repository
2. Import project in Vercel
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_BASE_URL` (your backend URL)
6. Deploy

### Backend (Render)
1. Push code to GitHub repository
2. Create new Web Service on Render
3. Connect to your repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn wsgi:app`
6. Add environment variable: `FRONTEND_ORIGIN` (your frontend URL)
7. Set health check path: `/api/health`
8. Deploy

## Academic Context

**Project**: CSDF — Digital Image Forensics and Analysis Tool  
**Subject**: Cyber Security and Digital Forensics  
**Subject Code**: 410244  
**University**: Savitribai Phule Pune University  
**Type**: Computer Engineering Mini-Project  

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with modern web technologies following security best practices
- Designed for educational demonstration of digital forensics concepts
- Respects privacy and does not store or transmit uploaded images externally