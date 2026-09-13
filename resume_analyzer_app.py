import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
import zipfile
import pandas as pd
from io import BytesIO
import tempfile

from scoring import (
    calculate_final_score, 
    get_matching_skills, 
    get_missing_skills
)

# Import scoring modules
try:
    from scoring import calculate_final_score, get_matching_skills, get_missing_skills
except ImportError:
    st.error("Missing scoring.py module. Please create it first.")
    st.stop()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate



# PDF support
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

load_dotenv()

# Async patch
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

def process_batch_resumes(zip_file, job_desc, api_key):
    """Process multiple resumes from a ZIP file"""
    
    results = []
    
    if not job_desc or not job_desc.strip():
        return [{"Candidate": "ERROR", "Match Score": 0, "Analysis": "Job description is empty!"}]
    
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        
        for file_name in file_list:
            # Skip folders and non-resume files
            if file_name.endswith('/'):
                continue
                
            if not file_name.endswith(('.pdf', '.txt')):
                continue
            
            file_content = zip_ref.read(file_name)
            resume_text = ""
            
            # Extract text
            if file_name.endswith('.txt'):
                try:
                    resume_text = file_content.decode('utf-8')
                except:
                    continue
                    
            elif file_name.endswith('.pdf'):
                if HAS_PYPDF:
                    try:
                        pdf_file = BytesIO(file_content)
                        reader = pypdf.PdfReader(pdf_file)
                        resume_text = "\n".join(
                            page.extract_text() or ""
                            for page in reader.pages
                        )
                    except:
                        continue
            
            # Skip if no text extracted
            if not resume_text or not resume_text.strip():
                results.append({
                    "Candidate": file_name.replace('.pdf', '').replace('.txt', ''),
                    "Match Score": 0,
                    "Analysis": "Could not extract text from resume"
                })
                continue
            
            try:
                # Calculate score using our algorithm
                score = calculate_final_score(resume_text, job_desc)
                matching_skills = get_matching_skills(resume_text, job_desc)
                missing_skills = get_missing_skills(resume_text, job_desc)
                
                # Build simple summary (no LLM for now)
                analysis_summary = f"""
CALCULATED SCORE: {score}%

Matching Skills ({len(matching_skills)}): {', '.join(matching_skills) if matching_skills else 'None'}
Missing Skills ({len(missing_skills)}): {', '.join(missing_skills) if missing_skills else 'None'}
"""
                
                results.append({
                    "Candidate": file_name.replace('.pdf', '').replace('.txt', ''),
                    "Match Score": score,
                    "Analysis": analysis_summary
                })
                
            except Exception as e:
                results.append({
                    "Candidate": file_name,
                    "Match Score": 0,
                    "Analysis": f"Error: {str(e)}"
                })
    
    return results if results else [{"Candidate": "ERROR", "Match Score": 0, "Analysis": "No resumes found in ZIP"}]
# Page config
st.set_page_config(
    page_title="ResumeAI | Smart Career Optimization Hub",
    page_icon="🎯",
    layout="wide"
)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.hero-container {
    text-align: center;
    padding: 2rem 0;
}

.brand-badge {
    display: inline-block;
    background: rgba(0,163,255,0.1);
    border: 1px solid rgba(0,163,255,0.3);
    color: #00A3FF;
    padding: 8px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-top: 1rem;
}

.accent-gradient {
    background: linear-gradient(90deg,#00A3FF,#00FFD1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 1.1rem;
    color: #94A3B8;
}

.custom-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg,#00A3FF,#00FFD1);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <span class="brand-badge">Next-Gen ATS Optimizer</span>
    <h1 class="main-title">
        Land More Interviews with
        <span class="accent-gradient"> Smart AI Alignment</span>
    </h1>
    <p class="subtitle">
        Instantly bridge the gap between your resume and hiring requirements.
    </p>
</div>
""", unsafe_allow_html=True)

api_key = os.getenv("GOOGLE_API_KEY")

resume_text = ""

api_key = os.getenv("GOOGLE_API_KEY")

# Add mode selector
st.markdown("<br>", unsafe_allow_html=True)
mode = st.radio(
    "Choose mode:",
    ("📄 Single Resume", "📦 Batch Processing (ZIP)"),
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("<br>", unsafe_allow_html=True)

resume_text = ""

# Layout
if mode == "📄 Single Resume":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "txt"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                resume_text = uploaded_file.read().decode("utf-8")
            elif uploaded_file.type == "application/pdf":
                if HAS_PYPDF:
                    reader = pypdf.PdfReader(uploaded_file)
                    resume_text = "\n".join(
                        page.extract_text() or ""
                        for page in reader.pages
                    )
            st.success("Resume uploaded successfully!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("💼 Job Description")
        job_desc = st.text_area(
            "Paste Job Description",
            height=250,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Analyze Button
    if st.button("📊 Scan & Analyze Application Fit"):
        if not resume_text:
            st.error("Please upload a resume.")
            st.stop()
        if not job_desc.strip():
            st.error("Please enter a job description.")
            st.stop()
        if not api_key:
            st.error("GOOGLE_API_KEY not found in .env file.")
            st.stop()

        try:
            with st.spinner("Analyzing resume..."):
                
                # Split text
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = splitter.split_text(resume_text)
                
                # Create embeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2"
                )
                vector_store = FAISS.from_texts(chunks, embeddings)
                
                # Initialize LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=api_key,
                    temperature=0.3
                )
                
                # Get relevant documents
                relevant_docs = vector_store.similarity_search(job_desc, k=5)
                context = "\n".join([doc.page_content for doc in relevant_docs])
                
                # Create prompt
                prompt = ChatPromptTemplate.from_template("""
You are an expert ATS and recruitment analyst.

Resume Context:
{context}

Job Description:
{job_desc}

Provide:
1. Match Percentage (%)
2. Key Matching Skills
3. Missing Skills
4. Strengths
5. Improvement Suggestions
6. Final Recommendation

Format professionally.
""")
                
                # Generate response
                calculated_score = calculate_final_score(resume_text, job_desc)
                matching_skills = get_matching_skills(resume_text, job_desc)
                missing_skills = get_missing_skills(resume_text, job_desc)

                formatted_prompt = prompt.format_messages(
                    context=context,
                    job_desc=job_desc
                )
                response = llm.invoke(formatted_prompt)
                st.markdown("## 📈 ATS Analysis")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match Score", f"{calculated_score}%")
                with col2:
                    st.metric("Matching Skills", len(matching_skills))
                with col3:
                    st.metric("Missing Skills", len(missing_skills))

                    st.markdown("---")
                    if matching_skills:
                        st.subheader("✅ Skills You Have")
                        st.write(", ".join(sorted(matching_skills)))

                    if missing_skills:
                        st.subheader("❌ Skills to Acquire")
                        st.write(", ".join(sorted(missing_skills)))

                        st.markdown("---")

                        st.markdown("### 📊 Detailed Analysis")
                        st.markdown(
                            f'<div class="custom-card">{response.content}</div>',
                            unsafe_allow_html=True
                        )
        
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")

else:  # Batch Processing Mode
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📦 Upload Resumes (ZIP)")
        st.write("Create a ZIP file with all resumes (.pdf or .txt)")
        zip_file = st.file_uploader(
            "Upload ZIP file",
            type=["zip"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("💼 Job Description")
        job_desc_batch = st.text_area(
            "Paste Job Description",
            height=250,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("📊 Analyze & Rank All Candidates"):
        if not zip_file:
            st.error("Please upload a ZIP file with resumes.")
            st.stop()
        if not job_desc_batch.strip():
            st.error("Please enter a job description.")
            st.stop()
        if not api_key:
            st.error("GOOGLE_API_KEY not found.")
            st.stop()
        
        try:
            with st.spinner("🔄 Processing resumes... This may take a minute"):
                results = process_batch_resumes(zip_file, job_desc_batch, api_key)
                
                # Sort by match score
                df = pd.DataFrame(results).sort_values("Match Score", ascending=False)
                
                st.markdown("## 🏆 Candidate Ranking")
                
                # Show rankings
                st.dataframe(
                    df[["Candidate", "Match Score"]],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Show detailed analysis
                st.markdown("---")
                st.markdown("## 📋 Detailed Analysis")
                
                for idx, row in df.iterrows():
                    with st.expander(f"🔍 {row['Candidate']} - {row['Match Score']}%"):
                        st.write(row['Analysis'])
                
                                # Download results - Create better formatted CSV
                csv_data = []
                for result in results:
                    # Parse analysis to extract skills
                    analysis = result.get("Analysis", "")
                    
                    matching_skills = ""
                    missing_skills = ""
                    
                    # Extract matching skills
                    if "Matching Skills" in analysis:
                        start = analysis.find("Matching Skills (")
                        if start != -1:
                            start = analysis.find(":", start) + 1
                            end = analysis.find("\n", start)
                            if end == -1:
                                end = analysis.find("Missing", start)
                            matching_skills = analysis[start:end].strip()
                    
                    # Extract missing skills
                    if "Missing Skills" in analysis:
                        start = analysis.find("Missing Skills (")
                        if start != -1:
                            start = analysis.find(":", start) + 1
                            end = len(analysis)
                            missing_skills = analysis[start:end].strip()
                    
                    csv_data.append({
                        "Candidate": result["Candidate"],
                        "Match Score (%)": result["Match Score"],
                        "Matching Skills": matching_skills,
                        "Missing Skills": missing_skills
                    })
                
                # Create DataFrame and convert to CSV
                csv_df = pd.DataFrame(csv_data)
                csv = csv_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="candidate_analysis.csv",
                    mime="text/csv"
                )
        
        except Exception as e:
            st.error(f"Batch processing error: {str(e)}")