
# UTCをJSTに変換
def change_time_JST(u_time):
    utc_time = datetime(u_time.year, u_time.month,u_time.day, \
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

# テキストからURLを抽出し、文字列として返す
def findurl(string):
    import regex
    urls = regex.findall('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', string)
    link = ''
    for url in urls:
        link = link + url + ' '
    return link

# ライブラリのインポート
import tweepy
from datetime import datetime,timezone
import pytz
import pandas as pd
import streamlit as st

#Twitter情報
consumer_key        = 'zzdCgpJKtFpFEypzwXZyhdPoM'
consumer_secret     = 'eDwjw8WBGrjs3n7qNmV40chNcblPo2SATGvxrYOP2ylfitHqqF'
access_token        = '99120036-4IxJhRYiY6YyQeXnuEBAotFD6kOM6eU8Kc7SCuxl4'
access_token_secret = 'O7YULUDPd6pAnjr0K5jSjlXZRW0Z92ZYzgdGiuKuTf2Wr'

#Twitter認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#　”wait_on_rate_limit = True”　利用制限にひっかかた時に必要時間待機する
api=tweepy.API(auth,wait_on_rate_limit=True)

def gettweet(word):
  # 検索条件
  search_word = word + ' min_faves:10 -filter:retweets'
  #取得件数
  item_number = 300

  #ツイートを抽出
  tweets = tweepy.Cursor(api.search,q=search_word, tweet_mode='extended',result_type="mixed",lang='ja').items(item_number)

  #抽出したデータから必要な情報を取り出す
  #取得したツイートを一つずつ取り出して必要な情報をtweet_dataに格納する
  tw_data = []

  for tweet in tweets:
      #ツイート時刻とユーザのアカウント作成時刻を日本時刻にする
      tweet_time = change_time_JST(tweet.created_at)
      create_account_time = change_time_JST(tweet.user.created_at)
      #テキストからURLを抜き出す
      tweet_urls=findurl(tweet.full_text)
      #tweet_dataの配列に取得したい情報を入れていく
      tw_data.append([
          tweet_time,
          tweet.full_text,
          tweet_urls,
          tweet.favorite_count, 
          tweet.retweet_count, 
          tweet.user.screen_name,
          tweet.user.name
                        ])

  #取り出したデータをpandasのDataFrameに変換
  #CSVファイルに出力するときの列の名前を定義
  labels=[
      'ツイート時刻',
      'ツイート本文',
      '参考URL',
      'いいね数',
      'リツイート数',
      'ユーザー名',
      'アカウント名'
      ]

  #tw_dataのリストをpandasのDataFrameに変換
  df = pd.DataFrame(tw_data,columns=labels)
  return df

#streamlit
st.sidebar.title("清水区関連ツイートまとめ")
st.sidebar.write("台風15号で被害を受けた清水区に関する情報")

st.sidebar.write("")
selected_item = st.sidebar.selectbox('表示キーワード',
                              ['清水区', '清水区 飲料水', '清水区 お風呂 OR シャワー', '清水区 生活用水', '清水区 食料', '清水区 子育て', '清水区 車 被災', '静岡 コインランドリー OR 洗濯'])
st.write(f'{selected_item}に関するツイート')


st.table(gettweet(selected_item))

st.sidebar.write("")
st.sidebar.write("")

st.sidebar.caption("""
Copyright (c) 2022 Nazareth-Software\n
""")

#CSVファイルに出力する
#CSVファイルの名前を決める
#file_name='./tw_data.csv'

#CSVファイルを出力する
#df.to_csv(file_name,encoding='utf-8-sig',index=False)
