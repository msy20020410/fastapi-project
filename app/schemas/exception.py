"""自定义异常定义。"""


class UnicornException(Exception):
    """独角兽业务异常。"""

    def __init__(self, name: str):
        self.name = name
