# Script to randomly generate heterologous reaction sets
# Created: 23 June 2019
# Author: Szabolcs Cselgo Kovacs
# Contact: kovszasz@brc.hu


import random,pickle
from random import randrange

def binary_saver(obj,name):
    f=''
    outfile=open(f+name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()
def binary_loader(name):
    f=''
    infile=open(f+name,'rb')
    return pickle.load(infile)


has_been=[]
output=input("Name of file to save:\t")
start=input("Start seed:\t")
end=input("End seed:\t")
number_of_reactions=input("Number of reactions in the set:\t")
#mc=input("Pathway of reaction set:\t")
mc='MetaCycAll'
MetaCyc=binary_loader(mc)
reaction_set={}
for i in range(int(start),int(end)):
    random.seed(i)
    reaction_set[i]=[]
    has_been=[]
    while len(has_been)!=int(number_of_reactions):
        r=randrange(0,len(list(MetaCyc.keys()))-1)
        if r not in has_been:
            reaction_set[i].append(list(MetaCyc.keys())[r])
            has_been.append(r)

binary_saver(reaction_set,output)
