import scent


class Dictionary(scent.Object):
    """連想配列のクラス。
    """

    def __init__(self, value: dict = {}):
        self._dict = value
        self._keys = list(value.keys())
        self._iterate_index = -1

    @property
    def dict(self) -> dict:
        return self._dict

    @dict.setter
    def dict(self, value: dict):
        self._dict = value
        self._keys = list(value.keys())

    @property
    def keys(self) -> list:
        return self._keys

    def __repr__(self) -> str:
        dict = {}
        for key, value in self:
            dict[key] = value
        return repr(dict)

    def __str__(self) -> str:
        dict = {}
        for key, value in self:
            dict[key] = value
        return str(dict)

    def __eq__(self, other: object) -> bool:
        return self.dict == other

    @property
    def iterate_index(self) -> int:
        return self._iterate_index

    def __iter__(self) -> "Dictionary":
        return self

    def __next__(self) -> tuple:
        if self.length() - 1 <= self.iterate_index:
            self._iterate_index = -1
            raise StopIteration()
        self._iterate_index += 1
        key = self._keys[self.iterate_index]
        return (key, self.get(key))

    def copy(self) -> "Dictionary":
        """インスタンスのコピーを作成する。
        """
        return Dictionary(self.dict.copy())

    def length(self) -> int:
        """配列の要素数を取得する。
        """
        return self.dict.__len__()

    def values(self) -> tuple:
        """配列内のすべての値を取得する。
        """
        values = []
        for key in self._keys:
            values.append(self.get(key))
        return tuple(values)

    def keys(self) -> tuple:
        """配列内のすべてのキーを取得する。
        """
        return tuple(self._keys)

    def put(self, key: str, dict: any):
        """配列に値を配置する。
        """
        self.dict[key] = dict
        if key in self._keys == False:
            self._keys.append(key)

    def add(self, value: any):
        """配列に値を追加する。キーはintで自動採番される。
        """
        key = self.length()
        while key in self.keys():
            key += 1
        self.put(str(key), value)

    def remove_key(self, key: str):
        """指定されたキーに一致する配列の要素を削除する。
        """
        try:
            del self.dict[key]
            self._keys.remove(key)
        except (KeyError, ValueError):
            pass

    def remove_value(self, dict: any):
        """指定された値を配列からすべて削除する。
        """
        try:
            for key in self.keys():
                if dict == self.get(key):
                    del self.dict[key]
                    self._keys.remove(key)
        except TypeError:
            pass

    def clear(self):
        """配列からすべての要素を削除する。
        """
        self.dict.clear()
        self._keys.clear()

    def get(self, key: str) -> any:
        """配列の値を取得する。
        """
        try:
            return self.dict[key]
        except KeyError:
            return None

    def get_int(self, key: str) -> int:
        """配列の値をintとして取得する。
        """
        return scent.String(self.get(key)).to_int()

    def get_float(self, key: str) -> float:
        """配列の値をfloatとして取得する。
        """
        return scent.String(self.get(key)).to_float()

    def get_bool(self, key: str) -> bool:
        """配列の値をboolとして取得する。
        """
        return scent.String(self.get(key)).to_bool()

    def get_datetime(self, key: str) -> "scent.Datetime":
        """配列の値をDatetimeとして取得する。
        """
        return scent.Datetime(self.get(key))

    def merge(self, *dictionaries: "Dictionary"):
        """ほかの配列を結合する。キーが重複する場合、あとの値で上書きされる。
        """
        for dictionary in dictionaries:
            for key in dictionary.keys():
                self.put(key, dictionary.get(key))

    def sort_keys(self, reverse: bool = False):
        """配列をキーで並び替える。
        """
        keys = list(self.keys())
        keys.sort(reverse=reverse)
        self._keys = keys

    def sort_values(self, reverse: bool = False):
        """配列を値で並び替える。
        """
        value_and_keys = {}
        for key, value in self:
            keys = []
            value_id = id(value)
            if value_id in value_and_keys.keys():
                keys = value_and_keys[value_id]
            else:
                value_and_keys[value_id] = keys
            keys.append(key)
        values = list(self.values())
        values.sort(reverse=reverse)
        keys_for_sort = []
        for value in values:
            value_id = id(value)
            keys = value_and_keys[value_id]
            for key in keys:
                keys_for_sort.append(key)
        self._keys = keys_for_sort
