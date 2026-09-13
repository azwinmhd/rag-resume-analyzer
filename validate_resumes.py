from scoring import calculate_final_score, get_matching_skills, get_missing_skills
import os

# Job descriptions for testing
JOB_DESCRIPTIONS = {
    "senior_data_scientist": """
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
- Drive measurable business impact through data
- Collaborate with engineering and product teams
""",

    "junior_data_scientist": """
Junior Data Scientist

Requirements:
- 1-3 years data science experience or recent graduate
- Python and SQL proficiency
- Machine Learning fundamentals
- Statistics knowledge
- Data visualization (Tableau/Power BI)

Responsibilities:
- Develop ML models under senior guidance
- Analyze datasets and create visualizations
- Support data science initiatives
- Learn new tools and methodologies
"""
}

def run_validation():
    """Validate all extracted resumes"""
    
    output_folder = "./extracted_resumes"
    
    if not os.path.exists(output_folder):
        print("❌ No extracted_resumes folder found!")
        print("Run: py -3.11 extract_resumes.py")
        return
    
    # Get all extracted resumes
    resume_files = sorted([f for f in os.listdir(output_folder) if f.endswith('.txt')])
    
    if not resume_files:
        print("❌ No resumes found in extracted_resumes folder!")
        return
    
    print("=" * 120)
    print("RESUME VALIDATION - SENIOR DATA SCIENTIST ROLE")
    print("=" * 120)
    
    job_role = "senior_data_scientist"
    job_desc = JOB_DESCRIPTIONS[job_role]
    
    results = []
    
    # Process each resume
    for i, resume_file in enumerate(resume_files, 1):
        try:
            resume_path = os.path.join(output_folder, resume_file)
            
            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()
            
            # Calculate metrics
            score = calculate_final_score(resume_text, job_desc)
            matching_skills = get_matching_skills(resume_text, job_desc)
            missing_skills = get_missing_skills(resume_text, job_desc)
            
            candidate_name = resume_file.replace('.txt', '')
            
            result = {
                "rank": i,
                "candidate": candidate_name,
                "score": score,
                "matching": len(matching_skills),
                "missing": len(missing_skills),
                "matching_skills": matching_skills,
                "missing_skills": missing_skills
            }
            
            results.append(result)
            
            # Print result
            print(f"{i:2}. {candidate_name:40} | Score: {score:3}% | ✅ {len(matching_skills):2} | ❌ {len(missing_skills):2}")
        
        except Exception as e:
            print(f"{i:2}. {resume_file:40} | ERROR: {str(e)}")
    
    # Summary statistics
    print("=" * 120)
    print("SUMMARY STATISTICS")
    print("=" * 120)
    
    if results:
        scores = [r["score"] for r in results]
        avg_score = sum(scores) / len(scores)
        
        print(f"Total Resumes Analyzed: {len(results)}")
        print(f"Average Match Score: {avg_score:.1f}%")
        print(f"Highest Score: {max(scores)}%")
        print(f"Lowest Score: {min(scores)}%")
        print(f"Scores 70%+: {sum(1 for s in scores if s >= 70)} resumes")
        print(f"Scores 50-69%: {sum(1 for s in scores if 50 <= s < 70)} resumes")
        print(f"Scores <50%: {sum(1 for s in scores if s < 50)} resumes")
    
    # Find your resume (if it exists)
    your_resumes = [r for r in results if 'azwin' in r['candidate'].lower()]
    if your_resumes:
        print(f"\n🎯 YOUR RESUME:")
        for r in your_resumes:
            print(f"   {r['candidate']}: {r['score']}%")
            print(f"   Matching Skills: {', '.join(r['matching_skills']) if r['matching_skills'] else 'None'}")
            print(f"   Missing Skills: {', '.join(r['missing_skills']) if r['missing_skills'] else 'None'}")
    
    print("=" * 120)
    
    return results

if __name__ == "__main__":
    run_validation()