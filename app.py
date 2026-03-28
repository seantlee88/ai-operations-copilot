import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# ---------------------------------
# OpenAI client
# ---------------------------------
# Replace this with your NEW key after rotating the old one
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------------
# Page setup
# ---------------------------------
st.set_page_config(
    page_title="AI Operations Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("AI Operations Copilot")
st.write(
    "Upload a business document to summarize it, extract action items and costs, or ask questions about it."
)

# ---------------------------------
# File upload
# ---------------------------------
st.header("1. Upload a Document")
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

file_text = ""

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".txt"):
            file_text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)
            pdf_text_list = []

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pdf_text_list.append(page_text)

            file_text = "\n".join(pdf_text_list)

        st.header("2. Document Preview")
        st.text_area("Preview", file_text, height=300)

        if not file_text.strip():
            st.warning("The file uploaded successfully, but no readable text was found.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# ---------------------------------
# Action section
# ---------------------------------
st.header("3. Choose an Action")
question = st.text_input("Ask a question about the document")

col1, col2, col3, col4 = st.columns(4)

with col1:
    summarize_clicked = st.button("Summarize")

with col2:
    action_items_clicked = st.button("Extract Action Items")

with col3:
    costs_clicked = st.button("Extract Costs")

with col4:
    ask_question_clicked = st.button("Ask Question")


def run_openai_request(messages):
    """Helper function to send a request to OpenAI."""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )


# ---------------------------------
# Summarize
# ---------------------------------
if summarize_clicked:
    if file_text:
        try:
            with st.spinner("Thinking..."):
                response = run_openai_request([
                    {
                        "role": "system",
                        "content": "You are an operations assistant that summarizes business documents clearly for managers."
                    },
                    {
                        "role": "user",
                        "content": f"""
Summarize this business document in a clear and professional format.

Organize the summary into these sections if relevant:
- Overview
- Locations or properties
- Timelines or scheduling
- Costs or estimates
- Key assumptions or notes

Use bullet points and keep it easy to scan.

Document:
{file_text}
"""
                    }
                ])

            st.subheader("Summary")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
    else:
        st.warning("Please upload a document first.")

# ---------------------------------
# Extract Action Items
# ---------------------------------
if action_items_clicked:
    if file_text:
        try:
            with st.spinner("Thinking..."):
                response = run_openai_request([
                    {
                        "role": "system",
                        "content": "You extract action items from business documents for operations teams."
                    },
                    {
                        "role": "user",
                        "content": f"""
Extract all action items, tasks, follow-ups, and scheduling needs from this document.

Format the result as bullet points.
If possible, include:
- task
- related location or property
- timing or deadline

If no action items are found, say: No action items found.

Document:
{file_text}
"""
                    }
                ])

            st.subheader("Action Items")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error extracting action items: {e}")
    else:
        st.warning("Please upload a document first.")

# ---------------------------------
# Extract Costs
# ---------------------------------
if costs_clicked:
    if file_text:
        try:
            with st.spinner("Thinking..."):
                response = run_openai_request([
                    {
                        "role": "system",
                        "content": "You extract pricing and cost details from business documents."
                    },
                    {
                        "role": "user",
                        "content": f"""
Extract all pricing, costs, totals, and financial details from this document.

Organize the result into these sections if relevant:
- Recurring costs
- One-time costs
- Estimated totals
- Payment or rental details

Use bullet points.
If possible, group costs by location or property.
If no costs are found, say: No costs found.

Document:
{file_text}
"""
                    }
                ])

            st.subheader("Costs")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error extracting costs: {e}")
    else:
        st.warning("Please upload a document first.")

# ---------------------------------
# Ask Question
# ---------------------------------
if ask_question_clicked:
    if file_text and question:
        try:
            with st.spinner("Thinking..."):
                response = run_openai_request([
                    {
                        "role": "system",
                        "content": "You answer questions about uploaded business documents. Only use information found in the document. If the answer is not in the document, say you could not find it in the document."
                    },
                    {
                        "role": "user",
                        "content": f"""
Answer the question using only the document below.

Be concise, accurate, and professional.
If the document does not contain the answer, say: I could not find that in the document.

Document:
{file_text}

Question:
{question}
"""
                    }
                ])

            st.subheader("Answer")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error answering question: {e}")
    elif not file_text:
        st.warning("Please upload a document first.")
    else:
        st.warning("Please type a question first.")