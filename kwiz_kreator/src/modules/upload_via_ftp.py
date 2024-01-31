import queue

# import pysftp
from ftplib import FTP
from .app_config import FtpConfig


class UploadViaFTP(object):
    _sftp_config: FtpConfig

    def __init__(self, sftp_config: FtpConfig):
        self.message_queue = queue.Queue()
        self.subscribers = []
        self._sftp_config = sftp_config

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        self.message_queue.put(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)



    @property
    def sftp_config(self):
        return self._sftp_config

    @sftp_config.setter
    def sftp_config(self, value: FtpConfig):
        self._sftp_config = value
        self.publish("sftp_config_changed")

    def push_to_server(self, file_name: str):

        if self._sftp_config is None:
            return

        try:
            with FTP(self._sftp_config.host) as ftp:
                ftp.login(user=self._sftp_config.username, passwd=self._sftp_config.password)
                ftp.cwd(self._sftp_config.remote_path)
                ftp.dir()
                with open(file_name + "/trivia.json", "rb") as trivia_file:
                    print(f'executing: STOR {self._sftp_config.remote_path}/trivia.json')
                    ftp.storbinary(f'STOR {self._sftp_config.remote_path}/trivia.json', trivia_file)
                ftp.dir()
                ftp.quit()
            self.publish('trivia_deployed')
        except Exception as e:
            print(e)
            return

