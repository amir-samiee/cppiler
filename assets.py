from enum import Enum, auto
SAMPLE_CODE_FILE_PATH = "test.cpp"


class Token_names(Enum):
    reservedword = auto()
    identifier = auto()
    symbol = auto()
    number = auto()
    string = auto()


class Re_names(Enum):
    whitespace = auto()
    unknown = auto()


class sample_code:
    file_opened = False
    cached_value = ""

    @classmethod
    @property
    def value(cls):
        if cls.file_opened:
            return cls.cached_value
        with open(SAMPLE_CODE_FILE_PATH, "r") as file:
            cls.cached_value = file.read()
        cls.file_opened = True
        return cls.cached_value

    example_program = """
#include
using namespace std;
int main(){return 0;}
""".replace("\n", "")
