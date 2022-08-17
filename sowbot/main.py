import os
from dotenv import load_dotenv
from drinkable_bot_stream import DrinkableBotStream

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数を読み込む
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

def main(): 
	init_stream()

def init_stream():
	print('init_stream')
	# Twitterタイムラインの監視をスタート
	drinkable_bot_stream = DrinkableBotStream(bearer_token)
	required_info = ['author_id', 'created_at', 'referenced_tweets']
	drinkable_bot_stream.filter(tweet_fields=required_info)

if __name__ == "__main__":
    main()