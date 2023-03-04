import scent


class TimeoutError(Exception):
    """scentライブラリの処理がタイムアウトした場合に発生する。
    """
