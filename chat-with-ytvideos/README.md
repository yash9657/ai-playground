# Chat with YouTube Video 📺

A professional Streamlit app that lets you chat with any YouTube video using OpenAI's GPT-4. Paste a YouTube video URL, and ask questions about its content—powered by automatic transcript extraction and Retrieval Augmented Generation (RAG).

---

## Features
- **Chat with YouTube videos:** Ask questions and get answers based on the video's transcript.
- **Automatic transcript extraction:** Fetches and processes the transcript for any YouTube video (if available).
- **Retrieval Augmented Generation (RAG):** Uses RAG to provide accurate, context-aware answers by combining retrieval from the video transcript with the power of GPT-4.
- **OpenAI GPT-4 integration:** Uses the latest LLM for high-quality answers.
- **Chat history:** See your previous questions and answers.
- **Professional UI:** Clean, step-by-step interface with progress indicators and error handling.

---

## What is Retrieval Augmented Generation (RAG)?
Retrieval Augmented Generation (RAG) is a technique that combines information retrieval with large language models (LLMs) to provide more accurate and contextually relevant answers. Instead of relying solely on the LLM's internal knowledge, RAG retrieves relevant pieces of information ("contexts") from an external source—in this case, the transcript of the YouTube video—and feeds them to the LLM to ground its responses.

**How RAG works in this app:**
- When you ask a question, the app searches the transcript for the most relevant sections.
- These sections are provided as context to GPT-4, which then generates an answer based on both the retrieved transcript and your question.
- This approach ensures that answers are accurate and specific to the content of the video, even if the LLM itself doesn't "know" the video.

---

## How It Works
1. **Transcript Extraction:**
   - You provide a YouTube video URL.
   - The app fetches the transcript using the YouTube Transcript API.
2. **Embedding & Knowledge Base:**
   - The transcript is embedded and stored in a temporary vector database.
3. **Chatting with RAG:**
   - You ask questions about the video.
   - The app retrieves relevant transcript sections using vector search (RAG) and uses OpenAI's GPT-4 to answer your question, grounded in the actual video content.

---

## Installation & Usage

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd chat-with-ytvideos
```

### 2. Install Dependencies
It's recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get an OpenAI API Key
- Sign up at [OpenAI](https://platform.openai.com/) and create an API key.

### 4. Run the App
```bash
streamlit run chat_youtube.py
```

### 5. Use the App
- Enter your OpenAI API key in the sidebar.
- Paste a YouTube video URL.
- Ask any question about the video!

---

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies.

---

## Notes
- The app only works with videos that have transcripts available.
- Your API key is never stored.
- All data is processed temporarily and is deleted after the session.

---

## License
MIT License 