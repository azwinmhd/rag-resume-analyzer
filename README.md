# 🚀 RAG-Powered Resume Analyzer

A cutting-edge Retrieval-Augmented Generation (RAG) application that analyzes how well your resume matches job descriptions using semantic search and AI.

## 📋 Overview

This project demonstrates a real-world RAG implementation that:
- **Chunks your resume** into semantic sections
- **Creates vector embeddings** using Google's state-of-the-art models
- **Performs similarity search** to find relevant resume sections
- **Uses LLM** (Gemini) to provide intelligent analysis
- **Delivers actionable insights** on resume-job fit

## 🎯 Features

✅ **Semantic Matching** - Understands meaning, not just keywords  
✅ **RAG Architecture** - Retrieval-Augmented Generation for accurate analysis  
✅ **Vector Search** - FAISS for fast similarity matching  
✅ **AI-Powered Analysis** - Gemini LLM for intelligent insights  
✅ **Streamlit UI** - Clean, intuitive interface  
✅ **Free & Open-Source** - Use Google's free Gemini API  

## 🛠️ Tech Stack

- **LangChain** - LLM orchestration & RAG framework
- **Google Gemini** - Free LLM & embeddings
- **FAISS** - Vector database for similarity search
- **Streamlit** - Web UI framework
- **Python 3.8+**

## 📦 Installation

### 1. Clone or download this project
```bash
git clone https://github.com/azwinmhd/rag-resume-analyzer.git
cd rag-resume-analyzer
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign in with your Google account
3. Click "Get API Key"
4. Click "Create API Key in new project"
5. Copy your API key

## 🚀 How to Run

### Option 1: Run Locally with Streamlit
```bash
streamlit run resume_analyzer_app.py
```
Then:
1. Open http://localhost:8501 in your browser
2. Enter your Google Gemini API key in the sidebar
3. Paste your resume and job description
4. Click "Analyze Match" and get results!

### Option 2: Deploy to Streamlit Cloud (Free)
1. Push this repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy your repo
4. Add your API key as a secret in the app settings

## 💡 How It Works

### The RAG Pipeline:

```
Resume Input
    ↓
Text Chunking (1000 chars with 200 overlap)
    ↓
Vector Embeddings (Google Embedding Model)
    ↓
FAISS Vector Store
    ↓
Similarity Search (Job Description vs Resume)
    ↓
Retrieve Top 5 Relevant Sections
    ↓
RAG Chain with Gemini LLM
    ↓
Intelligent Analysis Output
```

### What Happens Behind the Scenes:

1. **Chunking**: Resume is split into 1000-character chunks with 200 character overlap
2. **Embeddings**: Each chunk converted to 768-dimensional vectors
3. **Vector Store**: FAISS indexes chunks for fast retrieval
4. **Query**: Job description is embedded and searched
5. **Retrieval**: Top 5 most relevant resume sections retrieved
6. **Generation**: Gemini analyzes retrieved sections against job requirements
7. **Output**: Detailed match score, skills gap, and recommendations

## 📊 Example Output

```
Match Score: 78%

Key Matching Skills:
- Python & Data Science
- Machine Learning
- SQL & Databases
- Team Leadership

Missing Skills:
- Apache Spark
- Advanced Cloud DevOps
- Kubernetes

Recommendations:
1. Highlight ML projects in resume
2. Learn Spark for big data jobs
3. Practice system design interviews
```

## 🎓 Learning Outcomes

By building this project, you'll learn:
- ✅ RAG architecture and implementation
- ✅ Vector embeddings and similarity search
- ✅ LangChain for LLM applications
- ✅ FAISS for vector databases
- ✅ Prompt engineering
- ✅ Streamlit deployment
- ✅ Google Gemini API usage

## 📈 Improvements & Extensions

Want to make it better? Try:
- Add file upload for PDF resumes
- Multi-language support
- Export results to PDF
- Track match history over time
- Batch analyze multiple jobs
- Custom scoring weights
- Integration with LinkedIn

## 🔒 Security Notes

- Your resume is NOT stored anywhere
- API calls are made directly to Google
- Your Gemini API key is only used in this session
- No data is collected or logged

## 📝 Example Usage

### Sample Resume:
```
John Doe
Senior Data Scientist
Python, SQL, Machine Learning, TensorFlow

Experience:
- Built ML models with 95% accuracy
- Led team of 5 data scientists
- Deployed models to production
```

### Sample Job Description:
```
Senior Data Scientist
Requirements:
- 5+ years ML experience
- Python & SQL expertise
- Leadership experience
- Big data tools (Spark, Hadoop)
```

### Analysis:
```
Match: 85%
Strengths: Python, ML, Leadership
Gaps: Big data tools, Spark knowledge
Action: Learn Spark, update resume with ML metrics
```

## 🐛 Troubleshooting

**Problem**: "Error importing native provider: Missing credentials"
- **Solution**: Make sure you entered your Gemini API key in the sidebar

**Problem**: "ModuleNotFoundError"
- **Solution**: Run `pip install -r requirements.txt` again

**Problem**: "Slow analysis"
- **Solution**: This is normal (5-10 seconds) as it's doing embeddings. Be patient!

**Problem**: "FAISS error"
- **Solution**: Try `pip install --upgrade faiss-cpu`

## 🤝 Contributing

Found a bug or want to improve? Great!
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📚 Resources

- [LangChain Documentation](https://docs.langchain.com)
- [Google Gemini API](https://ai.google.dev)
- [FAISS Guide](https://github.com/facebookresearch/faiss)
- [Streamlit Docs](https://docs.streamlit.io)
- [RAG Concepts](https://www.deeplearning.ai/short-courses/retrieval-augmented-generation/)

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

Built with:
- LangChain
- Google Gemini
- FAISS
- Streamlit

## 📞 Questions?

- Check the GitHub Issues
- Review the code comments
- Watch DeepLearning.AI RAG course

---

**Made with ❤️ for learning RAG and AI applications**

⭐ If this helps you, please star the repo!
