import os
import re

def latest_acc(q,model,mode,prompt):
    pwd=f"log/{q}"
    folders=os.listdir(pwd)
    time_format = "%Y%m%d---%H-%M"
    prompt=re.sub(r'\+','\\+',prompt)
    pattern = re.compile(f"^{model}-{mode}-\\d*---\\d*-\\d*-{prompt}$")
    mx=None
    for folder in folders:
        match = pattern.search(folder)
        if match and (mx==None or folder > mx):
            mx=folder
    print(mx)
    if mx==None:
        return None
    f=open(f"{pwd}/{mx}/prompt.txt","r")
    data=f.read().split('\n')[-3].split(' ')[1].split('/')
    x,y=int(data[0]),int(data[1])
    f.close()
    # return x,y
    return f"{x/y*100:.2f}%"

prompt=["none","k-shot","0-CoT","CoT","CoT+SC","LTM","mat","Algorithm"]
# prompt=["none","k-shot","0-CoT","CoT","CoT+SC","LTM"]
for i in prompt:
    # print(latest_acc("topology","gpt-3.5-turbo-instruct","easy",i))
    print(f'{i}: {latest_acc("topology","gpt-3.5-turbo-instruct","easy",i)}')