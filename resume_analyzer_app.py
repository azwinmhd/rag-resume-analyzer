import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="RAG Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 RAG-Powered Resume & Job Fit Analyzer")
st.markdown("""
This tool uses **Retrieval-Augmented Generation (RAG)** to analyze how well your resume matches a job description.
It intelligently extracts relevant sections and provides detailed insights.
""")

# Sidebar for settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Your Resume")
    resume_text = st.text_area(
        "Paste your resume here:",
        height=300,
        placeholder="Paste your complete resume..."
    )

with col2:
    st.subheader("💼 Job Description")
    job_desc = st.text_area(
        "Paste the job description here:",
        height=300,
        placeholder="Paste the job description..."
    )

# Analysis button
if st.button("🔍 Analyze Match", use_container_width=True):
    if not resume_text or not job_desc:
        st.error("Please provide both resume and job description!")
    elif not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar!")
    else:
        try:
            with st.spinner("Analyzing resume fit... This may take a moment..."):
                
                # Step 1: Split resume into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                resume_chunks = text_splitter.split_text(resume_text)
                
                # Step 2: Create embeddings and vector store
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                vector_store = FAISS.from_texts(resume_chunks, embedding=embeddings)
                
                # Step 3: Initialize LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.3,
                    google_api_key=api_key
                )
                
                # Step 4: Create RAG chain for matching analysis
                match_prompt = PromptTemplate(
                    input_variables=["context", "question"],
                    template="""
                    Based on the resume sections provided below, analyze how well the candidate matches the job requirements.
                    
                    Resume Context:
                    {context}
                    
                    Job Description:
                    {question}
                    
                    Please provide:
                    1. Overall Match Score (0-100%)
                    2. Key Matching Skills
                    3. Missing Skills/Experience
                    4. Strengths for this role
                    5. Areas to improve
                    
                    Be specific and actionable.
                    """
                )
                
                # Step 5: Retrieve relevant resume sections
                relevant_docs = vector_store.similarity_search(job_desc, k=5)
                
                # Step 6: Create chain and run analysis
                chain = load_qa_chain(
                    llm,
                    chain_type="stuff",
                    prompt=match_prompt,
                    verbose=False
                )
                
                response = chain(
                    {
                        "input_documents": relevant_docs,
                        "question": job_desc
                    },
                    return_only_outputs=True
                )
                
                # Display results
                st.success("Analysis Complete!")
                
                st.markdown("---")
                st.subheader("📊 Analysis Results")
                st.markdown(response["output_text"])
                
                # Additional insights
                st.markdown("---")
                st.subheader("💡 Next Steps")
                st.info("""
                Based on this analysis:
                1. Highlight the matching skills in your resume
                2. Address the missing skills through learning/projects
                3. Prepare examples that demonstrate your strengths
                4. Practice answering questions about the identified gaps
                """)
                
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.info("Make sure your Google Gemini API key is valid and has access to the embedding and chat models.")

# Footer
st.markdown("---")
st.markdown("""
### How it works:
1. **Text Chunking**: Your resume is split into semantic chunks
2. **Embeddings**: Each chunk is converted to vector embeddings using Google's embedding model
3. **Similarity Search**: Job description is matched against resume chunks
4. **RAG Analysis**: Relevant resume sections are passed to Gemini for intelligent analysis
5. **Detailed Insights**: Get actionable feedback on your fit

Built with LangChain + Google Gemini + FAISS
""")