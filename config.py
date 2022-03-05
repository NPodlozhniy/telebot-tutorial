from enum import Enum

db_file = "database.vdb"

# in case when the environment does not define a variable
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class states(Enum):
    """
    Since Vedis is used as DB in which the stored values ​​are always strings,
    then statuses will also be strings
    """
    init = "noname"
    auth = "zelfer"

class db_config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False