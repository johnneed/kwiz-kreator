import json
import queue
from dataclasses import dataclass
from enum import Enum  # for enum34, or the stdlib version

from src.modules.decorators import debounce

_default_max_recent_files = 9
_default_default_question_count = 5
_default_publish_days = {5}
_default_publish_hour = 0
_default_window_width = 853
_default_window_height = 830
_default_window_mode = "MAXIMIZED"
_default_splitter_position = [0, 1]


class WindowModes(Enum):
    WINDOWED = 1
    MAXIMIZED = 2
    FULLSCREEN = 3


class WindowPreferences(Enum):
    HEIGHT = "height"
    WIDTH = "width"
    WINDOW_MODE = "window_mode"
    SPLITTER_POSITION = "splitter_position"


@dataclass
class FtpConfig:
    host: str
    username: str
    password: str
    remote_path: str
    port: int

    def to_dict(self):
        return {"host": self.host,
                "username": self.username,
                "password": self.password,
                "remote_path": self.remote_path,
                "port": self.port
                }

    @staticmethod
    def from_dict(config: dict):
        print(f"from_dict {config}")
        return FtpConfig(host=config.get("host", ""),
                         username=config.get("username", ""),
                         password=config.get("password", ""),
                         remote_path=config.get("remote_path", ""),
                         port=config.get("port", 21)
                         )

    def __str__(self):
        return f'FtpConfig host: {self.host} - username: {self.username} - password: {self.password} - remote_path: {self.remote_path} - port: {self.port}'

    def __repr__(self):
        return f'FtpConfig host: {self.host} - username: {self.username} - password: {self.password} - remote_path: {self.remote_path} - port: {self.port}'


@dataclass
class Preferences:
    ftp_config: FtpConfig
    publish_days: list[int]
    publish_hour: int
    default_question_count: int

    def to_dict(self):
        return {
            "publish_days": self.publish_days,
            "publish_hour": self.publish_hour,
            "default_question_count": self.default_question_count,
            "ftp_config": self.ftp_config.to_dict()
        }



    @staticmethod
    def from_dict(config):
        return Preferences(ftp_config=FtpConfig.from_dict(config.get("ftp_config", {})),
                           publish_days=config.get("publish_days", _default_publish_days),
                           publish_hour=config.get("publish_hour", _default_publish_hour),
                           default_question_count=config.get("default_question_count", _default_default_question_count)
                           )


class AppConfig(object):
    _publish_days: set[int]
    _publish_hour: int
    _default_question_count: int
    _window_width: int
    _window_height: int
    _window_mode: WindowModes
    _ftp_config: FtpConfig
    _max_recent_files: int
    _splitter_position: list[int]
    window_modes = WindowModes
    window_preferences = WindowPreferences

    def __init__(self, app_config_file_name: str):
        self._message_queue = queue.Queue()
        self._subscribers = []
        self._recent_files = []
        self._publish_days = _default_publish_days
        self._publish_hour = _default_publish_hour
        self._default_question_count = _default_default_question_count
        self._window_width = _default_window_width
        self._window_height = _default_window_height
        self._window_mode = WindowModes[_default_window_mode]
        self._splitter_position = _default_splitter_position
        self._file_name = app_config_file_name
        self._ftp_config = FtpConfig.from_dict({})
        self.__load()

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def publish(self, message):
        self._message_queue.put(message)
        for subscriber in self._subscribers:
            subscriber.receive(message)

    @property
    def publish_days(self):
        return self._publish_days

    @publish_days.setter
    def publish_days(self, value: set[int]):
        if value != self._publish_days:
            self._publish_days = set([x for x in value if 8 > x >= 0])
            self.publish("app_config_publish_days_changed")
            self.__save()

    @property
    def publish_hour(self):
        return self._publish_hour

    @publish_hour.setter
    def publish_hour(self, value: int):
        if 24 > value >= 0 and value != self._publish_hour:
            self._publish_hour = value
            self.publish("app_config_publish_hour_changed")
            self.__save()

    @property
    def default_question_count(self):
        return self._default_question_count

    @default_question_count.setter
    def default_question_count(self, value: int):
        if value > 0 and value != self._default_question_count:
            self._default_question_count = value
            self.publish("app_config_default_question_count_changed")
            self.__save()

    @property
    def window_width(self):
        return self._window_width

    @window_width.setter
    @debounce(5)
    def window_width(self, value: int):
        if value > 0 and value != self._window_width:
            self._window_width = value
            self.publish("app_config_window_width_changed")
            self.__save()

    @property
    def window_height(self):
        return self._window_height

    @window_height.setter
    @debounce(5)
    def window_height(self, value: int):
        if value > 0 and value != self._window_height:
            self._window_height = value
            self.publish("app_config_window_height_changed")
            self.__save()

    @property
    def window_mode(self):
        return self._window_mode

    @window_mode.setter
    @debounce(5)
    def window_mode(self, value: WindowModes):
        if (value in WindowModes) and (value != self._window_mode):
            self._window_mode = value
            self.publish("app_config_window_mode_changed")
            self.__save()

    @property
    def splitter_position(self):
        return self._splitter_position

    @splitter_position.setter
    @debounce(5)
    def splitter_position(self, value: list[int]):
        if value != self._splitter_position:
            self._splitter_position = value
            self.__save()

    @property
    def ftp_config(self):
        return self._ftp_config

    @ftp_config.setter
    def ftp_config(self, config):
        self._ftp_config = FtpConfig.from_dict(config)
        self.publish("app_config_ftp_config_changed")
        self.__save()

    def get_recent_files(self):
        return self._recent_files

    def get_recent_file_name(self, index: int):
        return self._recent_files[index] if index < len(self._recent_files) else None

    def remove_recent_file(self, file_name: str):
        if file_name in self._recent_files:
            self._recent_files.remove(file_name)
            self.publish('recent_files_changed')
            self.__save()

    def __load(self):
        try:
            with open(self._file_name) as json_file:
                config = json.load(json_file)
                self._recent_files = config.get("recent_files", [])
                self._publish_days = set(config.get("publish_days", _default_publish_days))
                self._publish_hour = config.get("publish_hour", _default_publish_hour)
                self._default_question_count = config.get("default_question_count", _default_default_question_count)
                self._window_width = config.get("window_width", _default_window_width)
                self._window_height = config.get("window_height", _default_window_height)
                self._window_mode = WindowModes[config.get("window_mode", _default_window_mode)]
                self._splitter_position = config.get("splitter_position", _default_splitter_position)
                self._ftp_config = FtpConfig.from_dict(config.get("ftp_config", {}))
                self._max_recent_files = config.get("max_recent_files", _default_max_recent_files)
        except Exception as e:
            print(e)
            self._recent_files = []
        self.publish('app_config_loaded')

    def save_window_preference(self, key: WindowPreferences, *args):
        print(f"save_window_preference {key} {args}")
        if key == WindowPreferences.HEIGHT:
            self.window_height = int(args[0])
        elif key == WindowPreferences.WIDTH:
            self.window_width = int(args[0])
        elif key == WindowPreferences.WINDOW_MODE:
            self.window_mode = WindowModes[args[0]]
        elif key == WindowPreferences.SPLITTER_POSITION:
            self.splitter_position = args[0]

    def save_preferences(self, preferences: Preferences):
        self._ftp_config = preferences.ftp_config
        self._publish_days = set(preferences.publish_days)
        self._publish_hour = preferences.publish_hour
        self._default_question_count = preferences.default_question_count
        self.__save()

    def __save(self):
        print("SAVING APP CONFIG")
        try:
            with open(self._file_name, 'w') as outfile:
                json.dump(self.to_dict(), outfile)
                outfile.close()
        except Exception as e:
            print(e)

    def add_recent_file(self, file_name: str):
        if file_name in self._recent_files:
            self._recent_files.remove(file_name)
        self._recent_files.insert(0, file_name)
        if len(self._recent_files) > self._max_recent_files:
            self._recent_files.pop()
        self.publish('recent_files_changed')
        self.__save()

    def clear_recent_files(self):
        self._recent_files = []
        self.publish('recent_files_changed')
        self.__save()

    def to_dict(self):
        return {
            "recent_files": self._recent_files,
            "publish_days": list(self._publish_days),
            "publish_hour": self._publish_hour,
            "default_question_count": self._default_question_count,
            "window_width": self._window_width,
            "window_height": self._window_height,
            "window_mode": self._window_mode.name,
            "splitter_position": self._splitter_position,
            "max_recent_files": self._max_recent_files,
            "ftp_config": self._ftp_config.to_dict()
        }

    def __str__(self):
        return f'app_config {self.to_dict()}'

    def __repr__(self):
        return f'RecentFiles {self.to_dict()}'
