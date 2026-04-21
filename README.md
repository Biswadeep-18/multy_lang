# Translate.AI - Advanced Multi-Language Engine

An enterprise-grade platform for high-fidelity translation, grammar refinement, and professional content drafting, powered by LangGraph and state-of-the-art LLMs (Gemini & Groq).

## 🚀 Features

- **Standard Translate**: Advanced translation with automatic language detection.
- **Enterprise Draft**: Professional content generation based on requirements.
- **Grammar & Tone Intelligence**: Native-level refinement and structured feedback.
- **Document Intelligence**: Upload PDFs/Images for instant text extraction and processing.
- **Structured Swagger API**: Fully documented REST API for seamless integration.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.11 or higher.
- `uv` package manager (recommended) or `pip`.

### 2. Environment Configuration
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Installation
Using `uv`:
```bash
uv sync
```
Using `pip`:
```bash
pip install -r requirements.txt
```
*(Note: If you don't have a requirements.txt, you can install the main dependencies: `fastapi uvicorn streamlit langchain langchain-google-genai langchain-groq langgraph python-dotenv`)*

---

## 🚦 How to Run

To run the full application, you need to start **both** the Backend and the Frontend in separate terminals.

### Step 1: Start the Backend (FastAPI)
The backend handles the AI logic, LangGraph workflows, and provides the Swagger API.

```bash
# From the root directory
python backend/main.py
```
- **API URL**: `http://localhost:8000`
- **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Documentation (Redoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Step 2: Start the Frontend (Streamlit)
The frontend provides the interactive user interface.

```bash
# From the root directory
streamlit run app.py
```
- **Local URL**: `http://localhost:8501`

---

## 🔌 API Documentation (Swagger)

The backend is structured with a professional Swagger UI. You can access it at `/docs` to:
- **Test Endpoints**: Send requests directly from the browser.
- **View Schemas**: Understand the input/output models.
- **Grouped Categories**:
    - **System**: Health checks (`/`) and configuration (`/languages`).
    - **AI Processing**: Unified processing (`/process`) and specific task endpoints (`/process/translate`, `/process/grammar`, `/process/draft`).

---

## 📂 Project Structure

- `backend/main.py`: FastAPI entry point with Swagger definitions.
- `app.py`: Streamlit main dashboard.
- `core/`: Core logic including LangGraph workflows (`graph.py`), state management (`state.py`), and vision processing (`vision.py`).
- `agents/`: Individual AI agent nodes for the Graph.
- `styles/`: Custom CSS for the premium UI.
