import scent_python as scent


class TimeoutError(Exception):
    """scentライブラリの処理がタイムアウトした場合に発生する。
    """
