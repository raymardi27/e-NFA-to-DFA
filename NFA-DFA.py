from re import sub  #this is to get the i/p in the inner dict loop in main
from tabulate import tabulate #this is for printing transition tables

def get_sigma(transitions,n=0):#To get the alphabet
    max = 'q0'
    if n == 1:
        max = 'A0'
    Transitions = transitions
    for i in Transitions:
        if len(Transitions[max]) < len(Transitions[i]):
            max = i
        for j in Transitions[i]:
            if j not in Transitions[max]:
                Transitions[max][j] = "-"
    sigma = list()
    for i in Transitions[max]:
        sigma.append(i)
    return sorted(sigma)

def complete(transitions,sigma): #to complete the table as in put in None where no value is present
    for i in transitions:
        for ele in sigma:
            if ele not in transitions[i]:
                transitions[i][ele] = "-"
    return transitions

def trans_table(transitions,n=0):#To print the transition table
    sigma = get_sigma(transitions,n)
    Transitions = complete(transitions,sigma)
    Pri_List,count = [],0
    state = 'q'
    if n == 1:
        state = 'A'
    for i in Transitions:
        row = [state+str(count)]
        for j in sigma:
            row.append(Transitions[i][j])
        Pri_List.append(row)
        count+=1
    print(tabulate(Pri_List,headers=sigma))
    
def get_closure(transitions):#To calculate epsilon closure values
    sigma = get_sigma(transitions)
    if 'eps' not in sigma:
        return
    Transitions = complete(transitions,sigma)
    for i in Transitions:
        eps_list = [i]
        if Transitions[i]['eps'] != '-':
            eps_list+=(Transitions[i]['eps'])
            for j in eps_list:#Iterates over the list we just got to access their eps lists.
                if Transitions[j]['eps'] != '-':
                    eps_list+=(Transitions[j]['eps'])   
        Transitions[i]['~eps-closure'] = sorted(list(set(eps_list)))
    return Transitions
    
def form_DFA(transitions):#to convert eps-NFA to DFA
    sigma = get_sigma(transitions)
    print("Conversion Started")
    if 'eps' not in sigma:
        print("This is not an epsilon NFA. Sorry the code won't work.")
        return 
    Transitions = complete(transitions,sigma) #is copy to make sure that original data is not accidentally overwritten
    cigma,new_states,new_states_added,aux_list,new_dict,aux,count = sigma,list(),list(),list(),dict(),dict(),0
    cigma.remove('eps');cigma.remove(' Stat');cigma.remove('~eps-closure')
    final_state = []
    for i in Transitions:
        if Transitions[i][' Stat'] == 'Ini' or Transitions[i][' Stat'] == 'Ini & Fin':
            new_states.append(Transitions[i]['~eps-closure'])
            new_states_added = new_states[0]
        if Transitions[i][' Stat'] == 'Fin' or Transitions[i][' Stat'] == 'Ini & Fin':
            final_state.append(i)
    unique_state = True
    print("Came upto 'Unique State'")
    while unique_state:
        state = 'A'+str(count)
        aux[state] = new_states_added
        aux_list.append(new_states_added)
        count+=1
        inner_dict = dict()
        for j in cigma:
            state_val = list()
            for i in new_states_added:
                if Transitions[i][j] not in state_val and Transitions[i][j] != '-':
                    state_val+=Transitions[i][j]
            val_list = list()
            for i in state_val:
                if Transitions[i]['~eps-closure'] not in val_list:
                    val_list+= Transitions[i]['~eps-closure']
            inner_dict[j] = val_list
            if val_list not in new_states:
                new_states.append(val_list)
        new_dict[state] = inner_dict
        unique_state = False
        for i in new_states:
            if i not in aux_list:
                new_states_added = i
                unique_state = True
                break 
    test_dict = new_dict
    for i in aux:
        for j in final_state:
            if j in aux[i]:
                new_dict[i][' Stat'] = 'Final'
            else:
                new_dict[i][' Stat'] = ''
    for i in test_dict:
        for j in cigma:
            test_dict[i][j] = list(aux.keys())[list(aux.values()).index(test_dict[i][j])]
    trans_table(new_dict,1)
    for i in aux:
        print("with ",i,'=',end="")
        if aux[i] == []:
            print(" Null")
        else:
            print(aux[i])
    # print_DFA_tt(new_dict,aux)
        
# def print_DFA_tt(transitions,aux):
#     cigma = get_sigma(transitions,1)
#     Pri_list,header_list = [],[' ']
#     for i,j in zip(transitions,aux):
#         row = [j]
#         row.append(transitions[i][' Stat'])
#         for k in cigma:
#             header_list.append(k)
#             for st,val in aux.items():
#                 if val == transitions[i][k]:
#                     row.append(st)
#         Pri_list.append(row)
#     header_list = sorted(list(set(header_list)))
#     print(tabulate(Pri_list,headers=header_list))

            

if __name__ == "__main__":
    file = open("data2.txt",'r+')
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
    main_dic = get_closure(main_dic)
    trans_table(main_dic)
    print("\n\nConverting to DFA...\n")
    form_DFA(main_dic)
            


