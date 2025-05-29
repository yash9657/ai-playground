# MCP Research Assistant

A modular research assistant that lets you search for and extract information about arXiv research papers using natural language, powered by FastMCP and Anthropic's Claude LLM.

## Overview

This project demonstrates how to expose custom research tools (for searching and extracting arXiv paper info) via a FastMCP server, and interact with them using a conversational chatbot client. The chatbot uses Anthropic's Claude LLM to interpret user queries and call the tools as needed.

**Key Features:**
- **Search arXiv papers** by topic and save their metadata.
- **Extract detailed info** about a specific paper by its arXiv ID.
- **Conversational interface**: Ask questions in natural language.
- **Modular**: Easily extend with new tools or models.

## Project Structure

```
mcp_project/
├── research_server.py      # FastMCP server exposing research tools
├── mcp_chatbot.py         # Chatbot client using Claude LLM and FastMCP tools
├── main.py                # (Demo placeholder)
├── pyproject.toml         # Project dependencies
├── papers/                # Saved paper info, organized by topic
│   ├── computer_science/
│   │   └── papers_info.json
│   ├── physics/
│   │   └── papers_info.json
│   └── ...
└── README.md              # This file
```

## How It Works

### 1. FastMCP Server (`research_server.py`)
- Exposes two tools:
  - `search_papers(topic, max_results=5)`: Searches arXiv for papers on a topic, saves their info in `papers/<topic>/papers_info.json`, and returns a list of paper IDs.
  - `extract_info(paper_id)`: Looks up detailed info for a paper ID across all saved topics.
- Runs as a FastMCP server using `mcp.run(transport='stdio')`.

### 2. Chatbot Client (`mcp_chatbot.py`)
- Connects to the FastMCP server as a client.
- Uses Anthropic's Claude LLM to interpret user queries and decide when to call the tools.
- Presents results in a conversational loop.

## Setup Instructions

### 1. Install Dependencies

Make sure you have [uv](https://github.com/astral-sh/uv) installed (for fast Python dependency management):

```bash
pip install uv
```

Then, from the `mcp_project` directory, install dependencies:

```bash
uv pip install -r requirements.txt  # if requirements.txt exists
# or, using pyproject.toml:
uv pip install
```

### 2. Set Up API Keys

- **Anthropic Claude API**: Set your API key as an environment variable or in a `.env` file:

  - In your shell:
    ```bash
    export ANTHROPIC_API_KEY="sk-ant-..."
    ```
  - Or in `.env` (in the same directory):
    ```
    ANTHROPIC_API_KEY=sk-ant-...
    ```

### 3. Run the Server and Chatbot

From the `mcp_project` directory:

```bash
uv run mcp_chatbot.py
```

This will:
- Start the FastMCP server (via stdio subprocess)
- Connect the chatbot client
- Enter an interactive chat loop

## Example Usage

### Search for Papers
```
Query: Search for papers on "computer science"
```
**Output:**
```
I'll search for papers on computer science for you. Let me retrieve that information.
Calling tool search_papers with args {'topic': 'computer science', 'max_results': 5}
Results are saved in: papers/computer_science/papers_info.json
I've found 5 papers related to computer science. Here are the paper IDs:
1. 1802.03292v1
2. 1501.05039v1
...
Would you like me to extract more detailed information about any of these specific papers? If so, please let me know which paper ID you're interested in.
```

### Extract Paper Info
```
Query: Give me a summary of this paper 1802.03292v1
```
**Output:**
```
Calling tool extract_info with args {'paper_id': '1802.03292v1'}
# Summary of "Mathematical Logic in Computer Science"
- **Title**: Mathematical Logic in Computer Science
- **Authors**: Assaf Kfoury
- **Published**: 2018-02-07
- **arXiv ID**: 1802.03292v1
- **Summary**: The article retraces major events and milestones in the mutual influences between mathematical logic and computer science since the 1950s.
- **PDF**: http://arxiv.org/pdf/1802.03292v1
```

## How the Components Work Together

- The **server** (`research_server.py`) exposes research tools via FastMCP.
- The **chatbot** (`mcp_chatbot.py`) connects to the server, lists available tools, and uses Claude LLM to interpret user queries and call the right tool.
- Paper info is saved in the `papers/` directory, organized by topic, and can be retrieved by paper ID.

## Extending the Project
- Add new tools to `research_server.py` using the `@mcp.tool()` decorator.
- The chatbot will automatically detect and expose new tools to the LLM.

## Troubleshooting
- **API Key errors**: Make sure your Anthropic API key is set in your environment or `.env` file.
- **Dependency issues**: Ensure you installed all dependencies with `uv pip install`.
- **Git issues**: If you have trouble pushing or pulling, make sure to resolve merge conflicts and finish merge commits as described in the earlier Q&A.

## License
MIT
