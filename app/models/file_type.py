from enum import Enum

class FileType(str, Enum):
    clean = "clean"
    invalid = "invalid"
    dnc = "dnc"