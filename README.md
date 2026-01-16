# Tools

A collection of Python utility scripts for productivity and automation.

## Scripts

### yt_analyzer.py
YouTube Transcript Analyzer - Fetches transcripts from YouTube videos and uses AI to summarize and extract key points.

**Features:**
- Extracts video ID from various YouTube URL formats
- Fetches transcripts via YouTube Transcript API
- Shows basic stats (word count, estimated duration)
- AI analysis via Gemini (optional, requires API key)
- Saves transcript to file

**Usage:**
```bash
python yt_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Setup:**
```bash
pip install youtube-transcript-api google-generativeai
export GEMINI_API_KEY="your_key_here"  # Optional, for AI analysis
```

## License
MIT

## Author
Jason ([@rice0649](https://github.com/rice0649))
