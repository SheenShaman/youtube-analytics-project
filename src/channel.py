import os
import json
from googleapiclient.discovery import build

API_KEY: str = os.getenv('YouTube_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.youtube = build('youtube', 'v3', developerKey=API_KEY)
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        print(youtube)

    def to_json(self, new_file):
        values = {'channel_id': self.channel_id,
                  'title': self.title,
                  'description': self.description,
                  'url': self.url,
                  'subscriber_count': self.subscriber_count,
                  'video_count': self.video_count,
                  'view_count': self.view_count}
        with open(new_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(values))
