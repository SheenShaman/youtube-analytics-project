from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id):
        self.__video_id = video_id
        try:
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=video_id).execute()

            self.title = video_response['items'][0]['snippet']['title']
            self.url = 'https://youtu.be/' + self.__video_id
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                maxResults=50).execute()
