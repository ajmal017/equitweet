from postgres_db import MyDB
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime
import json

class PandaBro(object):
  def __init__(self):
    with open('./aws_database.json', 'r') as f:
      db_config = json.load(f)

    my_db = MyDB(**db_config)
    conn = my_db._db_connection
    sql = "select * from tweets"

    self.tweets_df = pd.io.sql.read_sql(sql, conn)

    conn.close()

  ## For each ticker ###
  def get_mean_polarity(self):
    """
    get the mean polarity for each ticker
    """
    return self.tweets_df.groupby(self.tweets_df['ticker'])['polarity'].mean()
    # df.argmax() get ticker

  def generate_prices(self, start, end):
    tickers = pd.read_csv('data/constituents.csv', usecols=['Ticker']).values
    pieces = []
    for ticker in tickers[:5]:
      df = web.DataReader(ticker[0], 'yahoo', start, end)
      df['ticker'] = ticker[0]
      pieces.append(df)
    return pd.concat(pieces)

  def normalize_polarity(self):
    """
    normalize polarity by the number of followers and
    level of subjectivity
    """
    df = self.tweets_df.copy()
    max_followers = df['followers_count'].max()
    df['weighted_followers'] = df['followers_count'] / max_followers
    
    df['polarity'] *= df['weighted_followers']
    df['polarity'] *= df['subjectivity']
    return df

  def overall_sentiment(self):
    """
    overall s&p 500 sentiment -- weighted by volume
    TODO: include market volume
    """
    volume_by_date = pd.DataFrame(self.tweets_df.groupby(self.tweets_df['date'])['polarity'].count(), dtype=float)
    volume_by_date.columns = ['volume']
    volume_by_date['date'] = volume_by_date.index

    mean_by_date = pd.DataFrame(self.tweets_df.groupby(self.tweets_df['date'])['polarity'].mean())
    mean_by_date.columns = ['daily_sentiment']
    mean_by_date['date'] = mean_by_date.index

    date_volume_mean = pd.merge(volume_by_date, mean_by_date)

    max_volume = volume_by_date['volume'].max(numeric_only=True)
    date_volume_mean['weighted_volume'] = date_volume_mean['volume'] / max_volume
    date_volume_mean['daily_sentiment'] *= date_volume_mean['weighted_volume']
    return date_volume_mean.drop(['weighted_volume', 'volume'], 1)

