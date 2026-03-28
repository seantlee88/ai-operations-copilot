# AI Operations Copilot

AI Operations Copilot is a Streamlit-based AI assistant that helps summarize business documents, extract action items and costs, and answer questions from uploaded documents such as estimates, reports, and employee handbooks.

## Features
- Upload TXT and PDF documents
- Document preview
- AI-generated summary
- Extract action items
- Extract costs and pricing details
- Ask questions about the document

## Tools Used
- Python
- Streamlit
- OpenAI API
- PyPDF

## How to Run
1. Install requirements:
   pip install -r requirements.txt

2. Add your OpenAI API key to `.streamlit/secrets.toml`:
   OPENAI_API_KEY = "your_api_key_here"

3. Run the app:
   streamlit run app.py