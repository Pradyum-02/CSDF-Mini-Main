# CSDF Technical Documentation

## System Architecture

CSDF follows a traditional client-server architecture with a React/Vite frontend and Python/Flask backend.

### Frontend Architecture
- **Framework**: React 18 with Vite build tool
- **State Management**: React hooks (useState, useEffect)
- **Component Structure**: Functional components with props drilling
- **Styling**: Custom CSS with responsive design principles
- **HTTP Communication**: Fetch API with async/await

### Backend Architecture
- **Framework**: Flask 2.3.3
- **Pattern**: Modular application with blueprint routing
- **Image Processing**: Pillow (PIL fork) with NumPy arrays
- **EXIF Handling**: piexif library
- **WSGI Server**: Gunicorn for production deployment

## Component Details

### Frontend Components

#### ImageUploader.jsx
Handles file selection, validation, and upload initiation:
- Drag-and-drop API with visual feedback
- File type validation (MIME type checking)
- File size validation (10MB limit)
- Preview generation using FileReader API
- FormData construction for multipart upload
- Loading states and error handling

#### ImagePreview.jsx
Displays original image and ELA result side-by-side:
- Conditional rendering based on data availability
- Base64 image embedding for display
- Responsive layout using CSS flexbox

#### MetadataPanel.jsx
Renders extracted metadata in key-value format:
- Dynamic rendering based on available metadata
- Handling of missing or null values
- Clean presentation of technical EXIF data

#### HashPanel.jsx
Displays cryptographic hashes with copy-to-clipboard functionality:
- MD5, SHA-1, SHA-256 display
- Clipboard API integration for copying values
- Visual feedback on copy success
- Disabled states when hashes unavailable

#### ELAViewer.jsx
Presents Error Level Analysis results:
- Format-specific visibility (JPEG only)
- Informational disclaimer about ELA limitations
- Responsive image display with proper sizing

#### AnalysisSummary.jsx
Consolidates key findings in card-based layout:
- Grid-responsive design using CSS Grid
- Semantic grouping of related information
- Conditional rendering based on data availability
- Informational notes section

#### ReportActions.jsx
Handles report generation requests:
- Dual-format support (TXT and JSON)
- POST requests to backend report endpoint
- Blob creation and automatic download
- Error handling and user feedback

#### Dashboard.jsx
Main page controller:
- State management for analysis data and UI controls
- Coordination between upload and display components
- Conditional rendering based on analysis status
- Event handling for user interactions

### Backend Modules

#### app/__init__.py
Application factory pattern implementation:
- Flask app creation and configuration
- CORS middleware setup
- File upload size configuration
- Blueprint registration for API routes

#### app/forensic.py
File validation utilities:
- Extension-based file type checking
- MIME type validation approach
- Security-focused filename handling

#### app/routes.py
API endpoint implementations:
- `/health`: Service health monitoring
- `/analyze`: Main image processing pipeline
- `/report`: Report generation in multiple formats
- Error handling with appropriate HTTP status codes
- JSON response formatting

#### app/metadata.py
EXIF and image metadata extraction:
- Basic format, dimensions, and color mode detection
- EXIF data parsing using piexif library
- GPS coordinate conversion to decimal degrees
- Camera settings extraction (exposure, aperture, ISO, focal length)
- DateTime formatting and localization
- Error handling for corrupted or missing EXIF data

#### app/hashing.py
Cryptographic hash calculation:
- MD5, SHA-1, SHA-256 implementation using hashlib
- Binary data processing for accuracy
- Consistent lowercase hexadecimal output
- Performance-optimized for various file sizes

#### app/ela.py
Error Level Analysis implementation:
- JPEG-specific algorithm implementation
- Quality parameter configuration (default: 90%)
- Amplification factor for visibility (default: 10x)
- Pixel difference calculation using PIL.ImageChops
- Brightness enhancement for visibility
- Base64 encoding for frontend transmission
- Error handling for non-JPEG formats

#### app/reports.py
Report generation functionality:
- Structured data formatting for TXT and JSON outputs
- Human-readable text report generation
- Machine-readable JSON report generation
- Timestamp formatting in ISO 8601 UTC
- Analysis identification and tracking
- Comprehensive data inclusion from analysis results

## Data Flow

### Image Analysis Process
1. **Frontend**: User selects image file → Validation → Preview generation
2. **Frontend → Backend**: Multipart/form-data POST to `/api/analyze`
3. **Backend**: 
   - File reception and size validation
   - Image format detection and validation
   - Metadata extraction pipeline
   - Hash calculation from original bytes
   - ELA processing (JPEG only)
   - Response assembly with all results
4. **Backend → Frontend**: JSON response with analysis data
5. **Frontend**: State update → Component re-rendering → Result display

### Report Generation Process
1. **Frontend**: User selects report format → Data preparation
2. **Frontend → Backend**: POST to `/api/report` with analysis data and format
3. **Backend**: 
   - Data validation and formatting
   - Report generation based on requested format
   - File generation with appropriate headers
4. **Backend → Frontend**: File download response
5. **Frontend**: Automatic download initiation

## Security Considerations

### Input Validation
- File extension whitelisting
- MIME type verification
- File size limits (10MB)
- Image format validation via PIL
- Secure filename handling

### Processing Security
- In-memory processing when possible
- Temporary file handling with automatic cleanup
- No persistent storage of uploaded evidence
- Error message sanitization (no stack traces exposed)

### Communication Security
- CORS configuration for frontend origin restriction
- JSON content type enforcement
- HTTP status code adherence
- Error message generalization for production

### Cryptographic Security
- Standard library hash functions (hashlib)
- No custom cryptographic implementations
- Proper hash output formatting
- Collision-resistant algorithm selection

## Performance Characteristics

### Frontend
- Initial load: <2 seconds on broadband
- Component rendering: <100ms for typical analysis
- Memory usage: Proportional to image size for preview
- Bundle size: ~150KB gzipped

### Backend
- Request processing: <500ms for typical images
- Memory usage: Scales with image dimensions
- Concurrent support: Gunicorn worker-based scalability
- File processing: Streaming where possible to reduce memory footprint

### Scalability Limits
- Maximum concurrent users: Depends on server resources
- Maximum image size: 10MB (configurable)
- Processing time: O(n) where n = number of pixels
- Memory efficiency: Optimized for common image sizes

## API Specifications

### Health Check Endpoint
```
GET /api/health
Response:
{
  "status": "string",
  "service": "string",
  "version": "string"
}
```

### Image Analysis Endpoint
```
POST /api/analyze
Parameters:
  - image: file (form-data)

Response (Success):
{
  "analysis_id": "string",
  "filename": "string",
  "file_size": "integer",
  "format": "string",
  "width": "integer",
  "height": "integer",
  "mode": "string",
  "metadata": "object",
  "hashes": {
    "md5": "string",
    "sha1": "string",
    "sha256": "string"
  },
  "ela_available": "boolean",
  "ela_result": "string (base64 PNG) or null"
}

Response (Error):
{
  "error": "string message"
}
```

### Report Generation Endpoint
```
POST /api/report
Parameters:
  - analysis_data: object (from /analyze response)
  - format: string ("txt" or "json")

Response (Success - JSON):
  Analysis data in JSON format

Response (Success - TXT):
  Formatted text report with Content-Type: text/plain

Response (Error):
{
  "error": "string message"
}
```

## Deployment Configuration

### Vercel (Frontend)
- Build Command: `npm run build`
- Output Directory: `dist`
- Framework: Vite (SPA)
- Routes: All paths serve index.html for client-side routing
- Environment Variables:
  - `VITE_API_BASE_URL`: Backend API URL

### Render (Backend)
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`
- Health Check Path: `/api/health`
- Environment Variables:
  - `FRONTEND_ORIGIN`: Frontend origin for CORS
- Python Version: Compatible with requirements
- Worker Count: Automatic scaling based on plan

## Dependencies

### Frontend
- react: ^18.2.0
- react-dom: ^18.2.0
- @vitejs/plugin-react: ^4.0.0
- vite: ^4.4.0

### Backend
- Flask==2.3.3
- Pillow>=10.0.0
- numpy==1.24.3
- python-dotenv==1.0.0
- gunicorn==20.1.0
- piexif==1.1.3
- flask-cors==6.0.5
- pytest==9.1.1 (testing)

## Error Handling

### Frontend Errors
- Network failures: Retry suggestions and offline indicators
- Invalid responses: User-friendly error messages
- Validation errors: Specific field-level feedback
- Processing delays: Loading states with cancellation options

### Backend Errors
- Validation errors: 4xx HTTP status codes with descriptive messages
- Processing failures: 500 HTTP status codes with generic messages
- File errors: Specific messages for size, type, and format issues
- Unexpected errors: Generalized messages to prevent information leakage

## Testing Strategy

### Backend Testing
- Unit testing with pytest
- Mock file data for consistent testing
- Endpoint testing with Flask test client
- Hash algorithm validation with known values
- Metadata extraction with synthetic EXIF data
- File validation testing with various inputs
- Error condition testing with invalid inputs

### Frontend Testing
- Manual testing of all user interactions
- Cross-browser compatibility verification
- Responsive design testing at multiple breakpoints
- Build process verification
- Dependency security scanning

## Limitations and Known Issues

### Current Limitations
1. **ELA Specificity**: Standard ELA only reliable for JPEG images
2. **Metadata Dependency**: Results depend on embedded EXIF presence
3. **Hash Sensitivity**: Any byte change produces completely different الكتلة
4. **No AI Components**: Purely traditional forensics methods
5. **Educational Focus**: Not certified for legal evidence processing

### Browser Compatibility
- Chrome: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Edge: Latest 2 versions
- Mobile Safari: Latest 2 versions
- Chrome Android: Latest 2 versions

### Future Enhancements
- Reference hash verification system
- Batch processing capabilities
- Advanced image forensics techniques
- Machine learning-assisted analysis (research only)
- Blockchain-based evidence tracking
- Mobile application versions

## Contact and Support

For technical issues or questions regarding this implementation:
- Refer to the source code comments for implementation details
- Consult the README.md for setup and deployment instructions
- Review the USER_GUIDE.md for end-user documentation
- Check the LICENSE file for usage rights and limitations

---
*CSDF - Digital Image Forensics and Analysis Tool*
*Technical Reference for Development and Deployment*