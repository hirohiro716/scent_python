import scent_python as scent
import sys
import re


class String(scent.Object):
    """文字列のクラス。
    """

    def __init__(self, value=""):
        self._value = str(value)
        self._iterate_index = -1

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value)

    def __add__(self, other):
        return self.append(other)

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: any) -> bool:
        if self.value == str(other):
            return True
        return False

    @property
    def iterate_index(self) -> int:
        return self._iterate_index

    def __iter__(self):
        return self

    def __next__(self) -> "String":
        if self.length() - 1 <= self.iterate_index:
            self._iterate_index = -1
            raise StopIteration()
        self._iterate_index += 1
        return self.copy().extract(self.iterate_index, self.iterate_index + 1)

    def copy(self) -> "String":
        """インスタンスのコピーを作成する。
        """
        return String(self.value)

    def length(self) -> int:
        """文字数を取得する。
        """
        return self.value.__len__()

    def match(self, regex: str) -> bool:
        """正規表現に一致する場合はTrueを返す。
        """
        return re.match(regex, self.value) != None

    def insert(self, addition: any, index: int) -> "String":
        """文字列を指定インデックスに挿入する。
        """
        if addition == None:
            return
        length = self.length()
        position = index
        if position < 0:
            position = length + index
        if position > length:
            position = length
        self.value = self.value[:index] + str(addition) + self.value[index:]
        return self

    def prepend(self, addition: any) -> "String":
        """先頭に文字列を挿入する。
        """
        return self.insert(addition, 0)

    def append(self, addition: any) -> "String":
        """末尾に文字列を挿入する。
        """
        return self.insert(addition, self.length())

    def padding_left(self, addition: any, length: int) -> "String":
        """指定文字数になるまで左側に文字列を追加する。
        """
        while self.length() < length:
            self.prepend(addition)
        return self
    
    def padding_right(self, addition: any, length: int) -> "String":
        """指定文字数になるまで右側に文字列を追加する。
        """
        while self.length() < length:
            self.append(addition)
        return self
    
    def extract(self, startIndex: int = 0, endIndex: int = sys.maxsize) -> "String":
        """開始インデックスから終了インデックスまでを抽出する。
        """
        length = self.length()
        start = startIndex
        if start < 0:
            start = length + startIndex
            if start < 0:
                start = 0
        end = endIndex
        if end < 0:
            end = length + endIndex
        if end > length:
            end = length
        self.value = self.value[start: end]
        return self

    def extract_by_regex(self, regex: str) -> "String":
        """正規表現に一致した部分を抽出する。
        """
        value = ""
        for one in re.findall(regex, self.value):
            value += one
        self.value = value
        return self

    def repeat(self, number: int) -> "String":
        """インスタンスの文字列を指定回数繰り返す。
        """
        value = ""
        for i in range(number):
            value += self.value
        self.value = value
        return self

    def replace(self, regex: str, replacement: str) -> "String":
        """正規表現に一致した部分を置き換える。
        """
        self.value = re.sub(regex, replacement, self.value)
        return self

    def replace_cr(self, replacement: str) -> "String":
        """CRを置き換える。CRLFのCRは置き換えない。
        """
        return self.replace("\r([^\n])|\r$", replacement + "\\1")

    def replace_lf(self, replacement: str) -> "String":
        """LFを置き換える。CRLFのLFは置き換えない。
        """
        return self.replace("^\n|([^\r])\n", "\\1" + replacement)

    def replace_crlf(self, replacement: str) -> "String":
        """CRLFを置き換える。
        """
        return self.replace("\r\n", replacement)

    def replace_tab(self, replacement: str) -> "String":
        """タブを置き換える。
        """
        return self.replace("\t", replacement)

    def trim(self) -> "String":
        """先頭と末尾のスペース('U+0020'|'U+3000')を削除する。
        """
        self.replace("^[ 　]{1,}", "")
        return self.replace("[ 　]{1,}$", "")

    def remove_meaningless_decimal_point(self) -> "String":
        """意味のない小数点以下を削除する。
        """
        return self.replace("\.{1}0{1,}$", "")

    def narrow(self) -> "String":
        """半角に変換する。
        """
        value = ""
        for one in self.value:
            if one in String.wide_to_narrow_dict.keys():
                value += String.wide_to_narrow_dict[one]
            else:
                value += one
        self.value = value
        return self

    def wide(self) -> "String":
        """全角に変換する。
        """
        value = ""
        for one in self.value:
            if one in String.narrow_to_wide_dict.keys():
                value += String.narrow_to_wide_dict[one]
            else:
                value += one
        self.value = value
        return self

    def lower(self) -> "String":
        """小文字に変換する。
        """
        value = ""
        for one in self.value.lower():
            if one in String.upper_to_lower_dict.keys():
                value += String.upper_to_lower_dict[one]
            else:
                value += one
        self.value = value
        return self

    def upper(self) -> "String":
        """大文字に変換する。
        """
        value = ""
        for one in self.value.upper():
            if one in String.lower_to_upper_dict.keys():
                value += String.lower_to_upper_dict[one]
            else:
                value += one
        self.value = value
        return self

    def hiragana(self) -> "String":
        """カタカナをひらがなに変換する。
        """
        value = ""
        for one in self.value:
            if one in String.katakana_to_hiragana_dict.keys():
                value += String.katakana_to_hiragana_dict[one]
            else:
                value += one
        self.value = value
        return self

    def katakana(self) -> "String":
        """ひらがなをカタカナに変換する。
        """
        value = ""
        for one in self.value:
            if one in String.hiragana_to_katakana_dict.keys():
                value += String.hiragana_to_katakana_dict[one]
            else:
                value += one
        self.value = value
        return self

    def to_bytes(self, encoding: str = "utf-8") -> bytes:
        """bytesに変換する。
        """
        return self.value.encode(encoding, "replace")

    @staticmethod
    def from_bytes(bytes: bytes, encoding: str = "utf-8") -> "String":
        """バイト型からインスタンスを生成する。
        """
        return String(bytes.decode(encoding, "ignore"))

    def to_int(self) -> int:
        """intに変換する。失敗した場合はNoneを返す。
        """
        try:
            return int(self.replace("[^0-9\\-]", "").value)
        except ValueError:
            return None

    def to_float(self) -> float:
        """floatに変換する。失敗した場合はNoneを返す。
        """
        try:
            return float(self.replace("[^0-9\\-\\.]", "").value)
        except ValueError:
            return None

    def to_bool(self) -> bool:
        """boolに変換する。失敗した場合はNoneを返す。
        """
        match (self.lower().value):
            case "true" | "1":
                return True
            case "false" | "0":
                return False
        return None

    def to_datetime(self) -> "scent.Datetime":
        """Datetimeに変換する。失敗した場合はNoneを返す。
        """
        return scent.Datetime.from_str(self.value)

    def split(self, regex: str) -> list:
        """正規表現で分割したlistを作成する。
        """
        return re.split(regex, self.value)

    def sum(self) -> int:
        """この文字列中の整数1桁を抽出して加算し和を求める。
        """
        result = 0
        for one in self.extract_by_regex("[1-9]").value:
            result += String(one).to_int()
        return result

    @staticmethod
    def join(objects: tuple | list, separator: str = "") -> "String":
        """tupleまたはlist内の要素の文字列表現を連結したインスタンスを生成する。
        """
        result = String()
        for one in objects:
            if result.length() > 0:
                result.append(separator)
            result.append(one)
        return result

    wide_to_narrow_dict = {
        "ａ": "a",
        "ｂ": "b",
        "ｃ": "c",
        "ｄ": "d",
        "ｅ": "e",
        "ｆ": "f",
        "ｇ": "g",
        "ｈ": "h",
        "ｉ": "i",
        "ｊ": "j",
        "ｋ": "k",
        "ｌ": "l",
        "ｍ": "m",
        "ｎ": "n",
        "ｏ": "o",
        "ｐ": "p",
        "ｑ": "q",
        "ｒ": "r",
        "ｓ": "s",
        "ｔ": "t",
        "ｕ": "u",
        "ｖ": "v",
        "ｗ": "w",
        "ｘ": "x",
        "ｙ": "y",
        "ｚ": "z",
        "Ａ": "A",
        "Ｂ": "B",
        "Ｃ": "C",
        "Ｄ": "D",
        "Ｅ": "E",
        "Ｆ": "F",
        "Ｇ": "G",
        "Ｈ": "H",
        "Ｉ": "I",
        "Ｊ": "J",
        "Ｋ": "K",
        "Ｌ": "L",
        "Ｍ": "M",
        "Ｎ": "N",
        "Ｏ": "O",
        "Ｐ": "P",
        "Ｑ": "Q",
        "Ｒ": "R",
        "Ｓ": "S",
        "Ｔ": "T",
        "Ｕ": "U",
        "Ｖ": "V",
        "Ｗ": "W",
        "Ｘ": "X",
        "Ｙ": "Y",
        "Ｚ": "Z",
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
        "ァ": "ｧ",
        "ア": "ｱ",
        "ィ": "ｨ",
        "イ": "ｲ",
        "ゥ": "ｩ",
        "ウ": "ｳ",
        "ェ": "ｪ",
        "エ": "ｴ",
        "ォ": "ｫ",
        "オ": "ｵ",
        "カ": "ｶ",
        "ガ": "ｶﾞ",
        "キ": "ｷ",
        "ギ": "ｷﾞ",
        "ク": "ｸ",
        "グ": "ｸﾞ",
        "ケ": "ｹ",
        "ゲ": "ｹﾞ",
        "コ": "ｺ",
        "ゴ": "ｺﾞ",
        "サ": "ｻ",
        "ザ": "ｻﾞ",
        "シ": "ｼ",
        "ジ": "ｼﾞ",
        "ス": "ｽ",
        "ズ": "ｽﾞ",
        "セ": "ｾ",
        "ゼ": "ｾﾞ",
        "ソ": "ｿ",
        "ゾ": "ｿﾞ",
        "タ": "ﾀ",
        "ダ": "ﾀﾞ",
        "チ": "ﾁ",
        "ヂ": "ﾁﾞ",
        "ッ": "ｯ",
        "ツ": "ﾂ",
        "ヅ": "ﾂﾞ",
        "テ": "ﾃ",
        "デ": "ﾃﾞ",
        "ト": "ﾄ",
        "ド": "ﾄﾞ",
        "ナ": "ﾅ",
        "ニ": "ﾆ",
        "ヌ": "ﾇ",
        "ネ": "ﾈ",
        "ノ": "ﾉ",
        "ハ": "ﾊ",
        "バ": "ﾊﾞ",
        "パ": "ﾊﾟ",
        "ヒ": "ﾋ",
        "ビ": "ﾋﾞ",
        "ピ": "ﾋﾟ",
        "フ": "ﾌ",
        "ブ": "ﾌﾞ",
        "プ": "ﾌﾟ",
        "ヘ": "ﾍ",
        "ベ": "ﾍﾞ",
        "ペ": "ﾍﾟ",
        "ホ": "ﾎ",
        "ボ": "ﾎﾞ",
        "ポ": "ﾎﾟ",
        "マ": "ﾏ",
        "ミ": "ﾐ",
        "ム": "ﾑ",
        "メ": "ﾒ",
        "モ": "ﾓ",
        "ャ": "ｬ",
        "ヤ": "ﾔ",
        "ュ": "ｭ",
        "ユ": "ﾕ",
        "ョ": "ｮ",
        "ヨ": "ﾖ",
        "ラ": "ﾗ",
        "リ": "ﾘ",
        "ル": "ﾙ",
        "レ": "ﾚ",
        "ロ": "ﾛ",
        "ワ": "ﾜ",
        "ヲ": "ｦ",
        "ン": "ﾝ",
        "ヴ": "ｳﾞ",
        "！": "!",
        "”": "\"",
        "＃": "#",
        "＄": "$",
        "％": "%",
        "＆": "&",
        "’": "'",
        "（": "(",
        "）": "",
        "＝": "=",
        "－": "-",
        "～": "~",
        "＾": "^",
        "￥": "\\",
        "＠": "@",
        "＋": "+",
        "＊": "*",
        "｛": "{",
        "｝": "}",
        "［": "[",
        "］": "]",
        "；": ";",
        "：": ":",
        "＜": "<",
        "＞": ">",
        "，": ":",
        "．": ".",
        "？": "?",
        "＿": "_",
        "／": "/",
        "　": " ",
    }

    narrow_to_wide_dict = {
        "a": "ａ",
        "b": "ｂ",
        "c": "ｃ",
        "d": "ｄ",
        "e": "ｅ",
        "f": "ｆ",
        "g": "ｇ",
        "h": "ｈ",
        "i": "ｉ",
        "j": "ｊ",
        "k": "ｋ",
        "l": "ｌ",
        "m": "ｍ",
        "n": "ｎ",
        "o": "ｏ",
        "p": "ｐ",
        "q": "ｑ",
        "r": "ｒ",
        "s": "ｓ",
        "t": "ｔ",
        "u": "ｕ",
        "v": "ｖ",
        "w": "ｗ",
        "x": "ｘ",
        "y": "ｙ",
        "z": "ｚ",
        "A": "Ａ",
        "B": "Ｂ",
        "C": "Ｃ",
        "D": "Ｄ",
        "E": "Ｅ",
        "F": "Ｆ",
        "G": "Ｇ",
        "H": "Ｈ",
        "I": "Ｉ",
        "J": "Ｊ",
        "K": "Ｋ",
        "L": "Ｌ",
        "M": "Ｍ",
        "N": "Ｎ",
        "O": "Ｏ",
        "P": "Ｐ",
        "Q": "Ｑ",
        "R": "Ｒ",
        "S": "Ｓ",
        "T": "Ｔ",
        "U": "Ｕ",
        "V": "Ｖ",
        "W": "Ｗ",
        "X": "Ｘ",
        "Y": "Ｙ",
        "Z": "Ｚ",
        "0": "０",
        "1": "１",
        "2": "２",
        "3": "３",
        "4": "４",
        "5": "５",
        "6": "６",
        "7": "７",
        "8": "８",
        "9": "９",
        "ｧ": "ァ",
        "ｱ": "ア",
        "ｨ": "ィ",
        "ｲ": "イ",
        "ｩ": "ゥ",
        "ｳ": "ウ",
        "ｪ": "ェ",
        "ｴ": "エ",
        "ｫ": "ォ",
        "ｵ": "オ",
        "ｶ": "カ",
        "ｶﾞ": "ガ",
        "ｷ": "キ",
        "ｷﾞ": "ギ",
        "ｸ": "ク",
        "ｸﾞ": "グ",
        "ｹ": "ケ",
        "ｹﾞ": "ゲ",
        "ｺ": "コ",
        "ｺﾞ": "ゴ",
        "ｻ": "サ",
        "ｻﾞ": "ザ",
        "ｼ": "シ",
        "ｼﾞ": "ジ",
        "ｽ": "ス",
        "ｽﾞ": "ズ",
        "ｾ": "セ",
        "ｾﾞ": "ゼ",
        "ｿ": "ソ",
        "ｿﾞ": "ゾ",
        "ﾀ": "タ",
        "ﾀﾞ": "ダ",
        "ﾁ": "チ",
        "ﾁﾞ": "ヂ",
        "ｯ": "ッ",
        "ﾂ": "ツ",
        "ﾂﾞ": "ヅ",
        "ﾃ": "テ",
        "ﾃﾞ": "デ",
        "ﾄ": "ト",
        "ﾄﾞ": "ド",
        "ﾅ": "ナ",
        "ﾆ": "ニ",
        "ﾇ": "ヌ",
        "ﾈ": "ネ",
        "ﾉ": "ノ",
        "ﾊ": "ハ",
        "ﾊﾞ": "バ",
        "ﾊﾟ": "パ",
        "ﾋ": "ヒ",
        "ﾋﾞ": "ビ",
        "ﾋﾟ": "ピ",
        "ﾌ": "フ",
        "ﾌﾞ": "ブ",
        "ﾌﾟ": "プ",
        "ﾍ": "ヘ",
        "ﾍﾞ": "ベ",
        "ﾍﾟ": "ペ",
        "ﾎ": "ホ",
        "ﾎﾞ": "ボ",
        "ﾎﾟ": "ポ",
        "ﾏ": "マ",
        "ﾐ": "ミ",
        "ﾑ": "ム",
        "ﾒ": "メ",
        "ﾓ": "モ",
        "ｬ": "ャ",
        "ﾔ": "ヤ",
        "ｭ": "ュ",
        "ﾕ": "ユ",
        "ｮ": "ョ",
        "ﾖ": "ヨ",
        "ﾗ": "ラ",
        "ﾘ": "リ",
        "ﾙ": "ル",
        "ﾚ": "レ",
        "ﾛ": "ロ",
        "ﾜ": "ワ",
        "ｦ": "ヲ",
        "ﾝ": "ン",
        "ｳﾞ": "ヴ",
        "!": "！",
        "\"": "”",
        "#": "＃",
        "$": "＄",
        "%": "％",
        "&": "＆",
        "'": "’",
        "(": "（",
        ")": "）",
        "=": "＝",
        "-": "－",
        "‑": "－",
        "ｰ": "－",
        "~": "～",
        "^": "＾",
        "\\": "￥",
        "@": "＠",
        "+": "＋",
        "*": "＊",
        "{": "｛",
        "}": "｝",
        "[": "［",
        "]": "］",
        ";": "；",
        ":": "：",
        "<": "＜",
        ">": "＞",
        ":": "，",
        ".": "．",
        "?": "？",
        "_": "＿",
        "/": "／",
        " ": "　",
    }

    katakana_to_hiragana_dict = {
        "ァ": "ぁ",
        "ア": "あ",
        "ィ": "ぃ",
        "イ": "い",
        "ゥ": "ぅ",
        "ウ": "う",
        "ェ": "ぇ",
        "エ": "え",
        "ォ": "ぉ",
        "オ": "お",
        "カ": "か",
        "ガ": "が",
        "キ": "き",
        "ギ": "ぎ",
        "ク": "く",
        "グ": "ぐ",
        "ケ": "け",
        "ゲ": "げ",
        "コ": "こ",
        "ゴ": "ご",
        "サ": "さ",
        "ザ": "ざ",
        "シ": "し",
        "ジ": "じ",
        "ス": "す",
        "ズ": "ず",
        "セ": "せ",
        "ゼ": "ぜ",
        "ソ": "そ",
        "ゾ": "ぞ",
        "タ": "た",
        "ダ": "だ",
        "チ": "ち",
        "ヂ": "ぢ",
        "ッ": "っ",
        "ツ": "つ",
        "ヅ": "づ",
        "テ": "て",
        "デ": "で",
        "ト": "と",
        "ド": "ど",
        "ナ": "な",
        "ニ": "に",
        "ヌ": "ぬ",
        "ネ": "ね",
        "ノ": "の",
        "ハ": "は",
        "バ": "ば",
        "パ": "ぱ",
        "ヒ": "ひ",
        "ビ": "び",
        "ピ": "ぴ",
        "フ": "ふ",
        "ブ": "ぶ",
        "プ": "ぷ",
        "ヘ": "へ",
        "ベ": "べ",
        "ペ": "ぺ",
        "ホ": "ほ",
        "ボ": "ぼ",
        "ポ": "ぽ",
        "マ": "ま",
        "ミ": "み",
        "ム": "む",
        "メ": "め",
        "モ": "も",
        "ャ": "ゃ",
        "ヤ": "や",
        "ュ": "ゅ",
        "ユ": "ゆ",
        "ョ": "ょ",
        "ヨ": "よ",
        "ラ": "ら",
        "リ": "り",
        "ル": "る",
        "レ": "れ",
        "ロ": "ろ",
        "ヮ": "ゎ",
        "ワ": "わ",
        "ヰ": "ゐ",
        "ヱ": "ゑ",
        "ヲ": "を",
        "ン": "ん",
    }

    hiragana_to_katakana_dict = {
        "ぁ": "ァ",
        "あ": "ア",
        "ぃ": "ィ",
        "い": "イ",
        "ぅ": "ゥ",
        "う": "ウ",
        "ぇ": "ェ",
        "え": "エ",
        "ぉ": "ォ",
        "お": "オ",
        "か": "カ",
        "が": "ガ",
        "き": "キ",
        "ぎ": "ギ",
        "く": "ク",
        "ぐ": "グ",
        "け": "ケ",
        "げ": "ゲ",
        "こ": "コ",
        "ご": "ゴ",
        "さ": "サ",
        "ざ": "ザ",
        "し": "シ",
        "じ": "ジ",
        "す": "ス",
        "ず": "ズ",
        "せ": "セ",
        "ぜ": "ゼ",
        "そ": "ソ",
        "ぞ": "ゾ",
        "た": "タ",
        "だ": "ダ",
        "ち": "チ",
        "ぢ": "ヂ",
        "っ": "ッ",
        "つ": "ツ",
        "づ": "ヅ",
        "て": "テ",
        "で": "デ",
        "と": "ト",
        "ど": "ド",
        "な": "ナ",
        "に": "ニ",
        "ぬ": "ヌ",
        "ね": "ネ",
        "の": "ノ",
        "は": "ハ",
        "ば": "バ",
        "ぱ": "パ",
        "ひ": "ヒ",
        "び": "ビ",
        "ぴ": "ピ",
        "ふ": "フ",
        "ぶ": "ブ",
        "ぷ": "プ",
        "へ": "ヘ",
        "べ": "ベ",
        "ぺ": "ペ",
        "ほ": "ホ",
        "ぼ": "ボ",
        "ぽ": "ポ",
        "ま": "マ",
        "み": "ミ",
        "む": "ム",
        "め": "メ",
        "も": "モ",
        "ゃ": "ャ",
        "や": "ヤ",
        "ゅ": "ュ",
        "ゆ": "ユ",
        "ょ": "ョ",
        "よ": "ヨ",
        "ら": "ラ",
        "り": "リ",
        "る": "ル",
        "れ": "レ",
        "ろ": "ロ",
        "ゎ": "ヮ",
        "わ": "ワ",
        "ゐ": "ヰ",
        "ゑ": "ヱ",
        "を": "ヲ",
        "ん": "ン",
    }

    upper_to_lower_dict = {
        "あ": "ぁ",
        "い": "ぃ",
        "う": "ぅ",
        "え": "ぇ",
        "お": "ぉ",
        "や": "ゃ",
        "ゆ": "ゅ",
        "よ": "ょ",
        "つ": "っ",
        "ア": "ァ",
        "イ": "ィ",
        "ウ": "ゥ",
        "エ": "ェ",
        "オ": "ォ",
        "ヤ": "ャ",
        "ユ": "ュ",
        "ヨ": "ョ",
        "ツ": "ッ",
    }

    lower_to_upper_dict = {
        "ぁ": "あ",
        "ぃ": "い",
        "ぅ": "う",
        "ぇ": "え",
        "ぉ": "お",
        "ゃ": "や",
        "ゅ": "ゆ",
        "ょ": "よ",
        "っ": "つ",
        "ァ": "ア",
        "ィ": "イ",
        "ゥ": "ウ",
        "ェ": "エ",
        "ォ": "オ",
        "ャ": "ヤ",
        "ュ": "ユ",
        "ョ": "ヨ",
        "ッ": "ツ",
    }
