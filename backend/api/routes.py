from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
import logging
from datetime import datetime
from services.file_service import FileService
from algorithms.ats_scorer import ATSScorer
api_bp = Blueprint("api", __name__)
@api_bp.route("/upload", methods=["POST"])
def upload_resume():
    """Upload and process resume file"""
    try:
        # Check if file is present
        if "resume" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        # Validate file
        is_valid, message = FileService.validate_file(file.filename)
        if not is_valid:
            return jsonify({"error": message}), 400
        # Generate unique filename
        file_extension = file.filename.rsplit(".", 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)
        # Save file
        file.save(file_path)
        # Extract text
        text = FileService.extract_text(file_path, file_extension)
        # Process with NLP
        entities = current_app.nlp_service.extract_entities(text)
        # Store in database (simplified for this example)
        resume_data = {
            "id": str(uuid.uuid4()),
            "filename": file.filename,
            "unique_filename": unique_filename,
            "text": text,
            "entities": entities,
            "created_at": str(datetime.utcnow())
        }
        # Clean up uploaded file
        os.remove(file_path)
        return jsonify({
            "success": True,
            "resume_id": resume_data["id"],
            "entities": entities,
            "text_preview": text[:500] + "..." if len(text) > 500 else text
        })
    except Exception as e:
        logging.error(f"Error processing resume upload: {e}")
        return jsonify({"error": "Internal server error"}), 500
@api_bp.route("/score", methods=["POST"])
def calculate_score():
    """Calculate ATS score for resume against job description"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        resume_data = data.get("resume_data", {})
        job_description = data.get("job_description", "")
        if not resume_data or not job_description:
            return jsonify({"error": "Missing resume data or job description"}), 400
        # Prepare job data
        job_data = {
            "description": job_description,
            "skills": job_description.split(), # Simplified skill extraction
            "min_experience": data.get("min_experience", 0),
            "required_education": data.get("required_education", [])
        }
        # Calculate ATS score
        scorer = ATSScorer()
        score_result = scorer.calculate_ats_score(resume_data, job_data)
        return jsonify({
            "success": True,
            "ats_score": score_result
        })
    except Exception as e:
        logging.error(f"Error calculating ATS score: {e}")
        return jsonify({"error": "Internal server error"}), 500
@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "resume-ai-backend"
    })

