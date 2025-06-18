# YouTube Downloader Web App

A simple web application that allows downloading YouTube videos as MP4 (video) or MP3 (audio) using **Flask** and **yt-dlp**.

## How does it work?

1. Enter a YouTube video URL.
2. Choose the desired format: MP4 or MP3.
3. The app downloads the video with yt-dlp.
4. Converts the downloaded file to the chosen format using FFmpeg.
5. Deletes the original downloaded file after conversion.

## Requirements

- Python 3.X
- Flask
- yt-dlp

FFmpeg is included inside the project directory at `ffmpeg/bin/ffmpeg.exe`, so no need to add FFmpeg to your system PATH.

## Usage

1. Clone the repository.
2. Install the required Python packages:
   ```bash
   pip install flask yt-dlp
3. Start the program
