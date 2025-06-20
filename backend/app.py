
from flask import Flask
from flask_cors import CORS
import os
import logging
from config import Config
from data_structures.skill_trie import SkillTrie
from api.routes import api_bp
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    # Enable CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])
    # Create upload folder if it doesn"t exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    # Initialize skill trie
    app.skill_trie = SkillTrie()
    try:
        app.skill_trie.load_skills_from_file("data/skills.json")
    except Exception as e:
        logging.warning(f"Could not load skills file: {e}")
        # Create some default skills for testing
        default_skills = ["python", "javascript", "react", "flask", "sql", "machine learning"]
        for skill in default_skills:
            app.skill_trie.insert(skill)
    # Initialize NLP service (simplified for testing without spaCy)
    class SimpleNLPService:
        def __init__(self, skill_trie):
            self.skill_trie = skill_trie
        
        def extract_entities(self, text):
            import re
            # Simple entity extraction without spaCy
            entities = {
                'PERSON': [],
                'ORG': [],
                'SKILL': [],
                'EMAIL': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
                'PHONE': re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text),
                'LINKEDIN': re.findall(r'linkedin\.com/in/[\w-]+', text.lower()),
                'EDUCATION': [],
                'EXPERIENCE': []
            }
            
            # Simple skill extraction
            words = text.lower().split()
            for word in words:
                if self.skill_trie.search(word):
                    entities['SKILL'].append(word)
            
            return entities
    
    app.nlp_service = SimpleNLPService(app.skill_trie)
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "skills_loaded": app.skill_trie.skill_count}
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

