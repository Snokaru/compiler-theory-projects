import sys

class NFA:
    def __init__(self, states_matrix, initial_states, final_states):
        self.states_matrix = states_matrix
        self.initial_states = initial_states
        self.final_states = final_states
        self.number_of_states = len(self.states_matrix)

    def check_word(self, word):
        current_states = self.initial_states
        print(f"WORD: {word}")
        for token in word:
            print(f"CURRENT TOKEN: {token}; CURRENT STATES: {current_states}")
            token_is_ok = False
            next_states = []
            for state in current_states:
                for i in range(self.number_of_states):
                    if token in self.states_matrix[state][i]: 
                        token_is_ok = True
                        if i not in next_states:
                            next_states.append(i)
            if not token_is_ok:
                return False
            current_states = next_states
        print(f"FINAL STATES: {current_states}")
        
        for state in current_states:
            if state in final_states:
                return True
        return False
                        
if __name__ == '__main__':
    states_matrix = None
    filename = sys.argv[1]
    word = sys.argv[2]
    print(filename)
    with open(filename) as f:
        number_of_states, number_of_transitions = map(int, f.readline().strip().split(" "))
        states_matrix = [[[] for i in range(number_of_states)] for j in range(number_of_states)]
        for i in range(number_of_transitions):
            input_line = f.readline().strip().split(" ")
            first_state = int(input_line[0])
            second_state = int(input_line[1])
            states_matrix[first_state][second_state] = input_line[2:]
        initial_states = list(map(int, f.readline().strip().split(" ")))
        final_states = list(map(int, f.readline().strip().split(" ")))

    automata = NFA(states_matrix, initial_states, final_states)
    print(automata.check_word(word))
