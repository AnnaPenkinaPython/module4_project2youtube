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

    def json_file(self, data, filename='channel.json'):
        """добавляет инфу о канале,хранящуюся в атрибутах, в json file"""
        with open(filename, 'r') as file:
            file_data = json.load(file)
            file_data.append(data)
            return json.dump(file_data, file, indent=4, ensure_ascii=False)

    def print_info(self):
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    def __str__(self):
        return f'Youtube-channel: {self.title}'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count > other.subscriber_count


class Video(Youtube):
    def __init__(self, channel_id, video_name, view_count, like_count):  # переопределяем метод базового класса
        super().__init__(channel_id)
        self.video_name = video_name
        self.view_count = view_count
        self.like_count = like_count


class PLVideo(Video):
    def __init__(self, channel_id, video_name, view_count, like_count, video_id,
                 playlist_id, playlist_name):  # переопределяем метод базового класса
        super().__init__(channel_id, video_name, view_count, like_count)
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name

video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1)