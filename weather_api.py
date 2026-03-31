import requests

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weekly_forecast(self, city):
        """Получает прогноз на 7 дней"""
        params = {'q': city, 'appid': self.api_key, 'units': 'metric', 'lang': 'ru'}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None