import sys
from collections import OrderedDict

# CONVENTII:
# -> Neterminalele se noteaza cu litere mari
# -> Terminalele se noteaza cu litere mici
# -> Prima regula trecuta in fisier este regula de start
# Introducerea regulilor se face astfel:
# simbol_stanga simboluri_dreapta_1 simboluri_dreapta_2 (simbolurile din dreapta separate prin sau)
# lambda se noteaza prin $

class AST:
    def __init__(self, head):
        self.head = head

    def print_preorder(self, node, indent=0):
        print(indent * " ", node)
        for child in node.children:
            self.print_preorder(child, indent + 2)

class ASTNode:
    def __init__(self, value=None, parent=None, children=[]):
        self.value = value
        self.parent = parent
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def print_children(self, indent):
        print(self.children)

    def __repr__(self):
        return f'ASTNode({self.value})'

    def __str__(self):
        return f'ASTNode({self.value})'

current_node = ASTNode()
ast = AST(current_node)
left_derivation_rules = []
position = 0

def first(s):
    return next(iter(s))

def isnonterminal(letter):
    return letter.isupper() or letter == '$'

def read_language(filename):
    rules_dictionary = OrderedDict()
    with open(filename) as f:
        number_of_rules = list(map(int, f.readline().strip().split(" ")))[0]
        for _ in range(number_of_rules):
            input_line = f.readline().strip().split(" ")
            rules_dictionary[input_line[0]] = input_line[1:]
    return rules_dictionary

def apply_rule(word, rule, rules, indent):
    global position
    global left_derivation_rules
    global current_node
    if rule == '$':
        return
    #print(" " * indent, f'{rule}->{"|".join(rules[rule])}')
    all_productions_bad = True

    for production in rules[rule]:
        bad_production = False
        position_add = 0
        current_node.value = rule
        print(" " * indent, f'Trying production {rule}->{production}')
        left_derivation_rules.append(f'{rule}->{production}')
        for letter in production:
            if isnonterminal(letter):
                indent += 4
                next_node = ASTNode(letter, current_node, [])
                current_node.add_child(next_node)
                current_node = current_node.children[-1]

                bad_production = apply_rule(word, letter, rules, indent)

                current_node = current_node.parent
                indent -= 4
                if bad_production:
                    break
            elif position < len(word) and letter == word[position]:
                next_node = ASTNode(letter, current_node, [])
                current_node.add_child(next_node)
                position_add += 1
                position += 1
            else:
                bad_production = True 
                break
        if bad_production:
            left_derivation_rules.pop()
            position -= position_add
            print(" " * indent, f'Bad production')
        else:
            all_productions_bad = False
            print(" " * indent, f'Good production')
            break

    return all_productions_bad
    

if __name__ == '__main__':
    input_file = sys.argv[1]
    word = sys.argv[2]
    language_rules = read_language(input_file)
    #print(language_rules)
    apply_rule(word, first(language_rules), language_rules, 0)
    if position < len(word):
        print("CUVANTUL INTRODUS ESTE INCORECT SINTACTIC")
    else:
        print("CUVANTUL A PUTUT FI DERIVAT")
        print(left_derivation_rules)
        ast.print_preorder(ast.head)