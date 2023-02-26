import os
from googleapiclient.discovery import build
import json

from dotenv import load_dotenv


class Youtube:
    def __init__(self, channel_id):
        self.__channel_id = channel_id
        load_dotenv()
        api_key: str = os.environ.get('YOUTUBE_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + self.__channel_id
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']
        data = self.title + self.description + self.url + self.subscriber_count + self.video_count + self.view_count
    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_KEY'))
        return service

    def json_file(self, data, filename='channel.json'):
        """добавляет инфу о канале,хранящуюся в атрибутах, в json file"""
        with open(filename, 'r') as file:
            file_data = json.load(file)
            file_data.append(data)
            return json.dump(file_data, file, indent=4)



    def print_info(self):
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))


y = Youtube("UCMCgOm8GZkHp8zJ6l7_hIuA")
