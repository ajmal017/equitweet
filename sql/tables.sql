CREATE TABLE IF NOT EXISTS stocks (
  ticker VARCHAR(8) primary key, -- name this stock?
  name VARCHAR(100),
  sector VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tweets (
  ticker   VARCHAR(8) REFERENCES stocks(ticker),
  username VARCHAR(20), -- increase length
  tweet_id BIGINT, -- id from twitter
  followers_count INT,
  polarity DOUBLE PRECISION,
  subjectivity DOUBLE PRECISION,
  date DATE,
  UNIQUE (tweet_id, ticker)
);

CREATE TABLE IF NOT EXISTS prices (
  ticker VARCHAR(8) REFERENCES stocks(ticker),
  start_price REAL,
  end_price REAL,
  stat_date DATE
  -- what stock info do we want?
);
