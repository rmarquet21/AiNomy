import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from server.env import Env

ROOT_PATH = os.path.realpath(os.path.join(__file__, "..", ".."))


class HostContext:

    def __init__(self):
        self.load_local_env_if_required()

    def canonical_url(self) -> str:
        url = os.getenv(Env.AINOMY_CANONICAL_URL, 'http://localhost:4000')
        parsed_url = urlparse(url)
        assert parsed_url.scheme is not None or parsed_url.netloc is not None, \
            f"canonical url does not contains scheme, hostname and port {url}"

        return url

    def datastore_connection_string(self):
        connection_string = os.getenv(Env.AINOMY_DATABASE_URL, 'postgresql://ainomy:ainomy@ai-postgres/ainomy')
        return connection_string.replace("postgres://", "postgresql://")

    def fake_data(self) -> bool:
        return os.getenv(Env.FAKE_DATA, "0") == "1"

    def flask_secret(self):
        return os.getenv(Env.FLASK_SECRET, 'WA6WjaZHysFDPuwM')

    def debug(self) -> bool:
        return os.getenv(Env.FLASK_DEBUG) is not None

    def swagger_ui(self) -> bool:
        return os.getenv(Env.SWAGGER_UI, "0") == "1"

    def load_local_env_if_required(self):
        """
        this method is required when we are running flask in debug mode through pycharm.
        We just have to set the environment variable to LOCAL_DOTENV to reuse the existing
        .env file
        """
        local_env = os.getenv(Env.LOCAL_DOTENV, None)
        if local_env:
            root_path = os.path.join(ROOT_PATH, 'environments', local_env, '.env')
            if os.path.isfile(root_path):
                load_dotenv(dotenv_path=root_path)
