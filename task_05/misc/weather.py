from http import HTTPStatus

import requests


API_BASE_URL = "https://api-weather.example.com/"


class FetchWeatherError(Exception):
    pass


def get_weather(city):
    response = requests.get(f"{API_BASE_URL}{city}")
    if response.status_code == HTTPStatus.OK:
        return response.json()
    raise FetchWeatherError(response.text)
