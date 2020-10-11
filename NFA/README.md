# NONDETERMINISTIC FINITE AUTOMATA SIMULATOR

## How It Works
This Program Takes an input file representing an NFA with the following format: 
```
3 4 # number of states and number of transitions
0 1 b # following lines describe a transition as <first_state> <second_state> <transition_token> <transition_token> ...
0 0 a b
1 2 b
2 2 a b
0 # initial states
2 # final states
```


