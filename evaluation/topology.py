import openai
import os
from tqdm import tqdm
import networkx as nx
import numpy as np
import argparse
import time
from datetime import datetime, timedelta, timezone
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
import util

model_list = ["text-davinci-003","code-davinci-002","gpt-3.5-turbo","gpt-4"]
parser = argparse.ArgumentParser(description="connectivity")
parser.add_argument('--model', type=str, default="text-davinci-003", help='name of LM (default: text-davinci-003)')
parser.add_argument('--mode', type=str, default="easy", help='mode (default: easy)')
parser.add_argument('--prompt', type=str, default="none", help='prompting techniques (default: none)')
parser.add_argument('--T', type=int, default=0, help='temprature (default: 0)')
parser.add_argument('--token', type=int, default=2048, help='max token')
parser.add_argument('--SC', type=int, default=0, help='self-consistency (default: 0)')
parser.add_argument('--SC_num', type=int, default=5, help='number of cases for self-consistency (default: 5)')
parser.add_argument('--full', type=bool, default=False, help='full test or stand test')
parser.add_argument('--num', type=int, default=-1, help='number of tests')
args = parser.parse_args()
args.full="full" if args.full else "standard"
print(args.full)
if args.num==-1:
    args.num=len(os.listdir("NLgraph/topology/graph/"+args.mode+"/"+args.full))
    print(f"test on {args.num} tasks.")
assert args.prompt in ["CoT", "none", "0-CoT", "LTM", "PROGRAM","k-shot","Instruct","Algorithm","mat","kmat","rp","matm"]

def translate(edge, n, args):
    Q = ''
    if args.prompt in ["CoT", "k-shot", "LTM", "Instruct", "Algorithm","mat","kmat","rp","matm"]:
        with open("NLgraph/topology/prompt/" + args.prompt + "-prompt.txt", "r") as f:
            exemplar = f.read()
        Q = Q + exemplar + "\n\n"
    Q = Q + "In a directed graph with " + str(n) + " nodes numbered from 0 to " + str(n-1) + ":\n"
    for i in range(len(edge)):
        Q = Q + 'node '+str(edge[i][0])+' should be visited before node '+str(edge[i][1])+'\n'
    if args.prompt == "Instruct":
        Q = Q + "Let's construct a graph with the nodes and edges first.\n"
    Q = Q + "Q: Can all the nodes be visited? Give the solution. If yes, output the topology order in list form at the end.\nA:"
    match args.prompt:
        case "0-CoT":
            Q = Q + " Let's think step by step:"
        case "LTM":
            Q = Q + " Let's break down this problem:"
        case "PROGRAM":
            Q = Q + " Let's solve the problem by a Python program:"
    return Q

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(1000))
# def predict(Q):
#     input = Q
#     temperature = 0
#     if args.SC == 1:
#         temperature = 0.7
#     if 'gpt' in args.model:
#         Answer_list = []
#         for text in input:
#             response = openai.ChatCompletion.create(
#             model=args.model,
#             messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": text},
#             ],
#             temperature=temperature,
#             max_tokens=args.token,
#             )
#             Answer_list.append(response["choices"][0]["message"]["content"])
#         return Answer_list
#     response = openai.Completion.create(
#     model=args.model,
#     prompt=input,
#     temperature=temperature,
#     max_tokens=args.token,
#     )
#     Answer_list = []
#     for i in range(len(input)):
#         Answer_list.append(response["choices"][i]["text"])
#     return Answer_list

def log(Q, res, answer, args):
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    time = bj_dt.now().strftime("%Y%m%d---%H-%M")
    newpath = 'log/topology/'+args.model+'-'+args.mode+'-'+time+ '-' + args.prompt
    if args.SC == 1:
        newpath = newpath + "+SC"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    newpath = newpath + "/"
    np.save(newpath+"res.npy", res)
    np.save(newpath+"answer.npy", answer)
    with open(newpath+"prompt.txt","w") as f:
        f.write(Q)
        f.write("\n")
        f.write("Acc: " + str(res.sum())+'/'+str(len(res)) + '\n')
        print(args, file=f)

def check(solution, G):
    n = G.number_of_nodes()
    deg = [0] * n
    for i in range(n):
        deg[i] = G.in_degree[i]
    for node in solution:
        if deg[node] > 0:
            return 0
        for neighbor in list(G[node]):
            deg[neighbor] -= 1
    for i in range(n):
        if deg[i] != 0:
            return 0
    return 1
def process_ans(ans, pos, G):
    num, flag = 0, 0
    solution = []
    n = G.number_of_nodes()
    for i in range(pos, len(ans)):
        if ans[i] >= '0' and ans[i] <='9':
            num = num*10 + int(ans[i])
            flag = 1
        else:
            if flag == 1:
                solution.append(num)
                if len(solution) == n:
                    break
                flag = 0
            num = 0
    return solution

import re
def evaluate(ans, G):

    nums = re.findall(r'\d+', ans)
    
    n = G.number_of_nodes()

    if len(nums) < n:
        nums=[0]*n
    
    nums=[int(i) for i in nums]

    if check(nums[-n:], G):
        return 1
    return 0

    pos = ans.find("solution")
    if pos == -1:
        pos = max(ans.find("yes"), ans.find("in the following order"))
    if pos == -1:
        return 0
    solution = process_ans(ans, pos, G)
    flag1  = check(solution, G)
    solution = process_ans(ans, 0, G)

    flag2  = check(solution, G)

    return flag1 or flag2
    return ()

def main():
    # if 'OPENAI_API_KEY' in os.environ:
    #     openai.api_key = os.environ['OPENAI_API_KEY']
    # else:
    #     raise Exception("Missing openai key!")
    # if 'OPENAI_ORGANIZATION' in os.environ:
    #     openai.organization = os.environ['OPENAI_ORGANIZATION']
    res, answer = [], []
    # match args.mode:
    #     case "easy":
    #         g_num = 180
    #     case "medium":
    #         g_num = 450
    #     case "hard":
    #         g_num = 180
    g_num=args.num

    batch_num = 20
    for i in tqdm(range((g_num + batch_num - 1) // batch_num)):
        G_list, Q_list = [], []
        for j in range(i*batch_num, min(g_num, (i+1)*batch_num)):
            with open("NLgraph/topology/graph/"+args.mode+"/"+args.full+"/graph"+str(j)+".txt","r") as f:
                n, m = [int(x) for x in next(f).split()]
                edge = []
                for line in f: # read rest of lines
                    edge.append([int(x) for x in line.split()])
                G = nx.DiGraph()
                G.add_nodes_from(range(n))
                for k in range(m):
                    G.add_edge(edge[k][0], edge[k][1])
                Q = translate(edge, n, args)
                Q_list.append(Q)
                G_list.append(G)

        ans_list = util.predict(Q_list, args)
        for k in range(len(ans_list)):
            ans, G = ans_list[k], G_list[k]
            answer.append(ans.lower())
            # print(re.findall(r'\d+', ans))
            try:
                result = evaluate(ans.lower(), G)
                res.append(result)
            except Exception as e:
                print(ans.lower())
                print(e)

    res = np.array(res)
    answer = np.array(answer)
    log(Q, res, answer, args)
    print(res.sum())
if __name__ == "__main__":
    main()