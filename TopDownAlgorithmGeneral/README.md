# Top Down General Parser (with Backtracking)

## How It Works

This program takes an input representing a grammar from a file and an arithmetic equation and prints a left-most derivation, the abstract syntax tree resulting from the algorithm
or an error message if the synthax is incorrect.

## Grammar File Rules

1. Non-Terminal Symbols are capital letters
2. Lambda (None) is represented by the dollar sign ($)
2. The File Format is The Following
```
5 # number of rules in the grammar
E TX # a rule E->TX
X +TX -TX $ # a rule X->+TX|-TX
T FY
Y *FY /FY $
F (E) a b c d e f g h i j k l m n o p q r s t u v w x y z
```

Execution:
```
python3 main.py <grammar_file> <equation> 
python3 main.py input.txt "a+b-3*4+(8-2)"
```



