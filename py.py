import scent
import abc
import importlib
from importlib import util as importlib_util
import inspect


class Py(metaclass=abc.ABCMeta):
    """静的な汎用関数のクラス。
    """

    @staticmethod
    def extract_methods_from_class(clazz, prefix: str = "") -> list:
        """クラスからメソッドを抽出する。
        """
        result = []
        for func in inspect.getmembers(clazz, inspect.isfunction):
            name = scent.String(func[0])
            if name.match("^" + prefix + "[a-z_]{0,}"):
                result.append(func[1])
        return result
        # TODO 必要か