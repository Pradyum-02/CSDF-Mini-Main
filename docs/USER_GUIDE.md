# CSDF User Guide

## Getting Started

Welcome to CSDF - Digital Image Forensics and Analysis Tool. This guide will help you navigate and use all features of the application.

### Accessing the Application

Once deployed, access the application through your web browser at the frontend URL provided by Vercel.

## Using CSDF

### 1. Image Upload

Upon opening the application, you'll see the main dashboard with an image upload area:

- **Drag & Drop**: Drag an image file from your computer and drop it onto the upload area
- **Click to Upload**: Click the upload area to open your file selector and choose an image
- **Supported Formats**: JPEG, PNG, TIFF, BMP, WebP
- **Maximum Size**: 10 MB per file

### 2. Image Analysis

After selecting an image, the application will automatically:

1. Validate the file format and size
2. Extract metadata using EXIF parsing
3. Calculate cryptographic hashes (MD5, SHA-1, SHA-256)
4. Perform Error Level Analysis (if applicable to JPEG)
5. Display all results in organized panels

### 3. Reviewing Results

The analysis results are displayed in several sections:

#### File Information
- Original filename
- File size (bytes and human-readable format)
- Image format (JPEG, PNG, etc.)
- Dimensions (width × height in pixels)
- Aspect ratio
- Color mode (RGB, Grayscale, etc.)

#### Metadata Panel
Displays extracted EXIF information if available:
- Camera manufacturer and model
- Date and time the image was captured
- GPS coordinates (if embedded)
- Camera settings (aperture, shutter speed, ISO, focal length)
- Software used to create or modify the image

#### Hash Values
Cryptographic hashes of the original image file:
- MD5: 32-character hexadecimal string
- SHA-1: 40-character hexadecimal string
- SHA-256: 64-character hexadecimal string
*(Click "Copy" to copy any hash to your clipboard)*

#### Error Level Analysis (ELA)
For JPEG images only:
- Visual representation of compression inconsistencies
- Bright areas indicate different compression levels
- **Note**: ELA requires expert interpretation - bright areas do not prove tampering

#### Analysis Summary
Consolidated view of all findings with explanatory notes.

### 4. Generating Reports

To download a forensic analysis report:

1. Click either "Download TXT Report" or "Download JSON Report"
2. The report will be automatically downloaded to your device
3. Reports include:
   - Analysis timestamp and unique ID
   - All file information and metadata
   - Complete hash values
   - ELA status and parameters
   - Explanatory notes and limitations

## Understanding the Results

### Metadata Interpretation
- Present metadata confirms certain information was embedded when the image was created/saved
- Absent metadata doesn't indicate manipulation - many legitimate reasons exist for missing EXIF data
- GPS coordinates, when present, show where the image was taken (if enabled on the camera)

### Hash Value Usage
- Hash values uniquely identify the exact file contents
- Use hash values to verify file integrity over time or across transfers
- Identical hashes mean identical files; different hashes mean different files

### ELA Interpretation (JPEG Only)
- Uniform compression appears dark in ELA
- Edited/resaved areas often appear brighter
- **Important Factors Affecting ELA**:
  - Image content (high-detail vs flat areas)
  - Multiple saves/edits
  - Different software or quality settings
  - Scanning or printing then re-photographing
  - Always consult a forensic expert for definitive conclusions

## Troubleshooting

### Common Issues

**"Invalid image file" error**
- Ensure the file is actually an image, not another file types with image extension
- Try opening the file in an image viewer to confirm it's valid

**"File type not supported" error**
- Verify your file is one of: JPEG, PNG, TIFF, BMP, WebP
- Check that the file extension matches the actual file type

**"File size exceeds limit" error**
- Reduce image dimensions or save with higher compression
- Maximum allowed size is 10 MB

**Analysis fails to start**
- Check your internet connection
- Verify the backend service is running
- Contact administrator if problem persists

**No metadata displayed**
- Many images, especially those edited or saved from phones/social media, have metadata stripped
- This is normal and doesn't indicate anything suspicious

**ELA not available**
- ELA only works with JPEG images
- Other formats use different compression methods unsuitable for standard ELA

## Best Practices

### For Accurate Results
1. Use original, unaltered images when possible
2. Avoid uploading images through social media or messaging apps first (they often strip metadata)
3. For legal matters, consult a certified digital forensics examiner
4. Document your analysis process and findings

### For Educational Use
- Experiment with known-original images to establish baselines
- Test how different editing operations affect ELA results
- Compare metadata between original and exported images
- Understand that tools assist experts but don't replace expert judgment

## Security & Privacy

- Images are processed temporarily and not stored permanently
- No uploaded images are sent to external servers or third parties
- All analysis happens in your browser and on the designated backend server
- The application does not collect personal data beyond what's necessary for analysis
- Session data is cleared when you navigate away or close the browser

## Getting Help

If you encounter issues not covered in this guide:
1. Check that both frontend and backend services are operational
2. Verify network connectivity between frontend and backend
3. Consult the technical documentation for API specifications
4. Contact your system administrator or instructor for further assistance

---
*CSDF - Digital Image Forensics and Analysis Tool*
*Educational Tool for Cyber Security and Digital Forensics Studies*