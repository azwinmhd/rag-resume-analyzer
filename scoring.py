from skills_database import extract_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_skill_match(resume_text, job_desc):
    """
    Calculate skill matching score
    Returns: 0-100 score
    """
    
    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)
    
    if not job_skills:
        return 50  # Default if no skills found
    
    # Calculate matching skills
    matching_skills = resume_skills.intersection(job_skills)
    
    # Score based on matches
    skill_match_percentage = (len(matching_skills) / len(job_skills)) * 100
    
    return min(100, skill_match_percentage)

def calculate_experience_match(resume_text, job_desc):
    """
    Calculate experience level match
    Returns: 0-100 score
    """
    
    # Experience keywords
    junior_indicators = ["intern", "entry level", "junior", "graduate", "fresh"]
    mid_indicators = ["3 years", "4 years", "5 years", "mid-level", "intermediate"]
    senior_indicators = ["senior", "lead", "principal", "10 years", "8 years", "expert"]
    
    resume_lower = resume_text.lower()
    job_lower = job_desc.lower()
    
    # Detect required level from job description
    required_level = "entry"
    if any(word in job_lower for word in senior_indicators):
        required_level = "senior"
    elif any(word in job_lower for word in mid_indicators):
        required_level = "mid"
    
    # Detect candidate level from resume
    candidate_level = "entry"
    if any(word in resume_lower for word in senior_indicators):
        candidate_level = "senior"
    elif any(word in resume_lower for word in mid_indicators):
        candidate_level = "mid"
    
    # Calculate match
    level_map = {"entry": 1, "mid": 2, "senior": 3}
    required_score = level_map.get(required_level, 1)
    candidate_score = level_map.get(candidate_level, 1)
    
    if candidate_score >= required_score:
        return 100
    else:
        return 50 + (candidate_score / required_score * 50)

def calculate_semantic_match(resume_text, job_desc):
    """
    Calculate semantic similarity using TF-IDF
    Returns: 0-100 score
    """
    
    try:
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        vectors = vectorizer.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return similarity * 100
    except:
        return 50

def calculate_final_score(resume_text, job_desc):
    """
    Calculate final match score (weighted average)
    """
    
    skill_score = calculate_skill_match(resume_text, job_desc)
    experience_score = calculate_experience_match(resume_text, job_desc)
    semantic_score = calculate_semantic_match(resume_text, job_desc)
    
    # Weighted average
    final_score = (
        skill_score * 0.5 +      # Skills are most important
        experience_score * 0.3 +  # Experience level matters
        semantic_score * 0.2      # Semantic match as tiebreaker
    )
    
    return int(min(100, max(0, final_score)))

def get_missing_skills(resume_text, job_desc):
    """Get skills that candidate is missing"""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)
    
    missing = job_skills - resume_skills
    return list(missing)

def get_matching_skills(resume_text, job_desc):
    """Get skills that candidate has"""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)
    
    matching = resume_skills.intersection(job_skills)
    return list(matching)