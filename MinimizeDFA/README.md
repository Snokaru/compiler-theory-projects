# NONDETERMINISTIC FINITE AUTOMATA SIMULATOR

## How It Works



This program takes an input file representing a DFA with the following format: 
```
3 4 # number of states and number of transitions
0 1 b # following lines describe a transition as <first_state> <second_state> <transition_token> <transition_token> ...
0 0 a b
1 2 b
2 2 a b
0 # initial states
2 # final states
```
and a word and outputs whether the read word is part of the language represented by the automata.

Execution:
```
python3 main.py <automata_file>
```

Example:
```
python3 main.py input.txt abba
```


