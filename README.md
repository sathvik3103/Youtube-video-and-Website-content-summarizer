# Content Summarizer

A Streamlit application that generates summaries from YouTube videos and website content using Groq's language models.

## Features

- Summarizes content from:
  - YouTube videos (including transcripts)
  - General websites
- Powered by Groq's Gemma-7b-It model
- User-friendly interface
- URL validation
- Detailed error handling

## Installation

```bash
pip install -r requirements.txt
```

## Required Dependencies

- streamlit
- langchain-groq
- validators
- langchain-community
- unstructured

## Usage

1. Launch the application:
```bash
streamlit run app.py
```

2. Enter your Groq API key in the sidebar
3. Paste a valid URL (YouTube video or website)
4. Click "Summarize" to generate a concise summary

## Features Breakdown

**Input Handling**
- URL validation
- API key verification
- Support for multiple content types

**Content Processing**
- YouTube transcript extraction
- Website content parsing
- Maximum 500-word summaries

**Error Handling**
- Invalid URL detection
- Empty content validation
- Transcript availability checking
- Comprehensive exception handling

## Project Structure

```plaintext
.
├── app.py
├── requirements.txt
└── README.md
```

## Configuration

The application uses:
- Groq's Gemma-7b-It model
- Custom prompt templates
- Mozilla user agent for web scraping
- SSL verification bypass for certain websites

## Limitations

- Requires valid Groq API key
- YouTube videos must have available transcripts
- Websites must be accessible and contain readable content

