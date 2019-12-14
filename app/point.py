from sqlalchemy.types import UserDefinedType
import re

class Point(UserDefinedType):
    def __init__(self, *args):
        self._args = args

    def get_col_spec(self):
        return 'POINT'

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return "(%f, %f)" % (float(value[0]), float(value[1]))
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                m = re.match(r"\(([^)]+),([^)]+)\)", value)
                if m:
                    return (float(m.group(1)), float(m.group(2)))
        return process