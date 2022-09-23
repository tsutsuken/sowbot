"""
	DB操作周りの関数を詰め込んだモジュールです。
	これをimportしてください。
	from db_control import *

"""
from sow_model import SowMembers, SowClass, SowStatus
from sow_setting import *
import random
from datetime import datetime, timezone, timedelta


def join_sow(arg_user_id, arg_screen_name, arg_tweet_date):
	"""
        隊員を入隊させる。
        UserIDが既に存在する場合、かつScreenNameがDB上のデータと異なる場合、ScreenNameを更新する。

        Args: 
            arg_user_id (int): UserID。桁数良く分からん。
            arg_screen_name (string):  TwitterのScreenName(@～)。
            arg_tweet_date (string): joinコマンドをツイートした日時。この日時を入隊日時とする。

        Returns: 
            int: 成否等を返す。RESULT_SUCCESS 追加成功(0),RESULT_ERROR 追加失敗(1), JOIN_SOW_RESULT_UPDATE 更新(2), JOIN_SOW_RESULT_ALREADY 追加済(3)

        Examples:
            >>>join_sow(1234567890123456,"@emotto55", "Wed May 23 06:01:13 +0000 2022")
            
    """	
	print(f"call join_sow {arg_user_id}, {arg_screen_name}, {arg_tweet_date}")
	try:
		#arg_screen_nameが@で始まっていなかったら先頭に@追加する。
		# *** どの形で格納するのが都合いいかは今後要検討 ***
		if arg_screen_name[0]!="@":
			arg_screen_name = "@" + arg_screen_name

		#user_idがDBにあるか確認する
		query = session.query(SowMembers).filter(SowMembers.user_id==arg_user_id)
		if session.query(query.exists()).scalar():
			print('[join_sow]指定のuser idが存在します')
			#あった場合、screen_name確認
			#DBのscreen_nameと引数のscreen_nameが異なる場合はscreen_name更新する
			if query.first().screen_name!=arg_screen_name:
				print('[join_sow]screen nameが変更されています')
				query.first().screen_name = arg_screen_name
				session.commit()
				return JOIN_SOW_RESULT_UPDATE
			else:
				print('[join_sow]追加済みかつ変更なし')
				return JOIN_SOW_RESULT_ALREADY
		else:
			#DBにない場合は追加する。
			print('[join_sow]指定のuser idが存在しません。DBに追加します')

			sow = SowMembers(user_id=arg_user_id, screen_name=arg_screen_name,join_date=convert_datetime(arg_tweet_date), 
				status_id=0, class_id=0, summon_num=0, response_num=0)
			session.add(sow)
			session.commit()
			print('[join_sow]追加成功')
			return RESULT_SUCCESS
	except:
		print('[join_sow]追加失敗')
		return RESULT_ERROR

def leave_sow(arg_user_id):
	"""
        隊員を脱隊させる。

        Args: 
            arg_user_id (int): UserID。

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
            >>>leave_sow(1234567890123456)
            
    """		
	print(f"call leave_sow {arg_user_id}")
	try:
		#user_idが一致するユーザーを削除する
		session.query(SowMembers).filter(SowMembers.user_id==arg_user_id).delete()
		session.commit()
		print('[leave_sow]削除成功')
		return RESULT_SUCCESS
	except:
		print('[leave_sow]削除失敗')
		return RESULT_ERROR

def get_all_sow():
	"""
        全隊員のリスト返す。

        Args: なし            

        Returns: 
            str[]: 隊員のScreenNameリストを返す。

        Examples:
            >>>result = get_all_sow()
			>>>print(result)
			[@xxxxxx,@yyyyyy,...]
            
    """		
	print("call get_all_sow")
	members = []
	try:
		#screen_nameカラムのみ全件取得する
		result = session.query(SowMembers).filter(SowMembers.status_id==0).add_columns(SowMembers.screen_name).all()
		print(result)
		for row in result:
			members.append(row.screen_name)
		return members
	except:
		print('[get_all_sow]取得失敗')
		return members
	
def get_random_sow(num):
	"""
        ランダムで隊員リストを取得する。

        Args: 
            num (int): 取得人数。

        Returns: 
            str[]: 隊員のScreenNameリストを返す。

        Examples:
            >>>result = get_random_sow(2)
			>>>print(result)
			[@xxxxxx,@yyyyyy]
            
    """		
	print(f"call get_random_sow {num}")
	members=[]
	try:
		#DBのレコード件数
		len = session.query(SowMembers).count()
		if num > len:
			#レコード件数より要望人数が多い場合、全員のリスト返す
			return get_all_sow()
		else:
			members=[]
			query = session.query(SowMembers).filter(SowMembers.status_id==0, SowMembers.id.in_(random.sample(range(1, len+1), num))).all()
			for row in query:
				members.append(row.screen_name)
				#print(row.screen_name)
			return members
	except:
		print('[get_random_sow]取得失敗')
		return members

def get_rookies(arg_summon_num, num=0):
	"""
        新人隊員リストを取得する。
		召喚回数がsummon_num以下のうち,ランダムでnum人の隊員リストを返す。
		numが省略された場合、召喚回数がsummon_num以下の全隊員リストを返す。

        Args: 
            arg_summon_num (int): 召喚回数。
            num (int): 取得人数。デフォルト引数0

        Returns: 
            str[]: 隊員のScreenNameリストを返す。

        Examples:
            >>>result = get_rookies(3, 2)
			>>>print(result)
			[@xxxxxx,@yyyyyy]
            
    """		
	print(f"call get_rookies {arg_summon_num}, {num}")
	members=[]
	try:
		query = session.query(SowMembers).filter(SowMembers.status_id==0, SowMembers.summon_num<=arg_summon_num).all()
		if 	num>len(query) or num<=0:
			#指定人数が多いまたは省略されている場合、見つかった全隊員リスト返す
			for row in query:
				members.append(row.screen_name)
			return members
		else:
			#見つかった全隊員のうち、ランダムで指定人数のリスト返す
			for row in random.sample(query, num):
				members.append(row.screen_name)
			return members
	except:
		print('[get_rookies]取得失敗')
		return members

def get_aces(arg_response_rate, num=0):
	"""
        応答率の高い隊員リストを取得する。
		応答率がresponse_rate以上のうち,ランダムでnum人の隊員リストを返す。
		num省略された場合、応答率がresponse_rate以上の全隊員リストを返す。

        Args: 
            arg_response_rate (int): 応答率(%)
            num (int): 取得人数。デフォルト引数0

        Returns: 
            str[]: 隊員のScreenNameリストを返す。

        Examples:
            >>>result = get_aces(60, 2)
			>>>print(result)
			[@xxxxxx,@yyyyyy]
            
    """		
	print(f"call get_aces {arg_response_rate}, {num}")
	members=[]
	try:
		#どうやらカラム(int)同士の計算は、小数点以下切り捨てられてる？floatにキャストしてもだめ。%で表すために100かける(割ってから100かけてもダメ)
		query = session.query(SowMembers).filter(SowMembers.status_id==0, (SowMembers.response_num*100) / SowMembers.summon_num >= arg_response_rate).all()
		
		if 	num>len(query) or num<=0:
			#指定人数が多いまたは省略されている場合、見つかった全隊員リスト返す
			for row in query:
				members.append(row.screen_name)
			return members
		else:
			#見つかった全隊員のうち、ランダムで指定人数のリスト返す
			for row in random.sample(query, num):
				members.append(row.screen_name)
			return members
	except:
		print('[get_aces]取得失敗')
		return members

def add_summon_num(*arg_screen_name):
	"""
        召喚回数を増やす。

        Args: 
            arg_screen_name (str[]): ScreenNameリスト

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
			>>>members = [”@user01","@user02"]
		    >>>add_summon_num(*members)
		    >>>add_summon_num(*get_all_sow())  #全隊員の召喚回数を増やす
    """	
	print(f"call add_summon_num {arg_screen_name}")
	try:
		query = session.query(SowMembers).filter(SowMembers.screen_name.in_(arg_screen_name)).all()
		for member in query:
			member.summon_num += 1
		session.commit()
		return RESULT_SUCCESS
		
	except:
		print('[add_summon_num]失敗')
		return RESULT_ERROR

def add_response_num(*arg_screen_name):
	"""
        応答回数を増やす。

        Args: 
            arg_screen_name (str[]): ScreenNameリスト

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
		    >>>add_response_num(”@user01","@user02")
		    >>>add_response_num(*get_all_sow())  #全隊員の応答回数を増やす
    """	
	print(f"call add_response_num {arg_screen_name}")
	try:
		query = session.query(SowMembers).filter(SowMembers.screen_name.in_(arg_screen_name)).all()
		for member in query:
			member.response_num += 1
		session.commit()
		return RESULT_SUCCESS
		
	except:
		print('[add_response_num]失敗')
		return RESULT_ERROR

def reset_summon_num(*arg_screen_name):
	"""
        召喚回数をリセットする。

        Args: 
            arg_screen_name (str[]): ScreenNameリスト

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
		    >>>reset_summon_num(”@user01","@user02")
		    >>>reset_summon_num(*get_all_sow())  #全隊員の召喚回数をリセットする
    """	
	print(f"call reset_summon_num {arg_screen_name}")
	try:
		query = session.query(SowMembers).filter(SowMembers.screen_name.in_(arg_screen_name)).all()
		for member in query:
			member.summon_num = 0
		session.commit()
		return RESULT_SUCCESS
		
	except:
		print('[reset_summon_num]失敗')
		return RESULT_ERROR

def reset_response_num(*arg_screen_name):
	"""
        応答回数をリセットする。

        Args: 
            arg_screen_name (str[]): ScreenNameリスト

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
		    >>>reset_summon_num(”@user01","@user02")
		    >>>reset_summon_num(*get_all_sow())  #全隊員の応答回数をリセットする
    """
	print(f"call reset_response_num {arg_screen_name}")
	try:
		query = session.query(SowMembers).filter(SowMembers.screen_name.in_(arg_screen_name)).all()
		for member in query:
			member.response_num = 0
		session.commit()
		return RESULT_SUCCESS
		
	except:
		print('[reset_response_num]失敗')
		return RESULT_ERROR

def change_status(arg_screen_name, arg_status):
	"""
        ステータスを変更する。

        Args: 
            arg_screen_name (str): ScreenName
            arg_status (int): status. 0=入隊状態

        Returns: 
            int: 成否を返す。RESULT_SUCCESS 成功(0),RESULT_ERROR 失敗(1)

        Examples:
		    >>>change_status(”@user01", 1)
    """
	print(f"call change_status {arg_screen_name}, {arg_status}")
	try:
		session.query(SowMembers).filter(SowMembers.screen_name==arg_screen_name).first().status_id = arg_status
		session.commit()
		return RESULT_SUCCESS
		
	except:
		print('[change_status]失敗')
		return RESULT_ERROR

def convert_datetime(created_at):
	"""
        日付を変換する。

        Args: 
            created_at (str): ツイートのcreated_at

        Returns: 
            yyyymmeehhmmss(str):日付文字列

        Examples:
		    >>>print(convert_datetime("Wed May 23 06:01:13 +0000 2022"))
			20220523150113
    """
	print(f"call convert_datetime {created_at}")
	converted_time = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
	converted_time = converted_time.astimezone(timezone(timedelta(hours=+9)))
	converted_time = datetime.strftime(converted_time, '%Y%m%d%H%M%S')

	return converted_time

