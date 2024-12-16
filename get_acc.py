import os
import re

def latest_acc(q,model,mode,prompt):
    pwd=f"log/{q}"
    folders=os.listdir(pwd)
    time_format = "%Y%m%d---%H-%M"
    prompt=re.sub(r'\+','\\+',prompt)
    pattern = re.compile(f"^{model}-{mode}-\\d*---\\d*-\\d*-{prompt}$")
    fol=[]
    for folder in folders:
        match = pattern.search(folder)
        if match :
            fol.append(folder)
    fol=sorted(fol,reverse=True)
    fol=fol[:min(1,len(fol))]
    # print(fol)
    if len(fol)==0:
        return {'avg':None}
    res=[]
    for i in fol:
        f=open(f"{pwd}/{i}/prompt.txt","r")
        data=f.read().split('\n')[-3].split(' ')[1].split('/')
        x,y=int(data[0]),int(data[1])
        res.append(x/y)
        f.close()
    # return x,y
    return {'avg':f"{sum(res)/len(res)*100:.2f}%",'list':res}

# prompt=["none","k-shot","0-CoT","CoT","CoT+SC","LTM","mat","Algorithm"]
prompt=["none","k-shot","0-CoT","CoT","CoT+SC","mat","kmat","rp","matm"]
print("gpt-3.5-turbo-instruct")
for i in prompt:
    # print(f'{i}: {latest_acc("topology","gpt-4o-mini","easy",i)["avg"]}')
    print(f' {i}: {latest_acc("topology","gpt-3.5-turbo-instruct","easy",i)["avg"]}')
print("gpt-4o-mini")
for i in prompt:
    print(f' {i}: {latest_acc("topology","gpt-4o-mini","easy",i)["avg"]}')
    # print(f'{i}: {latest_acc("topology","gpt-3.5-turbo-instruct","easy",i)["avg"]}')