import sys

def read_automata(filename):
    states_matrix = None
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
        

    return {"final_states": final_states, "initial_states": initial_states, "states_matrix": states_matrix}

class DFA:
    def __init__(self, states_matrix, initial_states, final_states):
        self.states_matrix = states_matrix
        self.initial_states = initial_states
        self.final_states = final_states
        self.number_of_states = len(self.states_matrix)
        self.input = []
        self._get_possible_input()

    def _get_possible_input(self):
        for row in self.states_matrix:
            for input_list in row:
                for input_value in input_list:
                    if input_value not in self.input:
                        self.input.append(input_value)

    def convert_to_regex(self):
        list_of_final_states_conversions = [self.compute_r(1, i, self.number_of_states) for i in self.final_states]
        return "|".join(list_of_final_states_conversions)

    def compute_r(self, i, j, k, indent=1):
        if k == 0:
            print(" " * indent, f'i:{i}, j:{j}, k:{k}', end=" ")
            trajectory_content = [el for el in self.states_matrix[i-1][j-1]]
            if i == j:
                trajectory_content.insert(0, 'λ')
            if len(trajectory_content) == 0:
                trajectory_content.append("Ø")
            
            result_string = "|".join(trajectory_content)
            if len(trajectory_content) > 1:
                result_string = "(" + result_string + ")" 
            print(result_string)
            return result_string
        print(" " * indent, f'i:{i}, j:{j}, k:{k}')
        indent *= 2
        return self.compute_r(i, j, k-1, indent) + '|' + self.compute_r(i, k, k-1, indent) + '(' + self.compute_r(k, k, k-1, indent) + ')*' + self.compute_r(k, j, k-1, indent)
        indent /= 2


if __name__ == '__main__':
    automata_dict = read_automata(sys.argv[1])
    automata = DFA(automata_dict["states_matrix"], automata_dict["initial_states"], automata_dict["final_states"])
    print(automata.states_matrix)
    print("RESULTING REGEX:")
    print(automata.convert_to_regex())
