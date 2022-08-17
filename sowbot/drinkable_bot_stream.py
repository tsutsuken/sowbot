import os
import tweepy
from tweepy.client import Response

# 環境変数を読み込む
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# TODO: 正式なドリンカブルボットのusernameに置き換える
username_drinkable_bot= '@kenkonn' 
# TODO: 正式なベリロン共通ボットのidに置き換える
verylong_common_bot_author_id = 1289935680236183553 # @tsutsukenz
# TODO: 正式なトークン送付完了文言に置き換える
tweet_text_token_transfer_complete = '無事に届いたよ'

class DrinkableBotStream(tweepy.StreamingClient):
	def __init__(self, _bearer_token, *, return_type=Response,
                 wait_on_rate_limit=False, **kwargs):
		print('init DrinkableBotStream')
		super().__init__(_bearer_token, return_type=Response,
                 wait_on_rate_limit=False, **kwargs)
		self.client = tweepy.Client(_bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
		self.delete_all_rules()
		self.add_custom_rules()

	def delete_all_rules(self):
		print("delete_all_rules")
		rule_ids = []
		rules = self.get_rules()
		print('rules before deleting', rules)
		
		# rule_idsを作成
		if str(rules).find("id") == -1:
			print("did not delete: no id in rules")
			return
		for rule in rules.data:
			rule_ids.append(rule.id)
			
		# rulesを削除
		if(len(rule_ids) <= 0): 
			print("did not delete: rule_ids <= 0")
			return
		print("deleted rules")
		self.delete_rules(rule_ids)
		print('rules after deleting', self.get_rules())

	def add_custom_rules(self):
		print("add_custom_rules")
		rule_mention_to = username_drinkable_bot
		self.add_rules(tweepy.StreamRule(rule_mention_to))
		print('rules after adding', self.get_rules())
	
	def on_tweet(self, tweet):
		print("on_tweet")
		print(tweet.data)
		if tweet.author_id == verylong_common_bot_author_id:
			print("ベリロン共通ボットからのメンション")
			if tweet_text_token_transfer_complete in tweet.text:
				print("トークン送付完了ツイート")
				# referenced_tweetsがNoneでないかチェック
				print(f"referenced_tweets", tweet.referenced_tweets)
				if not tweet.referenced_tweets:
					print("referenced_tweetsが見つかりませんでした")
					return
				
				# reference_typeがreplied_toかチェック
				referenced_tweet = tweet.referenced_tweets[0]
				reference_type = referenced_tweet.type
				print(f"reference_type", reference_type)
				if reference_type != "replied_to":
					print("reference_typeがreplied_toではありませんでした")
					return
				
				# 「トークン送付完了ツイート」のリプライ先ツイートを取得
				tweet_id = referenced_tweet.id
				tweet_fetched = self.client.get_tweet(tweet_id, expansions=['author_id'], tweet_fields=['author_id','created_at'])
				print(f'tweet_fetched: {tweet_fetched}')
				tweet_text = tweet_fetched.data.text
				print(f'tweet_text: {tweet_text}')

				# TODO: ツイートからコマンドを取得
				# TODO: ツイートから送付トークン数を取得
				# TODO: sow軍団にメンションを飛ばす
			else:
				print("その他ツイート")
		else:
			print("一般ユーザからのメンション")
            # TODO: SOW軍団へのjoin
            # TODO: SOW軍団からのleave