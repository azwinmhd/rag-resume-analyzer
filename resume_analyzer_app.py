import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
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

# Layout
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

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_text(resume_text)

            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2"
            )

            vector_store = FAISS.from_texts(
                chunks,
                embeddings
            )

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.3
            )

            prompt = ChatPromptTemplate.from_template("""
You are an expert ATS and recruitment analyst.

Resume:
{context}

Job Description:
{input}

Provide:

1. Match Percentage (%)
2. Key Matching Skills
3. Missing Skills
4. Strengths
5. Improvement Suggestions
6. Final Recommendation

Format the response professionally.
""")

            document_chain = create_stuff_documents_chain(
                llm,
                prompt
            )

            retrieval_chain = create_retrieval_chain(
                vector_store.as_retriever(),
                document_chain
            )

            response = retrieval_chain.invoke({
                "input": job_desc
            })

            st.markdown("## 📈 ATS Analysis")

            st.markdown(
                f"""
                <div class="custom-card">
                {response["answer"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Analysis error: {str(e)}")