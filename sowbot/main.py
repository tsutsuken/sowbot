import os
import tweepy
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class SowBotStream(tweepy.StreamingClient):
	def on_tweet(self, tweet):
		print("on_tweet")
		print(tweet.data)

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


# Twitter認証情報を環境変数から読み込む
bearer_token = os.getenv('BEARER_TOKEN')

# Streamのrulesをリセット
sow_bot_stream = SowBotStream(bearer_token)
sow_bot_stream.delete_all_rules()

# Streamのrulesを追加
watch_target_twitter_id = '1556826633478483969' # @kenkonnのid。後にベリロン共通ボットのidに置き換える
rule_base = 'from:{} -from:twitter'
rule_formatted = rule_base.format(watch_target_twitter_id)
sow_bot_stream.add_rules(tweepy.StreamRule(rule_formatted))
print('rules after adding', sow_bot_stream.get_rules())

# Twitterタイムラインの監視をスタート
print('start watching tweets')
required_info = ['author_id', 'created_at']
sow_bot_stream.filter(tweet_fields=required_info)

