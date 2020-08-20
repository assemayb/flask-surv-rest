import os


base_dir = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(base_dir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
