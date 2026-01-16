#!/usr/bin/env python3
"""
YouTube Transcript Analyzer
Fetches transcript from a YouTube video and uses Gemini AI to summarize and extract key points.

Usage:
    python yt_analyzer.py <youtube_url>
    python yt_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID"

Setup:
    1. Get free API key from https://ai.google.dev
    2. Set environment variable: export GEMINI_API_KEY="your_key_here"
       Or edit this file and paste your key in the GEMINI_API_KEY variable below.
"""

import sys
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# ============================================
# PASTE YOUR GEMINI API KEY HERE (or use env var)
# ============================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# ============================================


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # Maybe it's just the video ID itself
    if re.match(r'^[0-9A-Za-z_-]{11}$', url):
        return url
    raise ValueError(f"Could not extract video ID from: {url}")


def get_transcript(video_id: str) -> str:
    """Fetch transcript from YouTube video."""
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id)
        # Combine all text segments
        full_transcript = " ".join([snippet.text for snippet in transcript_list])
        return full_transcript
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("No transcript found for this video.")


def analyze_with_gemini(transcript: str, api_key: str) -> str:
    """Use Gemini to summarize and extract key points."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""Analyze the following YouTube video transcript and provide:

1. **Summary** (2-3 paragraphs): What is this video about?

2. **Key Points** (bullet list): The main takeaways from the video

3. **Notable Quotes** (if any): Any particularly impactful or memorable statements

4. **Topics Covered** (tags): List the main topics/themes as tags

---

TRANSCRIPT:
{transcript[:30000]}  # Limit to avoid token limits
"""

    response = model.generate_content(prompt)
    return response.text


def basic_stats(transcript: str) -> dict:
    """Calculate basic statistics about the transcript."""
    words = transcript.split()
    return {
        "word_count": len(words),
        "char_count": len(transcript),
        "estimated_duration_minutes": len(words) // 150,  # ~150 words per minute
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python yt_analyzer.py <youtube_url>")
        print("Example: python yt_analyzer.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'")
        sys.exit(1)

    url = sys.argv[1]

    # Check for API key
    api_key = GEMINI_API_KEY
    if not api_key:
        print("=" * 60)
        print("WARNING: No Gemini API key found!")
        print("To enable AI analysis:")
        print("  1. Get free key from https://ai.google.dev")
        print("  2. Run: export GEMINI_API_KEY='your_key_here'")
        print("  3. Or edit this script and paste key in GEMINI_API_KEY")
        print("=" * 60)
        print("\nProceeding with transcript fetch only...\n")

    try:
        # Extract video ID
        print(f"Processing: {url}")
        video_id = extract_video_id(url)
        print(f"Video ID: {video_id}")

        # Get transcript
        print("Fetching transcript...")
        transcript = get_transcript(video_id)

        # Basic stats
        stats = basic_stats(transcript)
        print(f"\n{'=' * 60}")
        print("BASIC STATS")
        print(f"{'=' * 60}")
        print(f"Word count: {stats['word_count']:,}")
        print(f"Character count: {stats['char_count']:,}")
        print(f"Estimated duration: ~{stats['estimated_duration_minutes']} minutes")

        # AI Analysis (if API key available)
        if api_key:
            print(f"\n{'=' * 60}")
            print("AI ANALYSIS (Gemini)")
            print(f"{'=' * 60}")
            print("Analyzing with Gemini...")
            analysis = analyze_with_gemini(transcript, api_key)
            print(analysis)
        else:
            print(f"\n{'=' * 60}")
            print("RAW TRANSCRIPT (first 2000 chars)")
            print(f"{'=' * 60}")
            print(transcript[:2000] + "..." if len(transcript) > 2000 else transcript)

        # Save transcript to file
        output_file = f"transcript_{video_id}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Video ID: {video_id}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Word count: {stats['word_count']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(transcript)
        print(f"\nTranscript saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
