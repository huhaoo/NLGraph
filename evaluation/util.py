import openai
import os
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client= openai.OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url="https://aihubmix.com/v1"
)

log_file=open("log.txt","w")

finish_reason_stop=0

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(1000))
def predict(Q, args):
    time.sleep(1)
    # print("predict with args: ", args)
    prom = Q
    temperature = 0
    if args.SC == 1:
        temperature = 0.7
    if not 'instruct' in args.model and not 'Instruct' in args.model:
        Answer_list = []
        for text in prom:
            try:
                response = client.chat.completions.create(
                    model=args.model,  # 使用传入的模型名称
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": text},
                    ],
                    temperature=temperature,  # 控制文本生成的随机性
                    max_tokens=args.token,  # 设置生成的最大 token 数
                )
                # response = openai.ChatCompletion.create(
                # model=args.model,
                # messages=[
                # {"role": "system", "content": "You are a helpful assistant."},
                # {"role": "user", "content": text},
                # ],
                # temperature=temperature,
                # max_tokens=args.token,
                # )
                # print(response)
                # print(response.choices[0].message.content)
                print("prompt:", text, file=log_file)
                print("response:", response.choices[0].message.content, file=log_file)
                print("\n\n", file=log_file)
                Answer_list.append(response.choices[0].message.content)
            except Exception as e:
                print(e)
                exit(1)
        return Answer_list
    try:
        response = client.completions.create(
            model=args.model,            # 传入模型
            prompt=prom,                 # 传入用户输入
            temperature=temperature,     # 控制随机性
            max_tokens=args.token,       # 限制返回 token 数
        )
        # response = openai.Completion.create(
        # model=args.model,
        # prompt=prom,
        # temperature=temperature,
        # max_tokens=args.token,
        # )
        Answer_list=[]
        for i in range(len(prom)):
            Answer_list.append(response.choices[i].text)
            # print("prompt:", prom[i], file=log_file)
            # print("response:", response.choices[i].text, file=log_file)
            # print("\n\n", file=log_file)
            if response.choices[i].finish_reason == "stop":
                global finish_reason_stop
                finish_reason_stop+=1
        # print(Answer_list)
        return Answer_list
        # Answer_list = []
        # for i in range(len(prom)):
        #     Answer_list.append(response["choices"][i]["text"])
    except Exception as e:
        print(e)
        exit(1)