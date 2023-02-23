import os
from googleapiclient.discovery import build
import json

from dotenv import load_dotenv


class Youtube:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        load_dotenv()
        api_key: str = os.environ.get('YOUTUBE_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self):
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

y = Youtube("UCMCgOm8GZkHp8zJ6l7_hIuA")
y.print_info()