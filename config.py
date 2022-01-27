from enum import Enum

db_file = "database.vdb"

class states(Enum):
    """
    Since Vedis is used as DB in which the stored values ​​are always strings,
    then statuses will also be strings
    """
    init = "noname"
    auth = "zelfer"