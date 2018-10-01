import datetime
import requests
import json
import pandas as pd


class WeatherDataSet:
    def __init__(self, path=None):
        self.days = []
        self.path = path

    def load(self, path=None):
        if (path is None) & (self.path is None):
            raise ValueError('You should specify a path to load data set')
        elif (path is not None) & (self.path is None):
            self.path = path
        elif (path is None) & (self.path is not None):
            path = self.path

        df = pd.read_csv(path)
        _dict = {}

        for index, row in df.iterrows():
            lat_long_key = '{}__{}'.format(row['latitude'], row['longitude'])
            day = None
            if lat_long_key in _dict.keys():
                day = _dict[lat_long_key]
            else:
                day = DailyWeatherObservationSet()
                self.days.append(day)
                _dict[lat_long_key] = day

            day.entries.append(SingleWeatherObservation.load_from_csv(row))

    def save(self, path=None):
        if (path is None) & (self.path is None):
            raise ValueError('You should specify a path to save data set')
        elif (path is not None) & (self.path is None):
            self.path = path
        elif (path is None) & (self.path is not None):
            path = self.path

        data = []
        for day in self.days:
            for record in day.entries:
                data.append(record.to_dictionary())

        columns = ['time', 'latitude', 'longitude', 'day_night_index', 'temperature', 'feels_like', 'heat_index',
                   'dew_point', 'relative_humidity', 'condition', 'pressure', 'visibility', 'wind_speed',
                   'wind_direction', 'uv_index']
        df = pd.DataFrame(data, columns=columns)

        df.to_csv(path)

    def add_day_observations(self, day_data):
        self.days.append(day_data)

    def get_day_observations(self, date, latitude, longitude):
        result = None

        for day in self.days:
            if (day.latitude == latitude) & (day.longitude == longitude):
                result = day
                break

        return result

    def as_pandas_dataframe(self):
        if self.path is None:
            raise ValueError('You should specify a path to load data set')

        return pd.read_csv(self.path)


class DailyWeatherObservationSet:
    def __init__(self, entries=None, date=None, latitude=None, longitude=None):
        self.entries = entries
        if self.entries is None:
            self.entries = []

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
        response_data = json.loads(response.text)
        observations = []

        for observation in response_data['observations']:
            o = SingleWeatherObservation.load_from_api_response(observation, latitude, longitude)
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
    def __init__(self, latitude, longitude):
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
        self.latitude = latitude
        self.longitude = longitude

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
    def load_from_api_response(cls, observation, latitude, longitude):
        result = SingleWeatherObservation(latitude, longitude)

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

    @classmethod
    def load_from_csv(cls, observation):
        latitude = observation['latitude']
        longitude = observation['longitude']

        result = SingleWeatherObservation(latitude, longitude)

        result.date_time = observation['time']
        result.day_night = observation['day_night_index']
        result.temperature = observation['temperature']
        result.feels_like_temperature = observation['feels_like']
        result.heat_index = observation['heat_index']
        result.dew_point = observation['dew_point']
        result.relative_humidity = observation['relative_humidity']
        result.condition = observation['condition']
        result.pressure = observation['pressure']
        result.vis = observation['visibility']
        result.wind_speed = observation['wind_speed']
        result.wind_direction = observation['wind_direction']
        result.uv_index = observation['uv_index']

        return result

    def to_dictionary(self):
        return {
            'time': self.date_time,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'day_night_index': self.day_night,
            'temperature': self.temperature,
            'feels_like': self.feels_like_temperature,
            'heat_index': self.heat_index,
            'dew_point': self.dew_point,
            'relative_humidity': self.relative_humidity,
            'condition': self.condition,
            'pressure': self.pressure,
            'visibility': self.vis,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'uv_index': self.uv_index
        }

