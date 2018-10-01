import datetime
import requests
import json


class DailyWeatherObservationSet:
    def __init__(self, entries, date, latitude, longitude):
        self.entries = entries
        self.date = date
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def load_from_api(cls, date, latitude, longitude):
        url = 'https://api.weather.com/v1/geocode/{}/{}/observations/historical.json' \
              '?apiKey=6532d6454b8aa370768e63d6ba5a832e&startDate={}&endDate={}' \
              '&units=e'

        url = url.format(latitude, longitude, date, date)
        response = requests.get(url)
        json_data = json.loads(response.text)
        observations = []

        for observation in json_data['observations']:
            o = SingleWeatherObservation.load_from_api_response(observation)
            observations.append(o)

        return DailyWeatherObservationSet(observations, date, latitude, longitude)

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.date)

    def get_average_temperature(self):
        _sum = 0
        count = 0

        for entry in self.entries:
            _sum += entry.get_temperature()
            count += 1

        if count != 0:
            return _sum / count

        return None

    def get_average_feels_like_temperature(self):
        _sum = 0
        count = 0

        for entry in self.entries:
            _sum += entry.get_feels_like_temperature()
            count += 1

        if count != 0:
            return _sum / count

        return None

    def get_minimum_temperature(self):
        result = -1

        for entry in self.entries:
            if result == -1:
                result = entry.get_temperature()
            else:
                result = min(result, entry.get_temperature())

        if result != -1:
            return result

        return None

    def get_maximum_temperature(self):
        result = -1

        for entry in self.entries:
            if result == -1:
                result = entry.get_temperature()
            else:
                result = max(result, entry.get_temperature())

        if result != -1:
            return result

        return None


class SingleWeatherObservation:
    def __init__(self):
        self.date_time = 0
        self.day_night = ''
        self.temperature = 0
        self.feels_like_temperature = 0
        self.heat_index = 0
        self.dew_point = 0
        self.relative_humidity = 0
        self.condition = ''
        self.pressure = 0
        self.vis = 0
        self.wind_speed = 0
        self.wind_direction = ''
        self.uv_index = 0

    def get_date_time(self):
        return self.date_time

    def get_day_night_index(self):
        return self.day_night

    def get_temperature(self):
        return self.temperature

    def get_feels_like_temperature(self):
        return self.feels_like_temperature

    def get_heat_index(self):
        return self.heat_index

    def get_dew_point(self):
        return self.dew_point

    def get_relative_humidity(self):
        return self.relative_humidity

    def get_condition(self):
        return self.condition

    def get_pressure(self):
        return self.pressure

    def get_visibility(self):
        return self.vis

    def get_uv_index(self):
        return self.uv_index

    def get_wind_speed(self):
        return self.wind_speed

    def get_wind_direction(self):
        return self.wind_direction

    @classmethod
    def load_from_api_response(cls, observation):
        result = SingleWeatherObservation()

        result.date_time = observation['valid_time_gmt']
        result.day_night = observation['day_ind']
        result.temperature = observation['temp']
        result.feels_like_temperature = observation['feels_like']
        result.heat_index = observation['heat_index']
        result.dew_point = observation['dewPt']
        result.relative_humidity = observation['rh']
        result.condition = observation['wx_phrase']
        result.pressure = observation['pressure']
        result.vis = observation['vis']
        result.wind_speed = observation['wspd']
        result.wind_direction = observation['wdir']
        result.uv_index = observation['uv_index']

        return result
