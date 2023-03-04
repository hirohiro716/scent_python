import abc

class Object(metaclass=abc.ABCMeta):
    """scentライブラリすべてのクラスがこのクラスを継承する。
    """

    def id(self) -> int:
        """オブジェクト固有のIDを取得する。
        """
        return id(self)
    
    def str(self) -> str:
        """オブジェクトの文字列表現を取得する。
        """
        return str(self)
