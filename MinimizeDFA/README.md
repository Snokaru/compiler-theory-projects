# NONDETERMINISTIC FINITE AUTOMATA SIMULATOR

## How It Works

This program takes an input file representing a complete DFA with the following format: 
```
8 15 # number of states and number of transitions
0 1 0 # following lines describe a transition as <first_state> <second_state> <transition_token> <transition_token> ...
0 2 1
1 6 1
1 2 0
2 3 0
2 5 1
3 5 0
3 4 1
4 4 1
4 5 0
5 5 0 1
6 1 0
6 2 1
7 0 0
7 6 1
0 # initial states
3 4 5 7 # final states
```
and outputs the states matrix, initial states and final states of the minimized DFA  

Execution:
```
python3 main.py <automata_file>
python3 main.py input.txt # example
```



