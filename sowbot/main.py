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

# Streamを生成
bearer_token = os.getenv('BEARER_TOKEN')
sow_bot_stream = SowBotStream(bearer_token)

# Streamのrulesをリセット
sow_bot_stream.delete_all_rules()

# Streamにrulesを追加
username_sow_bot= '@kenkonn' # TODO: 正式なusernameに置き換える
rule_mention_to = username_sow_bot
sow_bot_stream.add_rules(tweepy.StreamRule(rule_mention_to))
print('rules after adding', sow_bot_stream.get_rules())

# Twitterタイムラインの監視をスタート
print('start watching tweets')
required_info = ['author_id', 'created_at']
sow_bot_stream.filter(tweet_fields=required_info)
