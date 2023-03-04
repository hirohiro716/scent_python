import scent_python as scent
import datetime
import math


class Datetime(scent.Object):
    """日時のクラス。
    """

    date_format = "%Y-%m-%d"

    time_format = "%H:%M:%S"

    default_datetime_format = date_format + " " + time_format

    def __init__(self, value: any = None, format: str = default_datetime_format):
        if value is None:
            value = datetime.datetime.now()
        if isinstance(value, datetime.datetime):
            self._value = datetime.datetime.fromtimestamp(value.timestamp())
        elif isinstance(value, Datetime):
            self._value = value.value.copy()
        else:
            temporary = scent.String(value).to_datetime()
            if temporary is None:
                self._value = datetime.datetime.min
            else:
                self._value = temporary.value
        self._format = format

    @property
    def value(self) -> datetime.datetime:
        return self._value

    @value.setter
    def value(self, value: datetime.datetime):
        self._value = value

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, format: str):
        self._format = format

    def __repr__(self) -> str:
        return repr(self.value)

    def __str__(self) -> str:
        return datetime.datetime.strftime(self.value, self.format)
        
    def __eq__(self, other: any) -> bool:
        if isinstance(other, Datetime):
            return self.value.timestamp() == other.value.timestamp()
        if isinstance(other, datetime.datetime):
            return self.value.timestamp() == other.timestamp()
        other_datetime = Datetime.from_str(str(other))
        if other_datetime is None:
            raise TypeError()
        return self.value.timestamp() == other_datetime.value.timestamp()
    
    def __lt__(self, other: any) -> bool:
        if isinstance(other, Datetime):
            return self.value.timestamp() < other.value.timestamp()
        if isinstance(other, datetime.datetime):
            return self.value.timestamp() < other.timestamp()
        other_datetime = Datetime.from_str(str(other))
        if other_datetime is None:
            raise TypeError()
        return self.value.timestamp() < other_datetime.value.timestamp()

    def __le__(self, other: any) -> bool:
        if isinstance(other, Datetime):
            return self.value.timestamp() <= other.value.timestamp()
        if isinstance(other, datetime.datetime):
            return self.value.timestamp() <= other.timestamp()
        other_datetime = Datetime.from_str(str(other))
        if other_datetime is None:
            raise TypeError()
        return self.value.timestamp() <= other_datetime.value.timestamp()

    def equals_date(self, other: any) -> bool:
        """日付(年月日)のみを比較して等しい場合はTrueを返す。
        """
        if isinstance(other, Datetime):
            return all([self.get_year() == other.get_year(), self.get_month() == other.get_month(), self.get_day() == other.get_day()])
        if isinstance(other, datetime.datetime):
            return all([self.get_year() == other.year, self.get_month() == other.month, self.get_day() == other.day])
        other_datetime = Datetime.from_str(str(other))
        if other_datetime is None:
            return False
        return all([self.get_year() == other_datetime.get_year(), self.get_month() == other_datetime.get_month(), self.get_day() == other_datetime.get_day()])

    def equals_time(self, other: any) -> bool:
        """時刻(時分秒)のみを比較して等しい場合はTrueを返す。
        """
        if isinstance(other, Datetime):
            return all([self.get_hour() == other.get_hour(), self.get_minute() == other.get_minute(), self.get_second() == other.get_second()])
        if isinstance(other, datetime.datetime):
            return all([self.get_hour() == other.hour, self.get_minute() == other.minute, self.get_second() == other.second])
        other_datetime = Datetime.from_str(str(other))
        if other_datetime is None:
            return False
        return all([self.get_hour() == other_datetime.get_hour(), self.get_minute() == other_datetime.get_minute(), self.get_second() == other_datetime.get_second()])

    def copy(self) -> "Datetime":
        """インスタンスのコピーを作成する。
        """
        return Datetime(datetime.datetime.fromtimestamp(self.value.timestamp()), self.format)
    
    def modify(self, year: int = None, month: int = None, day: int = None, hour: int = None, minute: int = None, second: int = None, microsecond: int = None):
        """日時を変更する。
        """
        params = {}
        if year is not None:
            params["year"] = year
        if month is not None:
            params["month"] = month
        if day is not None:
            params["day"] = day
        if hour is not None:
            params["hour"] = hour
        if minute is not None:
            params["minute"] = minute
        if second is not None:
            params["second"] = second
        if microsecond is not None:
            params["microsecond"] = microsecond
        self.value = self.value.replace(**params)
    
    def add(self, years: int = None, months: int = None, days: int = None, hours: int = None, minutes: int = None, seconds: int = None, microseconds: int = None):
        """日時に加算する。
        """
        if years is not None:
            self.modify(year=self.value.year + years)
        if months is not None:
            y = math.floor(months / 12)
            m = months % 12
            self.modify(year=y + self.value.year, month=m + self.value.month)
        params = {}
        if days is not None:
            params["days"] = days
        if hours is not None:
            params["hours"] = hours
        if minutes is not None:
            params["minutes"] = minutes
        if seconds is not None:
            params["seconds"] = seconds
        if microseconds is not None:
            params["microseconds"] = microseconds
        self.value = self.value + datetime.timedelta(**params)

    def get_year(self) -> int:
        """年を取得する。
        """
        return self.value.year

    def get_month(self) -> int:
        """月を取得する。
        """
        return self.value.month
    
    def get_day(self) -> int:
        """日を取得する。
        """
        return self.value.day

    def get_hour(self) -> int:
        """時を取得する。
        """
        return self.value.hour

    def get_minute(self) -> int:
        """分を取得する。
        """
        return self.value.minute

    def get_second(self) -> int:
        """秒を取得する。
        """
        return self.value.second
    
    def get_microsecond(self) -> int:
        """マイクロ秒を取得する。
        """
        return self.value.microsecond

    def get_weekday(self) -> "scent.WeekDay":
        """週を取得する。
        """
        match(self.value.weekday()):
            case 0:
                return scent.WeekDay.MONDAY
            case 1:
                return scent.WeekDay.TUESDAY
            case 2:
                return scent.WeekDay.WEDNESDAY
            case 3:
                return scent.WeekDay.THURSDAY
            case 4:
                return scent.WeekDay.FRIDAY
            case 5:
                return scent.WeekDay.SATURDAY
            case 6:
                return scent.WeekDay.SUNDAY

    def str_date(self) -> str:
        """年月日だけの文字列を生成する。フォーマットはdate_formatが使用される。
        """
        return datetime.datetime.strftime(self.value, Datetime.date_format)
    
    def str_time(self) -> str:
        """時刻だけの文字列を生成する。フォーマットはtime_formatが使用される。
        """
        return datetime.datetime.strftime(self.value, Datetime.time_format)

    @staticmethod
    def from_str(str: str) -> "Datetime":
        """日時の文字列からインスタンスを生成する。失敗した場合はNoneを返す。
        """
        string = scent.String(str)
        format = None
        if string.match("^[0-9]{4}/[0-1]{1}[0-9]{1}/[0-3]{1}[0-9]{1}$"):
            format = "%Y/%m/%d"
        if string.match("^[0-9]{4}\\-[0-1]{1}[0-9]{1}\\-[0-3]{1}[0-9]{1}$"):
            format = "%Y-%m-%d"
        if string.match("^[0-9]{4}/[0-1]{1}[0-9]{1}/[0-3]{1}[0-9]{1} [0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%Y/%m/%d %H:%M"
        if string.match("^[0-9]{4}\\-[0-1]{1}[0-9]{1}\\-[0-3]{1}[0-9]{1} [0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%Y-%m-%d %H:%M"
        if string.match("^[0-9]{4}/[0-1]{1}[0-9]{1}/[0-3]{1}[0-9]{1} [0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%Y/%m/%d %H:%M:%S"
        if string.match("^[0-9]{4}\\-[0-1]{1}[0-9]{1}\\-[0-3]{1}[0-9]{1} [0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%Y-%m-%d %H:%M:%S"
        if string.match("^[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%H:%M:%S"
        if string.match("^[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$"):
            format = "%H:%M"
        try:
            return scent.Datetime(datetime.datetime.strptime(string.value, format), format)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def years_list(current_year: int = datetime.datetime.now().year, subtraction: int = 10, addition: int = 10) -> list:
        """年リストを作成する。
        """
        return list(range(current_year - subtraction, current_year + addition + 1))
    
    @staticmethod
    def months_list() -> list:
        """月リストを作成する。
        """
        return list(range(1, 12 + 1))
    