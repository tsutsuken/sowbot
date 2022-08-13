import os
import tweepy
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class SowBotStream(tweepy.StreamingClient):
	def on_tweet(self, tweet):
		print(tweet.text)
		print("on_tweet")

# Twitter認証情報を環境変数から読み込む
bearer_token = os.getenv('BEARER_TOKEN')

# タイムラインの監視スタート
print('Start watching tweets')
sowBotStream = SowBotStream(bearer_token)
sowBotStream.sample()

