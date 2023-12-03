from http import HTTPStatus

import pytest
from unittest import mock

from misc.weather import get_weather, API_BASE_URL, FetchWeatherError
from tests.conftest import fake


class TestGetWeather:
    @mock.patch("requests.get", autospec=True)
    def test_get_weather(self, mocked_requests_get):
        response_json = fake.pydict(nb_elements=3)

        mocked_requests_get.return_value.status_code = HTTPStatus.OK
        mocked_requests_get.return_value.json.return_value = response_json

        city = fake.city()
        result = get_weather(city)

        mocked_requests_get.assert_called_once_with(f"{API_BASE_URL}{city}")
        assert result == response_json

    def test_get_weather_raises(self, mock_requests_get):
        response_text = "bad gateway"
        mock_requests_get.return_value.status_code = HTTPStatus.BAD_GATEWAY
        mock_requests_get.return_value.text = response_text

        city = fake.city()
        with pytest.raises(FetchWeatherError, match=response_text):
            get_weather(city)
