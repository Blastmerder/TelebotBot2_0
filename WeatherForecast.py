import requests
from enum import Enum


class Lang(Enum):
    RU = "ru", "russian", "русский"
    EN = "en", "english", "англиский"

    @staticmethod
    def get_all():
        return [
            Lang.RU,
            Lang.EN
        ]


class Units(Enum):
    METRIC = "метрическая", "metric"
    IMPERIAL = "имперская", "imperic"

    @staticmethod
    def get_all():
        return [
            Units.METRIC,
            Units.IMPERIAL
        ]


class WeatherForecast:
    _token = "dfa26d863001646f934431c755cefedf"
    _url = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self._city = "Москва"
        self._lang = Lang.RU
        self._units = "metric"

    def _get_params(self):
        return {
            'appid': WeatherForecast._token,
            'units': self._units,
            'lang': self._lang.value[0],
            'q': self._city
        }

    def get_data(self):
        return requests.get(WeatherForecast._url, self._get_params())

    def set_city(self, new_city: str) -> bool:
        prev_city = self._city
        self._city = new_city
        if self.get_data().status_code != 200:
            self._city = prev_city
            return False
        return True

    def set_lang(self, language: str) -> bool:
        for lang in Lang.get_all():
            if language == lang.value[0] or language == lang.value[1]:
                self._lang = lang
                return True
        return False

    def set_units(self, unit: str) -> bool:
        for lang in Units.get_all():
            if unit == lang.value[0] or unit == lang.value[1]:
                self._lang = lang
                return True
        return False
