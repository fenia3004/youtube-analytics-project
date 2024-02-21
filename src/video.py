import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    # создаем специальный объект для работы с API

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        try:
            self.video_id = video_id
            self.video_response = self.print_info()
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']
        except:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def __str__(self):
        return self.title

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',id=self.video_id).execute()
        return video_response


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API и наследованию."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
