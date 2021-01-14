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

    def print_preorder(self):
        self._print_preorder(self.head, 0)

    def _print_preorder(self, node, indent=0):
        print(indent * " ", node)
        for child in node.children:
            self._print_preorder(child, indent + 2)

    def get_number_of_children(self):
        return len(children)

    def copy_tree(self):
        head_node = ASTNode(self.head.value, None, [])
        ast = AST(head_node)
        self._copy_tree(ast.head, self.head)
        return ast

    def _copy_tree(self, copying_node, copied_node):
        copying_node.value = copied_node.value
        for child in copied_node.children:
            copying_node.children.append(ASTNode(parent=copying_node, children=[]))
            self._copy_tree(copying_node.children[-1], child)

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

def apply_rule(word, rule, rules, indent, position):
    if rule == '$':
        return
    #print(" " * indent, f'{rule}->{"|".join(rules[rule])}')
    position_add = 0
    good_productions = []
    for production in rules[rule]:

        print(" " * indent, f'Trying production {rule}->{production}')
        possible_productions = [position]

        for letter in production:
            if isnonterminal(letter):
                new_possible_productions = []
                for position in possible_productions:
                    results = apply_rule(word, letter, rules, indent + 4, position)
                    for next_production in results:
                        new_possible_productions.append(next_production) 
                possible_productions = new_possible_productions
                if len(possible_productions) == 0:
                    break
            else:
                new_possible_productions = []
                for possible_production in possible_productions:
                    if possible_production < len(word) and letter == word[possible_production]:
                        new_possible_productions.append(possible_production + 1)
                possible_productions = new_possible_productions

        if len(possible_productions) > 0:
            print(" " * indent, 'Production Worked!')
        else:
            print(" " * indent, 'Production Failed!')
        good_productions = good_productions + possible_productions
     
    return good_productions
    

if __name__ == '__main__':
    input_file = sys.argv[1]
    word = sys.argv[2]
    print(f"INPUT_PHRASE: {word}")
    language_rules = read_language(input_file)
    ast_head = ASTNode(None, None, [])
    ast = AST(ast_head)
    possible_productions = apply_rule(word, first(language_rules), language_rules, 0, 0)
    word_can_be_derived = False
    for el in possible_productions:
        if el == len(word):
            word_can_be_derived = True
            break
    if word_can_be_derived:
        print("THE WORD WAS DERIVED SUCCESFULLY")
    else:
        print("THE WORD IS INCORRECT SINTACTICALLY")
