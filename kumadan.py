from flask import Flask, flash, redirect, render_template, request, url_for
import threading

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from openai import OpenAI
client = OpenAI(api_key="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")
# message = "おなかが痛い"

def encourage(message:str):
    global encourage_msg
    prompt1 = [
        {"role": "user", "content": message+"。2文くらいで励ましてください"},
    ]
    res = client.chat.completions.create(
        model = "gpt-3.5-turbo",  # GPTのエンジン名を指定します
        messages = prompt1, # type: ignore
        max_tokens = 200,  # 生成するトークンの最大数
        n = 1,  # 生成するレスポンスの数
        temperature=0.5,  # 生成時のランダム性の制御
    )
    encourage_msg = res.choices[0].message.content
    # for i, choice in enumerate(res.choices):
    #     print(f"index: {i}:")
    #     print(f"role: {choice.message.role}.")
    #     print(f"content: {choice.message.content}")


def get_number(message:str):
    numbers = {"1":"#7119", "2":"#9110", "3":"188"}
    global number
    prompt2 = [
        {"role": "user", "content": message},
        {"role": "user", "content":'今の相談が体や健康に関する相談の場合は"1"、'
        '犯罪に関する相談の場合は"2"、消費者トラブルに関する質問の場合は"3"と答えよ。それ以外の場合は"0"と答えよ'},
    ]
    res = client.chat.completions.create(
        model = "gpt-3.5-turbo",  # GPTのエンジン名を指定します
        messages = prompt2, # type: ignore
        max_tokens = 20,  # 生成するトークンの最大数
        n = 1,  # 生成するレスポンスの数
        temperature=1,  # 生成時のランダム性の制御
    )
    for i in res.choices:
        result = i.message.content
        if result in numbers:
            number = numbers[result]
        else:
            number = "0120279338"   # よりそいホットライン
        # print(f"number = {number}")


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if request.form['input']:
            t1 = threading.Thread(target=get_number, args=(request.form['input'],))
            t2 = threading.Thread(target=encourage, args=(request.form['input'],))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            return render_template('main.html', msg=encourage_msg, number=number)
    return render_template('main.html')