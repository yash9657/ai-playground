# Bring Your Own Browser (BYOB) for LLMs

## Overview
Large Language Models (LLMs) like GPT-4o have a knowledge cutoff date, which means they lack information about events that occurred after that point. In scenarios where the most recent data is essential, it's necessary to provide LLMs with access to current web information to ensure accurate and relevant responses.

**Bring Your Own Browser (BYOB)** is a Python tool that overcomes this limitation by integrating web search capabilities with an LLM. This enables the model to generate responses based on the latest information available online, such as the newest product launches or breaking news.

## Features
- **Up-to-date answers:** Combines web search with LLMs for current information
- **Retrieval-Augmented Generation (RAG):** Passes search results to the LLM for context-aware responses
- **Customizable:** Use any public search API (Google Custom Search API by default)

## How It Works
1. **Set Up a Search Engine:** Uses Google's Custom Search API to perform web searches and obtain a list of relevant results.
2. **Build a Search Dictionary:** Collects the title, URL, and a summary of each web page from the search results to create a structured dictionary of information.
3. **Generate a RAG Response:** Implements Retrieval-Augmented Generation (RAG) by passing the gathered information to the LLM, which then generates a final response to the user's query.

## Setup Instructions

### 1. Clone the Repository
```bash
cd byob
```

### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up API Keys
- Create a `.env` file in the `byob` directory with the following:
  ```
  GOOGLE_API_KEY=your_google_api_key
  GOOGLE_CSE_ID=your_custom_search_engine_id
  LLM_API_KEY=your_llm_api_key
  ```
- You can obtain a Google API key and Custom Search Engine ID from the [Google Custom Search documentation](https://developers.google.com/custom-search/v1/overview).

### 4. Run the Project
```bash
python byob.py
```

## Example Usage
- Ask any question and get an up-to-date answer, even about the latest events or product launches.

## License
MIT. Use and modify freely.
