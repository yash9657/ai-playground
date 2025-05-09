import tempfile
import streamlit as st
from embedchain import App # wraps OpenAI + a vector database so we can “chat” over text we feed in.
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Tuple
from datetime import datetime

# --- Sidebar ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=60)
st.sidebar.title("Chat with YouTube Video 📺")
st.sidebar.markdown("""
**Instructions:**
1. Enter your OpenAI API key.
2. Paste a YouTube video URL.
3. Ask any question about the video!

*Transcripts are fetched and embedded for each video. Responses may take a few seconds.*
""")

# --- API Key Input ---
openai_access_token = st.sidebar.text_input("OpenAI API Key", type="password")

# Helper building our chatbot
# db_path: folder where Chroma stores its vector database.
def embedchain_bot(db_path: str, api_key: str) -> App:
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

def extract_video_id(video_url: str) -> str:
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[-1].split("&")[0]
    elif "youtube.com/shorts/" in video_url:
        return video_url.split("/shorts/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

@st.cache_data(show_spinner=False)
def fetch_video_data(video_url: str) -> Tuple[str, str]:
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript]) # Joins all lines of the transcript into one giant string.
        return "Unknown", transcript_text  # Title is set to "Unknown" since we're not fetching it
    except Exception as e:
        return "Unknown", "No transcript available for this video."

# --- Main Layout ---
st.title("Chat with YouTube Video 📺")
st.caption("Chat with any YouTube video using OpenAI's GPT-4!")

if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token) # Builds our app (the embedchain chatbot) with your key and that folder.

    with st.container():
        st.subheader("Step 1: Enter YouTube Video URL")
        video_url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

        if video_url:
            with st.spinner("Fetching transcript and adding to knowledge base..."):
                title, transcript = fetch_video_data(video_url)
                if transcript != "No transcript available for this video.":
                    try:
                        app.add(transcript, data_type="text", metadata={"title": title, "url": video_url}) # Add that text into our embedchain knowledge base.
                        st.success(f"Added video '{title}' to knowledge base!")
                    except Exception as e:
                        st.error(f"Error adding video: {e}")
                else:
                    st.warning(f"No transcript available for video '{title}'. Cannot add to knowledge base.")

            # --- Chat Section ---
            st.subheader("Step 2: Ask a Question")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            prompt = st.text_input("Ask any question about the YouTube Video", key="chat_input")
            ask_button = st.button("Ask", use_container_width=True)

            if ask_button and prompt:
                with st.spinner("Thinking..."):
                    try:
                        answer = app.chat(prompt)
                        # app.chat converts your question into an embedding
                        # Queries the vector database for relevant chunks
                        # Runs GPT-4 over those questions + your question
                        st.session_state.chat_history.append({
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "question": prompt,
                            "answer": answer
                        })
                        st.write(answer)
                    except Exception as e:
                        st.error(f"Error chatting with the video: {e}")

            # --- Chat History ---
            if st.session_state.chat_history:
                st.markdown("---")
                st.subheader("Chat History")
                for entry in reversed(st.session_state.chat_history):
                    st.markdown(f"**[{entry['timestamp']}] You:** {entry['question']}")
                    st.markdown(f"**AI:** {entry['answer']}")
                    st.markdown("---")
else:
    st.info("Please enter your OpenAI API key in the sidebar to get started.")