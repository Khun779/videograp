import yt_dlp
import os

def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mkv',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            extension = 'mkv'
            video_path = os.path.join(output_path, f"{video_title}.{extension}")
            return video_path
    except Exception as e:
        raise e