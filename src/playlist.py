import datetime, isodate
from src.channel import Channel


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = Channel.get_service()
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)
                                                         ).execute()

    @property
    def title(self):
        return self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()["items"][0]["snippet"][
            "title"]

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        max_like = 0
        id_video = None
        for video in self.video_response['items']:
            like_count = int(video['statistics']['likeCount'])

            if like_count > max_like:
                max_like = like_count
                id_video = video['id']
        return f'https://youtu.be/{id_video}'
