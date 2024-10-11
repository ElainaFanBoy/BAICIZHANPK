import requests
import random
from hashlib import md5


def make_md5(st, encoding='utf-8'):
    return md5(st.encode(encoding)).hexdigest()


def translate(query):
    appid = ''
    appkey = ''
    from_lang = 'en'
    to_lang = 'zh'
    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) +appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    res = requests.post(url, params=params, headers=headers).json()
    dst = ''.join([i['dst'] for i in res['trans_result']])
    return dst


if __name__ == '__main__':
    string = 'bat'
    transRes = translate(string)
    print(transRes)