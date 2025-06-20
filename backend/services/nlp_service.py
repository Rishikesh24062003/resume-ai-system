import spacy
import re
from spacy.tokens import Doc
from spacy.language import Language
# Load the English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install spaCy English model: python -m spacy download en_core_web_sm")
    raise
@Language.component("contact_extractor")
def contact_extractor(doc):
    """Custom spaCy component to extract contact information"""
    # Email extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, doc.text)
    # Phone extraction
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', # US format
        r'\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b', # (123) 456-7890
        r'\b\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b' # International
    ]
    phones = []
    for pattern in phone_patterns:
        phones.extend(re.findall(pattern, doc.text))
    # LinkedIn profile extraction
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin = re.findall(linkedin_pattern, doc.text.lower())
    doc._.emails = emails
    doc._.phones = phones
    doc._.linkedin = linkedin
    return doc
class NLPService:
    """Advanced NLP service for resume processing"""
    def __init__(self, skill_trie):
        # Set custom extensions
        if not Doc.has_extension("emails"):
            Doc.set_extension("emails", default=[])
        if not Doc.has_extension("phones"):
            Doc.set_extension("phones", default=[])
        if not Doc.has_extension("linkedin"):
            Doc.set_extension("linkedin", default=[])
        self.nlp = nlp
        self.nlp.add_pipe("contact_extractor", last=True)
        self.skill_trie = skill_trie
    def extract_entities(self, text):
        """Extract all relevant entities from resume text"""
        doc = self.nlp(text)
        entities = {
            'PERSON': self._extract_persons(doc),
            'ORG': self._extract_organizations(doc),
            'SKILL': self._extract_skills(doc),
            'EMAIL': doc._.emails,
            'PHONE': doc._.phones,
            'LINKEDIN': doc._.linkedin,
            'EDUCATION': self._extract_education(doc),
            'EXPERIENCE': self._extract_experience(doc)
        }
        return entities
    def _extract_persons(self, doc):
        """Extract person names, typically the candidate's name"""
        persons = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                persons.append(ent.text.strip())
        return list(set(persons))
    def _extract_organizations(self, doc):
        """Extract organization names"""
        orgs = []
        for ent in doc.ents:
            if ent.label_ == "ORG":
                orgs.append(ent.text.strip())
        return list(set(orgs))
    def _extract_skills(self, doc):
        """Extract skills using the skill trie and NLP"""
        skills = set()
        # Extract using trie for exact matches
        for token in doc:
            if not token.is_stop and not token.is_punct and len(token.text) > 2:
                # Exact match
                if self.skill_trie.search(token.text):
                    skills.add(token.text)
                # Fuzzy match for potential typos
                else:
                    fuzzy_matches = self.skill_trie.fuzzy_search(token.text, max_distance=1)
                    if fuzzy_matches and fuzzy_matches[0][1] <= 1:
                        skills.add(fuzzy_matches[0][0])
        # Extract multi-word skills
        for noun_phrase in doc.noun_chunks:
            phrase = noun_phrase.text.lower().strip()
            if self.skill_trie.search(phrase):
                skills.add(phrase)
        return list(skills)
    def _extract_education(self, doc):
        """Extract education information"""
        education_keywords = ["university", "college", "bachelor", "master", "phd", "degree", "diploma", "graduate", "undergraduate", "alumni", "school"]
        education = []
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in education_keywords):
                education.append(sent.text.strip())
        return education
    def _extract_experience(self, doc):
        """Extract work experience information"""
        experience = []
        # Look for date ranges and organizations
        for ent in doc.ents:
            if ent.label_ in ["DATE", "ORG"]:
                # Get surrounding context
                start = max(0, ent.start - 10)
                end = min(len(doc), ent.end + 10)
                context = doc[start:end].text
                experience.append(context.strip())
        return experience

