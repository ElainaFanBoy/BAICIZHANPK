import mitmproxy.http
import json
import os
from termcolor import cprint
from trans import combined_translate
import numpy as np


def count(str1, str2):
    words1 = list(str1)
    words2 = list(str2)
    words = list(set(words1 + words2))
    vector1 = [words1.count(word) for word in words]
    vector2 = [words2.count(word) for word in words]
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    return dot_product / (norm1 * norm2)


def match(word, options):
    dst = combined_translate(word)
    print("翻译结果：", dst)
    scores = [count(opt, dst) for opt in options]
    max_score = max(scores)
    if max_score:
        return options[scores.index(max_score)]
    else:
        return ""


class Capture:
    def __init__(self):
        self.order = None

    def response(self, flow: mitmproxy.http.HTTPFlow):
        response = flow.response
        if 'https://pk.baicizhan.com/api/rankpk/challenge/heartbeat' in flow.request.url:
            res = json.loads(response.text)['data']
            if res['order'] != self.order:
                self.order = res['order']
                print('-' * 50)
                print(f'第{self.order}题 >>>')
                word = res['puzzle']['title']
                options = [i['text'] for i in res['puzzle']['options']]
                cprint(f'单词：{word}', 'red')
                print('选项', ' | '.join(options))
                answer = match(word, options)
                if answer:
                    cprint(f'匹配答案为选项 {options.index(answer) + 1} : {answer}', 'green')
                else:
                    cprint('无匹配答案，请手动作答！', 'red')


addons = [
    Capture()
]

if __name__ =='__main__':
    os.system('mitmdump -q -s capture.py')