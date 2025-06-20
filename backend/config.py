import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/resume_ai')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB max file size
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

