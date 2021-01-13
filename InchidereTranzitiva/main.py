import sys

class Pair:

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return f'P({self.first}, {self.second})'

class Relation:

    def __init__(self, alphabet, pairs=[]):
        self.pairs = pairs
        self.alphabet = alphabet

    def __str__(self):
        return f'R({", ".join(list(map(str, self.pairs)))})'

    def add_pair(self, pair):
        self.pairs.append(pair)

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

if __name__ == '__main__':
    filename = sys.argv[1]
    r = None
    with open(filename) as f:
        alphabet = f.readline().strip().split(" ")
        r = Relation(alphabet)
        number_of_pairs_in_relation = int(f.readline().strip())
        for _ in range(number_of_pairs_in_relation):
            input_line = f.readline()
            first, second = input_line.strip().split(" ")
            pair = Pair(first, second)
            r.add_pair(pair)
    print("Initial Relation: ", r)
    transitive_closure_relation = r.compute_transitive_closure()
    print("Transitive Closure Relation: ", transitive_closure_relation)
    transitive_reflexive_closure_relation = r.compute_transitive_reflexive_closure()
    print("Transitive Reflexive Closure Relation: ", transitive_reflexive_closure_relation)

