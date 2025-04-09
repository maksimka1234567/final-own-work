import io
import logging
from contextlib import contextmanager, redirect_stdout
from json import dumps
from multiprocessing import Process
from time import sleep

from flask import Flask

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Server:
    def __init__(self, host, port, data):
        self.__host__ = host
        self.__port__ = port
        self.__data__ = data

    @contextmanager
    def run(self):
        p = Process(target=self.server)
        p.start()
        sleep(1)
        yield
        p.kill()

    def server(self):
        _ = io.StringIO()
        with redirect_stdout(_):
            app = Flask(__name__)

            @app.route('/')
            def index():
                return dumps(self.__data__)

            app.run(self.__host__, self.__port__)


if __name__ == '__main__':
    data = [
        {"genie": "Belial", "vessel": "kettle", "duration": 1079, "afraid": "steam train"},
        {"genie": "Phenex", "vessel": "lamp", "duration": 1008, "afraid": "car"},
        {"genie": "Belial", "vessel": "lamp", "duration": 289, "afraid": "horn"},
        {"genie": "Zepar", "vessel": "watering", "duration": 160, "afraid": "bright light"},
        {"genie": "Phenex", "vessel": "lamp", "duration": 482, "afraid": "horn"},
        {"genie": "Phenex", "vessel": "lamp", "duration": 1132, "afraid": "siren"},
        {"genie": "Zepar", "vessel": "lamp", "duration": 897, "afraid": "horn"},
        {"genie": "Belial", "vessel": "lamp", "duration": 1063, "afraid": "car"}
    ]

    server = Server('127.0.0.1', 8080, data)
    with server.run():
        while (row := input('Введите "stop" для завершения работы сервера: ')) != 'stop':
            ...
