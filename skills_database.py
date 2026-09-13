# Common skills for data science roles
DATA_SCIENCE_SKILLS = {
    "python": ["python", "py"],
    "sql": ["sql", "mysql", "postgresql", "oracle"],
    "r": ["r programming", "r language"],
    "machine learning": ["machine learning", "ml", "sklearn", "scikit-learn"],
    "deep learning": ["deep learning", "neural network", "tensorflow", "keras", "pytorch"],
    "data analysis": ["data analysis", "analytics", "data analytics"],
    "statistics": ["statistics", "statistical", "hypothesis testing"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi"],
    "excel": ["excel", "vba", "spreadsheet"],
    "spark": ["spark", "apache spark", "pyspark"],
    "aws": ["aws", "amazon web services", "s3", "ec2"],
    "gcp": ["gcp", "google cloud", "bigquery"],
    "azure": ["azure", "microsoft azure"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab"],
    "tensorflow": ["tensorflow"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv"],
    "etl": ["etl", "extract transform load"],
    "data pipeline": ["data pipeline", "pipeline"],
    "api": ["api", "rest", "restful"],
    "linux": ["linux", "unix"],
    "communication": ["communication", "presentation"],
    "leadership": ["leadership", "mentor", "lead"],
    "project management": ["project management", "agile", "scrum"],
}

def get_skill_keywords():
    """Flatten skills for searching"""
    all_keywords = {}
    for skill, keywords in DATA_SCIENCE_SKILLS.items():
        for keyword in keywords:
            all_keywords[keyword.lower()] = skill
    return all_keywords

def extract_skills(text):
    """Extract skills from text"""
    text_lower = text.lower()
    found_skills = set()
    
    for keyword, skill_name in get_skill_keywords().items():
        if keyword in text_lower:
            found_skills.add(skill_name)
    
    return found_skills