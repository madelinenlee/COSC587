import providers.weather as weather

if __name__ == '__main__':
    _date = '20160625'
    _latitude = '38.98055649'
    _longitude = '-76.92222595'

    ds = weather.WeatherDataSet()
    ds.add_day_observations(weather.DailyWeatherObservationSet.load_from_api(_date, _latitude, _longitude))
    _latitude = '28.98055649'
    _longitude = '-77.92222595'
    ds.add_day_observations(weather.DailyWeatherObservationSet.load_from_api(_date, _latitude, _longitude))
    ds.save('/Users/yektaie/Desktop/df.csv')

    ds2 = weather.WeatherDataSet('/Users/yektaie/Desktop/df.csv')
    ds2.load()
    ds2.save('/Users/yektaie/Desktop/df2.csv')


