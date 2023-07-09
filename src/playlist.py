import datetime
from src.channel import Channel


class PlayList(Channel):
    """
    Получает данные по видеороликам в плейлисте
    """
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.title = str(self.get_playlist_videos()['items'][0]['snippet']['title'].split('.')[0])
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

    @property
    def playlist_id(self):
        return self.__playlist_id

    def get_playlist_videos(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                                  maxResults=50,).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails',
                                                          id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """
        Возвращает суммарную длительность плейлиста
        """
        sum_duration = datetime.timedelta(minutes=0, seconds=0)
        for video in self.get_playlist_videos()['items']:
            duration = video['contentDetails']['duration']
            try:
                seconds = int(duration[2:duration.index('M')]) * 60 + int(duration[duration.index('M') + 1:-1])
                delta = datetime.timedelta(seconds=seconds)
                sum_duration += delta
            except ValueError:
                seconds = int(duration[2:duration.index('M')]) * 60
                delta = datetime.timedelta(seconds=seconds)
                sum_duration += delta

        return sum_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное(по лайкам) видео из плейлиста
        """
        max_likes = 0
        for video in self.get_playlist_videos()['items']:
            if int(video["statistics"]["likeCount"]) > int(max_likes):
                max_likes = video["statistics"]["likeCount"]
        return f"https://youtu.be/{video['id']}"

