from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List
import logging
class ATSScorer:
    """Advanced ATS scoring algorithm with multiple scoring factors"""
    def __init__(self):
        self.weights = {
            'skills_match': 0.35,
            'keyword_density': 0.25,
            'experience_match': 0.20,
            'education_match': 0.10,
            'format_score': 0.10
        }
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words='english',
            max_features=5000,
            lowercase=True,
            token_pattern=r'\b[a-zA-Z]{2,}\b'
        )
    def calculate_ats_score(self, resume_data: Dict, job_data: Dict) -> Dict:
        """Calculate comprehensive ATS score"""
        try:
            scores = {}
            # Skills matching score
            scores['skills_match'] = self._calculate_skills_match(
                resume_data.get('skills', []),
                job_data.get('skills', [])
            )
            # Keyword density score
            scores['keyword_density'] = self._calculate_keyword_density(
                resume_data.get('text', ''),
                job_data.get('description', '')
            )
            # Experience matching score
            scores['experience_match'] = self._calculate_experience_match(
                resume_data.get('experience', []),
                job_data.get('min_experience', 0)
            )
            # Education matching score
            scores['education_match'] = self._calculate_education_match(
                resume_data.get('education', []),
                job_data.get('required_education', [])
            )
            # Format score (ATS readability)
            scores['format_score'] = self._calculate_format_score(resume_data.get('text', ''))
            # Calculate weighted total score
            total_score = sum(
                scores[component] * self.weights[component]
                for component in scores.keys()
            )
            return {
                'total_score': round(total_score * 100, 2),
                'component_scores': {k: round(v * 100, 2) for k, v in scores.items()},
                'recommendations': self._generate_recommendations(scores)
            }
        except Exception as e:
            logging.error(f"Error calculating ATS score: {e}")
            return {'total_score': 0, 'component_scores': {}, 'recommendations': []}
    def _calculate_skills_match(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skills matching score"""
        if not job_skills:
            return 1.0
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        matched_skills = set(resume_skills_lower) & set(job_skills_lower)
        return len(matched_skills) / len(job_skills_lower)
    def _calculate_keyword_density(self, resume_text: str, job_description: str) -> float:
        """Calculate keyword density using TF-IDF"""
        if not resume_text or not job_description:
            return 0.0
        try:
            documents = [resume_text, job_description]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
            return float(similarity)
        except Exception as e:
            logging.error(f"Error calculating keyword density: {e}")
            return 0.0
    def _calculate_experience_match(self, resume_experience: List[str], required_years: int) -> float:
        """Calculate experience matching score"""
        if required_years == 0:
            return 1.0
        # Simple heuristic: count years mentioned in experience
        total_years = 0
        for exp in resume_experience:
            years = self._extract_years_from_text(exp)
            total_years += years
        return min(total_years / required_years, 1.0)
    def _calculate_education_match(self, resume_education: List[str], required_education: List[str]) -> float:
        """Calculate education matching score"""
        if not required_education:
            return 1.0
        if not resume_education:
            return 0.0
        # Simple matching based on keywords
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'certification']
        resume_edu_text = ' '.join(resume_education).lower()
        matches = sum(1 for keyword in education_keywords if keyword in resume_edu_text)
        return min(matches / len(required_education), 1.0)
    def _calculate_format_score(self, resume_text: str) -> float:
        """Calculate format score based on ATS readability"""
        if not resume_text:
            return 0.0
        score = 0.0
        # Check for proper sections
        sections = ['experience', 'education', 'skills', 'contact']
        for section in sections:
            if section in resume_text.lower():
                score += 0.25
        return min(score, 1.0)
    def _extract_years_from_text(self, text: str) -> int:
        """Extract years of experience from text"""
        import re
        year_patterns = [
            r'(\d+)\s*years?',
            r'(\d+)\s*yrs?',
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*to\s*(\d{4})'
        ]
        total_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 2: # Date range
                        try:
                            years = int(match[1]) - int(match[0])
                            total_years += max(0, years)
                        except ValueError:
                            continue
                    else:
                        try:
                            total_years += int(match[0])
                        except ValueError:
                            continue
                else:
                    try:
                        total_years += int(match)
                    except ValueError:
                        continue
        return total_years
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        if scores['skills_match'] < 0.5:
            recommendations.append("Add more relevant skills mentioned in the job description.")
        if scores['keyword_density'] < 0.3:
            recommendations.append("Include more keywords from the job description in your resume.")
        if scores['format_score'] < 0.7:
            recommendations.append("Improve resume structure with clear sections (Experience, Education, Skills, Contact).")
        if scores['experience_match'] < 0.6:
            recommendations.append("Highlight more relevant work experience or years of experience.")
        return recommendations

