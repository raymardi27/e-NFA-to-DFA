from re import sub
from copy import deepcopy
from tabulate import tabulate
from NFA_DFA import get_sigma,complete,trans_table

def divide(i,P,transitions):
    if len(i) == 1:
        return i
    print("I is :",i)
    sigma = get_sigma(transitions)
    sigma.remove(' Stat')
    Dup = deepcopy(transitions)
    for k in sigma:
        for  j in i:
            if transitions[j][k][0] in i:
                Dup[j]["tr"+str(k)] = 'Same'
            else:
                for l in P:
                    if l != i:
                        if transitions[j][k][0] in l:
                            Dup[j]["tr"+str(k)] = str(l)
    trans_table(Dup)
    divgrp = list()
    for j in i:
        if len(divgrp) == 1 and divgrp[0] == i:
            break
        grp,ele = [j],1 # ele is to let us know that the number of elements in each "group". Just to avoid using the len function
        for l in i[(i.index(j)+1):]:
            if len(l) == 0:
                    break
            count = 0
            for k in sigma:    
                if Dup[j]["tr"+str(k)] == Dup[l]["tr"+str(k)]:
                    count+=1
            if count == len(sigma):
                grp.append(l)
        grp = sorted(list(set(grp)))
        print(grp)
        for m in divgrp:
            if grp[0] in m:
                ele = 0
        if ele != 0:
            divgrp.append(grp)
    print("divgrp:",divgrp)
    lis = list()
    for i in divgrp:
        lis.append(divide(i,divgrp,transitions))
    return lis

def minimize(transitions):
    P,a,b = list(),list(),list()
    for i in transitions:
        if transitions[i][' Stat'] == 'Fin' or transitions[i][' Stat'] == 'Ini & Fin':
            b.append(i)
        else:
            a.append(i)
    P.append(a);P.append(b)
    B = list()
    for i in P:
        B.append(divide(i,P,transitions))
    print(B)



if __name__ == "__main__":
    file = open("dfadata.txt",'r+')
    main_dic = dict() #main is the one having the state and its transitions.
    # num = int(input("Input the number of states: "))
    num = int(file.readline())
    # print("Enter the Transition states: (Format- <input>:<list of states>;<input>:<list of states>. Epsilon should be mentioned as 'eps' only! Do not put the epsilon transition for the same state!)")
    for i in range(num):
        state = 'q'+str(i)
        # string = input("For "+state+" : ").split(";")
        string = file.readline().split(";")
        for i in range(len(string)):
            string[i] = string[i].rstrip('\n')
        inner_dict = dict() #inner is the one with input and the next states.
        for part in string:
            ip = sub(r':.*','',part) #The first part of the semi-colon is the inputs
            tr = sub(r'.*:','',part).split(',') #The transitions
            if tr[0] != '':
                inner_dict[ip] = tr
        main_dic[state] = inner_dict
    imp = file.readline().rstrip('\n').split()
    fmp = file.readline().rstrip('\n').split()
    # imp = input("Input the initial states: ").split()
    # fmp = input("Input the final states: ").split()
    for i in main_dic:
        if i in imp and i in fmp:
            main_dic[i][' Stat'] = 'Ini & Fin'
        elif i in fmp:
            main_dic[i][' Stat'] = 'Fin'
        elif i in imp:
            main_dic[i][' Stat'] = 'Ini'
        else:
            main_dic[i][' Stat'] = ''
    trans_table(main_dic)
    minimize(main_dic)
    
    