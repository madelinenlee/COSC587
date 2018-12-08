import pandas as pd

def clean():
    d = {'kickoff_humidity': 'humidity_mean',
         'kickoff_visibility': 'visibility_mean',
         'wind_intensity': 'wind_intensity_mean'}
    filter_df = df[df["kickoff_wind"].notnull()]
    filter_df["wind_intensity"], filter_df["wind_direction"] = zip(*filter_df['kickoff_wind'].apply(lambda x: x.split("mi")))
    filter_df["wind_intensity"] = filter_df["wind_intensity"].astype(int)
    mean_df = filter_df.groupby('team_a').agg({'kickoff_humidity':'mean', 'kickoff_visibility':'mean'
                                        ,'wind_intensity':'mean'}).rename(d)
    mean_df["Common_Weather"] = filter_df.groupby(['team_a'])['kickoff_weather_summary'].agg(lambda x:x.value_counts().index[0])
    mean_df["Common_Wind Direction"] = filter_df.groupby(['team_a'])['wind_direction'].agg(
        lambda x: x.value_counts().index[0])
    mean_df.to_csv("map_graph.csv")
    print(mean_df)


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/madelinenlee/COSC587/master/cleaned_data/weather_cleaned.csv"
    df = pd.read_csv(url,index_col=0, parse_dates=[0])
    #df = pd.read_csv("cleaned_data\\weather_cleaned.csv", sep=',', encoding='latin1')
    clean()
