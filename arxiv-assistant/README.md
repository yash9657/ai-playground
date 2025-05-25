# MCP: Conversational arXiv Research Assistant

This project provides a Jupyter notebook (`MCP.ipynb`) that implements a conversational research assistant for searching and summarizing arXiv papers. The assistant leverages Anthropic's Claude LLM to interpret user queries and call custom tools for paper search and information extraction.

## Features

- **arXiv Paper Search**: Search for relevant arXiv papers by topic and store their metadata (title, authors, summary, PDF URL, publication date) locally in organized JSON files.
- **Paper Information Extraction**: Retrieve detailed information about a specific paper (by arXiv ID) from the locally saved metadata.
- **Conversational Agent**: Interact with the assistant in natural language. The agent interprets queries, decides which tool to use, and returns results conversationally.
- **Extensible Tool Schema**: Tools are defined with clear input schemas and mapped to Python functions, making it easy to add new capabilities.

## How It Works

1. **User Query**: You enter a query (e.g., "Search for papers on LLM interpretability").
2. **LLM Interpretation**: Anthropic Claude interprets your query and determines which tool to use.
3. **Tool Execution**: The notebook executes the corresponding Python function (e.g., searching arXiv or extracting paper info).
4. **Conversational Response**: The assistant returns the results in a conversational format.

## Not an Official MCP Implementation

This project is **not** a direct implementation of Anthropic's Model Context Protocol (MCP). Instead, it is a custom, local tool-using agent inspired by the concept of LLM tool use. Tool invocation and mapping are handled within the notebook, and the official MCP API/protocol is not used.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <your-repo-url>
   cd <your-repo>/MCP
   ```

2. **Install Dependencies**

   Open the notebook and run the following cell (or install manually):

   ```python
   !pip install arxiv python-dotenv anthropic
   ```

3. **Set Up Anthropic API Key**

   - Obtain an API key from [Anthropic](https://www.anthropic.com/).
   - Set your API key in the notebook (e.g., using a `.env` file or directly in the code).

4. **Run the Notebook**

   Open `MCP.ipynb` in Jupyter or Colab and follow the instructions in the notebook cells.

## Usage Example

- **Search for Papers**:
  > Search for papers on "LLM interpretability"

- **Get Paper Summary**:
  > Give me a summary of this paper 2412.07992v3

- **Exit**:
  > quit

## Directory Structure

```
MCP/
├── MCP.ipynb         # Main notebook (conversational agent and tool logic)
├── README.md         # This file
└── papers/           # Saved paper metadata organized by topic
```

## License

This project is provided for educational and research purposes. Please check the terms of use for the Anthropic API and arXiv data.

## Acknowledgments

- [Anthropic Claude](https://www.anthropic.com/)
- [arxiv Python library](https://github.com/lukasschwab/arxiv.py) 