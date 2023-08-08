An ultra simple subtitle downloader using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

NOTE: not production ready.

### Instructions
 - Spin up a Linux server.
 - Make sure everythings up to date: `sudo apt-get update`
 - Install pip: `sudo apt-get install python3-pip`
 - Install Flask: `pip3 install Flask`
 - Install [yt-dlp](https://github.com/yt-dlp/yt-dlp): `pip3 install yt-dlp`
 - Run the app: `python3 app.py`
 - Send a POST to `http://your-server-ip:8000/download_subtitles` that looks like `{ "url": "https://www.youtube.com/watch?v=EXAMPLE" }`
