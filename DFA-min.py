from re import sub
from tabulate import tabulate
from NFA_DFA import get_sigma,complete,trans_table

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
    
    