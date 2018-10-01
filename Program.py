import providers.weather as weather

if __name__ == '__main__':
    _date = '20160625'
    _latitude = '38.98055649'
    _longitude = '-76.92222595'

    a = weather.DailyWeatherObservationSet.load_from_api(_date, _latitude, _longitude)
    print(a)