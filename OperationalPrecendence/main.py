import sys
from collections import OrderedDict

class Pair:

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f'P({self.first}, {self.second})'

def isnonterminal(symbol, rules):
    for rule in rules:
        if rule == symbol:
            return True
    return False


class Relation:

    def __init__(self, alphabet, pairs=[]):
        self.pairs = pairs
        self.alphabet = alphabet

    def __str__(self):
        return f'R({", ".join(list(map(str, self.pairs)))})'

    def add_pair(self, pair):
        self.pairs.append(pair)

    def check_pair(self, pair):
        for p in self.pairs:
            if pair.first == p.first and pair.second == p.second:
                return True
        return False

    def compute_transitive_closure(self):
        resulting_relation = Relation(alphabet, [])
        
        # WE TREAT THE RELATION AS A DIRECTED GRAPH
        adjacency_matrix = [[False for _ in range(len(self.alphabet))] for _ in range(len(self.alphabet))]
        for i in range(len(self.alphabet)):
            for j in range(len(self.alphabet)):
                is_pair = False
                for pair in self.pairs:
                    if pair.first == self.alphabet[i] and pair.second == self.alphabet[j]:
                        is_pair = True
                        break
                if is_pair:
                    adjacency_matrix[i][j] = True

        # FLOYD-WARSHALL
        for k in range(len(self.alphabet)):
            for i in range(len(self.alphabet)):
                for j in range(len(self.alphabet)):
                    adjacency_matrix[i][j] = adjacency_matrix[i][j] or (adjacency_matrix[i][k] and adjacency_matrix[k][j])

        for i in range(len(self.alphabet)):
            for j in range(len(self.alphabet)):
                if adjacency_matrix[i][j]:
                    pair = Pair(self.alphabet[i], self.alphabet[j])
                    resulting_relation.add_pair(pair)
        
        return resulting_relation

    def compute_transitive_reflexive_closure(self):
        resulting_relation = self.compute_transitive_closure()
        for symbol in self.alphabet:
            relation_exists = False
            for pair in resulting_relation.pairs:
                if pair.first == symbol and pair.second == symbol:
                    relation_exists = True
                    break
            if not relation_exists:
                resulting_relation.add_pair(Pair(symbol, symbol))
        return resulting_relation


def read_language(filename):
    rules_dictionary = OrderedDict()
    with open(filename) as f:
        alphabet = f.readline().strip().split(" ")
        number_of_rules = list(map(int, f.readline().strip().split(" ")))[0]
        for _ in range(number_of_rules):
            input_line = f.readline().strip().split(" ")
            rules_dictionary[input_line[0]] = input_line[1:]
    return (alphabet, rules_dictionary)

def compute_F(alphabet, rules):
    F = Relation(alphabet, [])
    for x in alphabet:
        for y in alphabet:
            for rule in rules:
                for production in rules[rule]:
                    if rule == x and production[0] == y:
                        F.add_pair(Pair(x, y))
                        break
    return F

def compute_L(alphabet, rules):
    L = Relation(alphabet, [])
    for x in alphabet:
        for y in alphabet:
            for rule in rules:
                for production in rules[rule]:
                    if rule == x and production[-1] == y:
                        L.add_pair(Pair(x, y))
                        break
    return L

def compute_F_1_2(alphabet, rules):
    F = Relation(alphabet, [])
    for x in alphabet:
        for y in alphabet:
            for rule in rules:
                for production in rules[rule]:
                    if (rule == x and production[0] == y) or (rule == x and isnonterminal(production[0], rules) and (len(production) > 1 and production[1] == y)):
                        F.add_pair(Pair(x, y))
                        break
    return F

def compute_L_1_2(alphabet, rules):
    L = Relation(alphabet, [])
    for x in alphabet:
        for y in alphabet:
            for rule in rules:
                for production in rules[rule]:
                    if (rule == x and production[-1] == y) or (rule == x and isnonterminal(production[-1], rules) and (len(production) - 1 > 0 and production[-2] == y)):
                        L.add_pair(Pair(x, y))
                        break
    return L

def compute_precedence_relations(alphabet, rules):
    F = compute_F_1_2(alphabet, rules)
    L = compute_L_1_2(alphabet, rules)
    F_transitive = F.compute_transitive_closure()
    L_transitive = L.compute_transitive_closure()
    F_transitive_reflexive = F.compute_transitive_reflexive_closure()
    L_transitive_reflexive = L.compute_transitive_reflexive_closure()
    terminals = [symbol for symbol in alphabet if not isnonterminal(symbol, rules)]
    
    relation_table = {}
    for letter in terminals:
        relation_table[letter] = {}
    for x in terminals:
        for y in terminals:
            relation_table[x][y] = [] 

    for x in terminals:
        for y in terminals:
            # CHECK LESS THAN
            found_match = False
            for rule in rules:
                for production in rules[rule]:
                    for i in range(len(production)-1):
                        if production[i] == x and F_transitive.check_pair(Pair(production[i+1], y)):
                            found_match = True
                            relation_table[x][y].append(-1)
                            break
                    if found_match:
                        break
                if found_match:
                    break

            # CHECK EQUALS
            found_match = False
            for rule in rules:
                for production in rules[rule]:
                    for i in range(len(production)-2):
                        if production[i] == x and isnonterminal(production[i+1], rules) and production[i+2] == y:
                            found_match = True
                            relation_table[x][y].append(0)
                            break
                    if found_match:
                        break
                if found_match:
                    break

            # CHECK MORE THAN
            found_match = False
            for rule in rules: 
                for production in rules[rule]:
                    for i in range(len(production)-1):
                        if L_transitive.check_pair(Pair(production[i], x)) and F_transitive_reflexive.check_pair(Pair(production[i+1], y)):
                            found_match = True
                            relation_table[x][y].append(1)
                            break
                    if found_match:
                        break
                if found_match:
                    break
    return relation_table
 
                            
def print_table(alphabet, table):
    for x in alphabet:
        print(x, end=" ")
    print()
    for x in alphabet:
        print(x, end=" ")
        for y in alphabet:
            print(table[x][y], end=" ")
        print()


if __name__ == '__main__':
    input_file = sys.argv[1]
    alphabet, language_rules = read_language(input_file)
    table = compute_precedence_relations(alphabet, language_rules) 
    terminals = [symbol for symbol in alphabet if not isnonterminal(symbol, language_rules)]
    print_table(terminals, table)
