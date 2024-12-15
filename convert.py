import numpy as np

a=np.load('answer.npy')
print(a,file=open("answer.txt",'w'))