import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    # создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.print_info()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/" + self.channel["items"][0]["id"]
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self) -> str:
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    def __dict_to_json(self):
        """Функция заполняющая словарь
        """

        result = {}

        for key, value in self.__dict__.items():
            if not isinstance(value, (list, dict)):
                result[key] = value

        return result

    def to_json(self, name_file):
        """

        Args:
            name_file (src): путь к по которому будет создан json файл
        """

        with open(name_file, 'w', encoding='utf-8') as f:
            json.dump([self.__dict_to_json()], f, ensure_ascii=False, indent=2)