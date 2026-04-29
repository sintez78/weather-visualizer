import requests

class WeatherFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_weekly_forecast(self, city):
        params = {
            'q': city, 
            'appid': self.api_key, 
            'units': 'metric', 
            'lang': 'ru'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка сервера: {response.status_code}")
                print(response.text) 
                return None
                
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return None
