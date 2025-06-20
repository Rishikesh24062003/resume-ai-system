# Resume AI System

A comprehensive Resume Parsing and Ranking System built with Python, React, MongoDB, and Docker. This system leverages Natural Language Processing (NLP) and advanced data structures to efficiently parse resumes, extract relevant information, and provide ATS (Applicant Tracking System) compatibility scoring.

## Features

- **Resume Parsing**: Extract text from PDF, DOCX, DOC, and TXT files
- **NLP Processing**: Advanced entity extraction using spaCy
- **Skill Matching**: Efficient skill detection using Trie data structure with fuzzy search
- **ATS Scoring**: Comprehensive scoring algorithm with multiple factors
- **Modern UI**: React-based frontend with Tailwind CSS
- **Containerized**: Full Docker support for easy deployment

## Technology Stack

### Backend
- Python 3.11+
- Flask web framework
- spaCy for NLP processing
- scikit-learn for ML algorithms
- pdfplumber for PDF text extraction
- python-docx for Word document processing

### Frontend
- React 18
- Tailwind CSS for styling
- Lucide React for icons
- Axios for API communication

### Infrastructure
- Docker & Docker Compose
- MongoDB for data storage
- Redis for caching
- Nginx for reverse proxy

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 16+ (for local development)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-ai-system
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Full application: http://localhost (via Nginx)

### Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Upload Resume
```
POST /api/upload
Content-Type: multipart/form-data
Body: resume file
```

### Calculate ATS Score
```
POST /api/score
Content-Type: application/json
Body: {
  "resume_data": {...},
  "job_description": "...",
  "min_experience": 2,
  "required_education": ["bachelor"]
}
```

### Health Check
```
GET /api/health
GET /health
```

## Project Structure

```
resume-ai-system/
├── backend/
│   ├── algorithms/          # ATS scoring algorithms
│   ├── api/                # Flask API routes
│   ├── data/               # Skills data and configurations
│   ├── data_structures/    # Trie and other data structures
│   ├── services/           # Business logic services
│   ├── tests/              # Unit tests
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container config
├── nginx/
│   └── nginx.conf          # Nginx configuration
├── docker-compose.yml      # Multi-container setup
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Features in Detail

### Resume Parsing
- Supports multiple file formats (PDF, DOCX, DOC, TXT)
- Extracts clean, normalized text
- Handles various document layouts and formats

### NLP Processing
- Named Entity Recognition (NER) for persons, organizations
- Custom contact information extraction (emails, phones, LinkedIn)
- Education and experience section identification
- Advanced skill extraction with fuzzy matching

### ATS Scoring Algorithm
The scoring system evaluates resumes based on multiple factors:

1. **Skills Match (35%)**: Comparison with job requirements
2. **Keyword Density (25%)**: TF-IDF similarity with job description
3. **Experience Match (20%)**: Years of experience evaluation
4. **Education Match (10%)**: Educational background alignment
5. **Format Score (10%)**: ATS-friendly formatting assessment

### Skill Trie Data Structure
- Efficient skill matching with O(m) lookup time
- Fuzzy search with Levenshtein distance
- Supports skill categorization
- Memory-optimized with __slots__

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `MONGO_URI`: MongoDB connection string
- `REDIS_URL`: Redis connection string
- `CORS_ORIGINS`: Allowed CORS origins
- `UPLOAD_FOLDER`: File upload directory

### Skills Database
The system uses a JSON file (`backend/data/skills.json`) to store skill definitions with categories. You can extend this file to include more skills and categories.

## Development

### Adding New Skills
Edit `backend/data/skills.json`:
```json
{
  "skill": "new-technology",
  "category": "programming"
}
```

### Extending ATS Scoring
Modify `backend/algorithms/ats_scorer.py` to add new scoring factors or adjust weights.

### Custom NLP Components
Add new spaCy components in `backend/services/nlp_service.py` for additional entity extraction.

## Testing

Run backend tests:
```bash
cd backend
python -m pytest tests/
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Deployment

### Production Deployment
1. Update environment variables in `.env`
2. Set `FLASK_ENV=production`
3. Use proper secret keys and database credentials
4. Configure SSL/TLS certificates for HTTPS
5. Set up monitoring and logging

### Scaling Considerations
- Use multiple Gunicorn workers for backend
- Implement Redis caching for frequent operations
- Consider MongoDB sharding for large datasets
- Use CDN for frontend assets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.

