import os
from googleapiclient.discovery import build
import json
from datetime import datetime
import isodate as isodate

import datetime

from dotenv import load_dotenv

load_dotenv()


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
        service = build
        return service

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


class Video:
    load_dotenv()
    api_key: str = os.environ.get('YOUTUBE_KEY')

    def __init__(self, video_id, video_name="Default"):
        self.__video_id = video_id
        self.video_name = video_name

        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        self._init_from_api()

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=Video.api_key)
        return service

    def _init_from_api(self):
        video_response = self.get_service().videos().list(part='snippet,statistics',
                                                          id=self.__video_id
                                                          ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.__video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):  # переопределяем метод базового класса
        super().__init__(video_id)
        self.playlist = self.get_service().playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']

    def get_video_in_playlist(cls, video_id: str, playlist_id: str) -> dict:
        """Получает данные о видео в плейлисте"""
        video_in_playlist = cls.get_service().playlistItems().list(videoId=video_id,
                                                                   playlistId=playlist_id,
                                                                   part='snippet').execute()
        return video_in_playlist


class PlayList:

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        api_key: str = os.getenv('api_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.__playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.__playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                            maxResults=50).execute()
        self.title = self.__playlist['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        api_key: str = os.getenv('api_key')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        total_duration = datetime.timedelta()
        for video in response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        videos = {}
        likes = []

        for i in range(len(self.__playlist_videos)):
            videos[self.response['items'][i]['statistics']['likeCount']] = self.__playlist_videos[i]
            likes.append(self.response['items'][i]['statistics']['likeCount'])

        return likes, max(likes), max(videos)



video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1)
