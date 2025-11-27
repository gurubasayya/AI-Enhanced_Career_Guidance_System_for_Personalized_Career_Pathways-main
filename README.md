# CareerAI - AI-Powered Career Guidance System

A modern Flask web application that provides personalized career guidance using AI-powered analysis.

## Features

- **User Authentication**: Secure login and registration system
- **Smart Resume Upload**: Support for multiple file formats (PDF, DOC, DOCX, images) with automatic information extraction
- **Auto-Fill Personal Information**: Automatically extracts and pre-fills personal details from uploaded resumes
- **Personal Profile**: Comprehensive personal information collection
- **Skills Assessment**: Technical and soft skills evaluation
- **Aptitude Testing**: Optional comprehensive aptitude assessment
- **Career Analysis**: AI-powered career recommendations
- **Skill Gap Analysis**: Identify areas for improvement
- **Course Recommendations**: Personalized learning suggestions
- **Market Insights**: Global job market suitability analysis

## Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd career-guidance-flask
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
# Or use the installation script
python install_dependencies.py
\`\`\`

   **Note**: For image processing (OCR), you also need Tesseract OCR:
   - Windows: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. Create uploads directory:
\`\`\`bash
mkdir uploads
\`\`\`

5. Run the application:
\`\`\`bash
python app.py
\`\`\`

6. Open your browser and navigate to `http://localhost:5000`

## Project Structure

\`\`\`
career-guidance-flask/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── upload_resume.html # Resume upload
│   ├── personal_info.html # Personal information form
│   ├── skills_assessment.html # Skills evaluation
│   ├── exam_choice.html  # Assessment choice
│   ├── aptitude_test.html # Aptitude test
│   └── career_analysis.html # Results page
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── script.js    # JavaScript functionality
├── uploads/              # File upload directory
├── forms.py              # WTForms form definitions
├── requirements.txt      # Python dependencies
├── install_dependencies.py # Dependency installation script
├── test_resume_parser.py # Resume parsing test script
└── README.md            # Project documentation
\`\`\`

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Resume**: Upload your resume in supported formats (PDF, DOC, DOCX, images)
3. **Auto-Filled Information**: Review and update the automatically extracted personal information
4. **Skills Assessment**: Select your technical and soft skills
5. **Aptitude Test**: Choose to take the optional assessment for better recommendations
6. **View Results**: Get personalized career recommendations and skill gap analysis

## Resume Parsing Features

The application automatically extracts the following information from uploaded resumes:
- **Name**: Full name from resume header
- **Email**: Email address detection
- **Phone**: Phone number in various formats
- **LinkedIn**: LinkedIn profile URL
- **Education**: College/University name
- **Degree**: Degree program (Computer Science, Engineering, etc.)

### Supported File Formats
- **PDF**: Text extraction using pdfplumber
- **DOC/DOCX**: Microsoft Word document parsing
- **Images**: OCR text extraction from PNG, JPG, JPEG, GIF
- **TXT**: Plain text files

### Testing Resume Parser

To test the resume parsing functionality:
\`\`\`bash
python test_resume_parser.py
\`\`\`

## Future Enhancements

- Integration with actual AI/ML models for career analysis
- Database integration for user data persistence
- Email notifications and report generation
- Social media integration
- Advanced analytics and reporting
- Mobile app development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
