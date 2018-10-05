import pandas as pd
import requests

TEAMS = {'NE': 'patriots',
         'TB': 'buccaneers',
         'MIA': 'dolphins',
         'TEN': 'titans',
         'OAK': 'raiders',
         'KC': 'chiefs',
         'BAL': 'ravens',
         'HOU': 'texans',
         'NYG': 'giants',
         'PHI': 'eagles',
         'CIN': 'bengals',
         'MIN': 'vikings',
         'SEA': 'seahawks',
         'ATL': 'falcons',
         'GB': 'packers',
         'ARI': 'cardinals',
         'BUF': 'bills',
         'NYJ': 'jets',
         'CLE': 'browns',
         'PIT': 'steelers',
         'IND': 'colts',
         'JAX': 'jaguars',
         'DEN': 'broncos',
         'LAC': 'chargers',
         'DAL': 'cowboys',
         'WAS': 'redskins',
         'CHI': 'bears',
         'DET': 'lions',
         'CAR': 'panthers',
         'NO': 'saints',
         'SF': '49ers',
         'LAR': 'rams'}

COLUMNS = [
    'year',
    'season',
    'team_a',
    'team_b',
    'kickoff_dome',
    'kickoff_weather_summary',
    'kickoff_temperature',
    'kickoff_feels_like',
    'kickoff_wind',
    'kickoff_humidity',
    'kickoff_visibility',
    'kickoff_barometer',
    'kickoff_dew_point',
    'kickoff_cloud_cover',
    'kickoff_precipitation_prob',
    'q2_dome',
    'q2_weather_summary',
    'q2_temperature',
    'q2_feels_like',
    'q2_wind',
    'q2_humidity',
    'q2_visibility',
    'q2_barometer',
    'q2_dew_point',
    'q2_cloud_cover',
    'q2_precipitation_prob',
    'q3_dome',
    'q3_weather_summary',
    'q3_temperature',
    'q3_feels_like',
    'q3_wind',
    'q3_humidity',
    'q3_visibility',
    'q3_barometer',
    'q3_dew_point',
    'q3_cloud_cover',
    'q3_precipitation_prob',
    'q4_dome',
    'q4_weather_summary',
    'q4_temperature',
    'q4_feels_like',
    'q4_wind',
    'q4_humidity',
    'q4_visibility',
    'q4_barometer',
    'q4_dew_point',
    'q4_cloud_cover',
    'q4_precipitation_prob'
]

def get_content_divs(html):
    result = []
    start = "<div class='span3'>"

    while html.find(start) > 0:
        html = html[html.find(start):]
        result.append(html[0:(html.find('</div>') + 6)])
        html = html[1:]

    return result


def get_section_prefix(html):
    result = None

    if html.find('<b>Kickoff</b>') >= 0:
        result = 'kickoff_'
    elif html.find('<b>Q2</b>') >= 0:
        result = 'q2_'
    elif html.find('<b>Q3</b>') >= 0:
        result = 'q3_'
    elif html.find('<b>Q4</b>') >= 0:
        result = 'q4_'

    return result


def was_game_under_dome(html):
    result = 'N'

    if html.find('<img alt="Dome"') >= 0:
        result = 'Y'

    return result


def get_weather_summary(html):
    index = html.find('<p><img') + 1
    html = html[index:]
    index = html.find('<p>') + 3
    html = html[index:]
    index = html.find('</p>')
    html = html[0:index]

    return html.strip()


def get_weather_value(html, param):
    result = ''

    index = html.find('<p> ' + param + ': <b>')
    if index >= 0:
        html = html[index + 9 + len(param):]
        index = html.find('</b>')
        result = html[0:index].strip()

    return result


def get_data_entry(html):
    result = {}
    prefix = get_section_prefix(html)

    if prefix is not None:
        result[prefix + 'dome'] = was_game_under_dome(html)
        result[prefix + 'weather_summary'] = get_weather_summary(html)
        result[prefix + 'temperature'] = get_weather_value(html, 'Temperature')
        result[prefix + 'feels_like'] = get_weather_value(html, 'Feels Like')
        result[prefix + 'wind'] = get_weather_value(html, 'Wind')
        result[prefix + 'humidity'] = get_weather_value(html, 'Humidity')
        result[prefix + 'visibility'] = get_weather_value(html, 'Visibility')
        result[prefix + 'barometer'] = get_weather_value(html, 'Barometer')
        result[prefix + 'dew_point'] = get_weather_value(html, 'Dew Point')
        result[prefix + 'cloud_cover'] = get_weather_value(html, 'Cloud Cover')
        result[prefix + 'precipitation_prob'] = get_weather_value(html, 'Precipitacion Prob')

    return result


def get_data_from_page(html):
    result = {}

    divs = get_content_divs(html)  # BeautifulSoup had a bug!!! It could not find the end of the div tag correctly
    for div in divs:
        entry = get_data_entry(div)

        for key, value in entry.items():
            result[key] = value

    return result


def get_weather_data(year, week, team_a, team_b):
    result = None
    url = 'http://www.nflweather.com/game/{}/week-{}/{}-at-{}'.format(year, week, TEAMS[team_a], TEAMS[team_b])

    response = requests.get(url)
    if response.status_code == 200:
        result = get_data_from_page(response.text)
        result['year'] = year
        result['season'] = week
        result['team_a'] = team_a
        result['team_b'] = team_b

    return result


if __name__ == '__main__':
    df = pd.read_csv('data/fantasy-data.csv')
    data = []

    i = 0
    for row in df.itertuples():
        i += 1
        _year = row.Season
        _week = row.Week
        _teamA = row.Team
        _teamB = row.Opponent
        print(f'[{i}] {_year}-S{_week}: {_teamA} vs. {_teamB}')

        new_rows = get_weather_data(_year, _week, _teamA, _teamB)
        if new_rows is None:
            new_rows = get_weather_data(_year, _week, _teamB, _teamA)

        if new_rows is not None:
            data.append(new_rows)

        if i % 1000 == 0:
            df = pd.DataFrame(data, columns=COLUMNS)
            df.to_csv('data/weather.csv')

    print('saving file')
    df = pd.DataFrame(data, columns=COLUMNS)
    df.to_csv('data/weather.csv')
    print('done')
