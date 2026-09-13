from scoring import calculate_final_score, get_matching_skills, get_missing_skills
import zipfile
from io import BytesIO

# Test job description
job_desc = """
Senior Data Scientist

Requirements:
- 5+ years data science experience
- Python, SQL, Machine Learning expertise
- Deep Learning, TensorFlow/PyTorch
- AWS or GCP experience
- Leadership/mentoring experience
- Strong statistics and mathematics background

Responsibilities:
- Build and deploy production ML models
- Lead data science projects and teams
- Mentor junior data scientists
"""

# Read your ZIP file
zip_path = "extracted_resumes.zip"

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        print(f"Files in ZIP: {file_list}\n")
        
        # Process each file
        for file_name in file_list:
            print(f"Processing: {file_name}")
            
            if file_name.endswith('.txt'):
                file_content = zip_ref.read(file_name)
                resume_text = file_content.decode('utf-8')
                
                print(f"Resume length: {len(resume_text)} chars")
                print(f"First 100 chars: {resume_text[:100]}\n")
                
                # Score it
                score = calculate_final_score(resume_text, job_desc)
                matching = get_matching_skills(resume_text, job_desc)
                missing = get_missing_skills(resume_text, job_desc)
                
                print(f"Score: {score}%")
                print(f"Matching Skills: {matching}")
                print(f"Missing Skills: {missing}")
                print("---\n")
                
except Exception as e:
    print(f"ERROR: {str(e)}")