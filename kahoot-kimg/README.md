# Kahoot OCR Bot

![Kahoot Example](kahoot.png)

## Overview

This project is a Python automation tool that uses OCR (Optical Character Recognition) and AI to automatically read Kahoot quiz questions and answer options from your screen, and (optionally) select the correct answer using OpenAI's GPT model.

- **Cross-platform**: Works on macOS, Windows, and Linux.
- **Universal**: No hardcoded coordinates—uses a region recorder for any screen size or layout.
- **Automated**: Extracts question/options and can auto-click the correct answer.

## How It Works

1. **Region Setup**: On first use, run the region recorder script. Hover over each question/answer box corner and press a hotkey to save their positions.
2. **OCR Extraction**: When you trigger the main script, it screenshots the defined regions, extracts text using Tesseract OCR, and formats the question/options.
3. **AI Answering**: The extracted text is sent to OpenAI's GPT model, which returns the most likely correct answer.
4. **Auto-Click**: The script can automatically click the correct answer on your screen.

## Setup Instructions

### 1. Clone the Repository
```bash
cd kahoot-kimg
```

### 2. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Tesseract OCR
- **macOS**: `brew install tesseract`
- **Windows**: [Download installer](https://github.com/tesseract-ocr/tesseract)
- **Linux**: `sudo apt-get install tesseract-ocr`

### 4. Set Up OpenAI API Key
- Create a `.env` file in `kahoot-kimg` with:
  ```
  OPENAI_API_KEY=sk-...
  ```

### 5. Record Screen Regions
Run the region recorder script (see `region_recorder.py`):
```bash
python region_recorder.py
```
Follow the prompts to hover and press the hotkey for each region. This creates `kahoot_regions.json`.

### 6. Run the Main Script
```bash
python kahoot_ocr.py
```
- Use the hotkey (e.g., Ctrl+Space) to trigger OCR and answer extraction.

## Usage Notes
- Make sure your Kahoot window is visible and not obstructed.
- The script will print the extracted question, options, and the selected answer.
- You can customize the hotkey in the script if needed.

## Example
![Kahoot Example](kahoot.png)

## License
MIT. Use and modify freely. 