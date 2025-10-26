# TatvaAI Chatbot

TatvaAI is an advanced Streamlit chatbot designed to provide comprehensive career guidance by answering queries using a FAQ database and user-uploaded PDF documents. This project combines modern UI/UX design, intelligent keyword matching, document integration, user feedback, analytics, and chat export features for an immersive and insightful experience.

---

## Features

- **User Interface & Experience**
  - Custom logo and branding with clean, intuitive layout
  - Responsive design with aligned logo and project title
  - Styled chat bubbles differentiating user and bot messages
  - Real-time typing animation enhances realism

- **Chatbot Intelligence**
  - Keyword-based FAQ answering powered by rapidfuzz fuzzy matching
  - Domain/category filtering for tailored responses
  - Convenient clickable example questions for quick testing

- **Document Upload & Integration**
  - Upload PDF documents as additional knowledge base
  - Text extraction from PDFs using PyPDF2
  - Bot searches uploaded documents for relevant answers when FAQ lacks response

- **Chat History & Export**
  - Persistent session chat history display
  - Export entire chat conversation to a `.txt` file with one click

- **Feedback & Analytics**
  - Positive (👍) and negative (👎) feedback buttons per response
  - Analytics dashboard tracks total questions, likes, and dislikes
  - Real-time feedback integrated to inform bot improvement

- **Extensibility**
  - Modular code structure facilitates easy feature additions or API integrations
  - Ready for future voice input, multilingual support, and multimedia responses

- **Documentation & Demonstration**
  - Detailed README and usage instructions included
  - Screenshots and video demo embed capabilities supported
  - Fully managed dependencies listed in `requirements.txt`

---
Clone repository
git clone https://github.com/adithyaanilbhat/tatvaai.git
cd tatvaai-chatbot

Install dependencies
pip install -r requirements.txt

Run app
streamlit run app.py

Ensure `faq.csv` and logo images are in the root folder.

---

## Project Structure

app.py # Main application script
faq.csv # FAQ dataset CSV file
tatva_logo1.jpg # Logo image
requirements.txt # Python dependencies
README.md # Project documentation
/screenshots # Demo screenshots and assets
chat_history.txt # Exported chat logs

---

## Screenshots

Add example UI screenshots here:

- `chat_history_export.png`
- `Positive and Negative Feedback.png`

---

## Demo Video

Camera taken Videos
This larger README provides a detailed, clear, and professional presentation of your project’s features, usage, and structure with appropriate Markdown formatting for great GitHub display.



## Getting Started

