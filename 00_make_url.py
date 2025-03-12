import os #.env 속 데이터 사용하는 모듈
import requests #json 불러오는 모듈
from dotenv import load_dotenv #.env.에서 데이터 가져오는 모듈

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}' #api 토큰값 입력

res = requests.get(URL+ '/getUpdates') #json와주세요 #getUpdates는 url은 고정값, /뒤에 오는 명령어는 변수값이기 때문
res_dict = res.json() #json dict로 쓸게요

user_id = res_dict['result'][0]['message']['from']['id'] #result 안에 0번 폴더 안에 message 안에 from 안에 id 정보
text = res_dict['result'][0]['message']['text'] #result 안에 0번 폴더 안에 message안에 text 정보

requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={text}') # f스트링 안의 기능을 자동 실행(user id에게 text)