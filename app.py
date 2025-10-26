import streamlit as st
import csv
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rapidfuzz import fuzz
import time
import tempfile
import PyPDF2  # For PDF document parsing; pip install PyPDF2

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
    words = word_tokenize(text.lower())
    filtered_words = [w for w in words if w.isalnum() and w not in stopwords.words('english')]
    return filtered_words

# Header with logo and name
col1, col2 = st.columns([0.7, 4.8])

with col1:
    st.image('tatva_logo1.jpg', width=80)

with col2:
    st.markdown("""
    <div style="
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        color: #4B0082; 
        font-weight: bold; 
        font-size: 65px; 
        line-height: 1;
    ">
        TatvaAI
    </div>
    """, unsafe_allow_html=True)

# Intro text
st.markdown("""
<h3 style="color: #6A5ACD; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    Empowering Your Journey with Tatva-तत्त्व — the essence of truth and wisdom
</h3>
<p style="font-size:16px; font-family: Arial, sans-serif; color:#9370DB;">
    Welcome to TatvaAI, where ancient wisdom meets modern AI. Ask any career-related question and receive detailed, insightful answers built upon the foundations of knowledge and truth.
</p>
<hr>
""", unsafe_allow_html=True)

# Document upload feature
st.markdown("### Upload a PDF document for reference")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
document_text = ""

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    # Extract text from PDF
    with open(tmp_file_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        text_pages = []
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            text_pages.append(page.extract_text())
        document_text = "\n".join(text_pages)
    st.success("Document uploaded and text extracted successfully.")
else:
    st.info("No document uploaded yet.")

csv_file = "faq.csv"
qa_pairs = {}
domains = set()

if os.path.exists(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keyword = row['keyword'].strip().lower()
            domain = row['domain'].strip() if 'domain' in row else ""
            answer = row['answer'].strip()
            qa_pairs[keyword] = (answer, domain)
            if domain:
                domains.add(domain)
else:
    st.error(f"FAQ file '{csv_file}' not found. Please place it in the project folder.")
    st.stop()

domain_list = ["All"] + sorted(domains)
selected_domain = st.selectbox("Choose career domain:", domain_list)
example_questions = [
    "What is machine learning?",
    "How to get internships in automation?",
    "What skills needed for robotics?"
]

st.markdown("#### Try clicking an example question:")
for question in example_questions:
    if st.button(question):
        st.session_state['input'] = question

# User input field
user_input = st.text_input("Type your question:", value=st.session_state.get('input', ''))

def simple_chatbot(question, selected_domain):
    question = question.lower()
    best_match = ""
    highest_score = 0

    # Simulate typing indicator
    with st.spinner("TatvaAI is typing..."):
        time.sleep(1)

    # Match in FAQ CSV
    for keyword, (answer, domain) in qa_pairs.items():
        if selected_domain != "All" and domain != selected_domain:
            continue
        score = fuzz.token_set_ratio(keyword, question)
        if score > highest_score and score > 60:
            best_match = keyword
            highest_score = score

    if best_match:
        return qa_pairs[best_match][0]

    # Search uploaded document text as fallback
    if document_text:
        if all(word in document_text.lower() for word in preprocess(question)):
            return "Answer might be in the uploaded document. Please refer to it."
        else:
            return "No matching info found in the FAQ or uploaded document."

    return "Sorry, I don’t know the answer yet. Please try another question."

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'feedback' not in st.session_state:
    st.session_state['feedback'] = {}

if 'analytics' not in st.session_state:
    st.session_state['analytics'] = {"questions_asked": 0, "positive_feedback": 0, "negative_feedback": 0}

if user_input:
    answer = simple_chatbot(user_input, selected_domain)
    st.session_state['chat_history'].append(("You", user_input))
    st.session_state['chat_history'].append(("TatvaAI", answer))
    st.session_state['analytics']['questions_asked'] += 1

for i, (sender, msg) in enumerate(st.session_state['chat_history']):
    if sender == "You":
        st.markdown(f"""
            <div style="
                background-color:#222244; padding:12px 16px; border-radius:18px 18px 6px 18px;
                margin:10px 0 10px 120px; text-align:right; color:#e0e0e0; font-size:16px; max-width:70%;
                float:right; clear:both;">
                <b>{sender}:</b> {msg}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="
                background-color:#471a63; padding:12px 16px; border-radius:18px 18px 18px 6px;
                margin:10px 120px 10px 0; color:#fff; font-size:16px; max-width:70%;
                float:left; clear:both;">
                <b>{sender}:</b> {msg}
            </div>""", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍", key=f"{i}_like"):
                st.session_state['feedback'][i] = 'like'
                st.session_state['analytics']['positive_feedback'] += 1
        with col2:
            if st.button("👎", key=f"{i}_dislike"):
                st.session_state['feedback'][i] = 'dislike'
                st.session_state['analytics']['negative_feedback'] += 1

st.markdown("---")
st.markdown("### Analytics Summary")
st.markdown(f"Total questions asked: {st.session_state['analytics']['questions_asked']}")
st.markdown(f"Positive feedbacks: {st.session_state['analytics']['positive_feedback']}")
st.markdown(f"Negative feedbacks: {st.session_state['analytics']['negative_feedback']}")

# Export chat history button
if st.button("Export Chat as Text"):
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        for sender, msg in st.session_state['chat_history']:
            f.write(f"{sender}: {msg}\n")
    st.success("Chat history exported successfully as 'chat_history.txt'")



