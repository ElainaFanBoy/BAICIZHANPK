import requests
import random
from hashlib import md5
import os
import json
import re


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


def translate_bcz(word):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    word = word.replace(" ", "_")
    file_path = os.path.join('bcz_data', 'words', f"{word}.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            word_data = json.load(file)
        mean_cn = word_data.get("mean_cn", "没有找到中文释义")
        meanings = re.split(r'\s*;\s*', mean_cn)
        cleaned_meanings = []
        for meaning in meanings:
            cleaned_meaning = re.sub(r'\s*[a-zA-Z]+\.\s*', '', meaning).strip()
            if cleaned_meaning:
                cleaned_meanings.append(cleaned_meaning)
        result = '；'.join(cleaned_meanings)
        return result
    except FileNotFoundError:
        return f"文件未找到: {file_path}"
    except json.JSONDecodeError:
        return "文件格式有误"


def combined_translate(word):
    baicizhan_result = translate_bcz(word)
    baidu_translate_result = translate(word)
    return f"{baidu_translate_result}；{baicizhan_result}"

if __name__ == '__main__':
    string = 'coordinate'
    transRes = combined_translate(string)
    print(transRes)