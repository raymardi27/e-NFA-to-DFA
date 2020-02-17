# e-NFA-to-DFA
Theory of Computation Assignment

Takes an epsilon-NFA as input and gives out a DFA as an output, in a neat tabular form

Input Format:
    "input":"list of states";"input":"list of states"
    Do NOT input an epsilon transition to the same state //TODO    Fix epsilon same state bug
    For no transition just put a ':'
    
Certain lines are commented out, they are for the input from the file. The format as given in the file is to be followed.
    Format is:
     "Number of States"
     "input along with transitions"
     "next input and so on" //format of input as mentioned above
     "initial state"
     "final state"
     
//TODO Minimize the DFA
