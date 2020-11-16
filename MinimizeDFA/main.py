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

    def minimize(self):
        minimization_table = [[None for i in range(self.number_of_states)] for j in range(self.number_of_states)] 
        for state in self.final_states:
            for other_state in range(self.number_of_states):
                if other_state not in self.final_states:
                    minimization_table[state][other_state] = minimization_table[other_state][state] = 0
        can_be_marked = True
        step_counter = 0
        while can_be_marked:
            step_counter += 1
            can_be_marked = False
            for i in range(self.number_of_states):
                for j in range(self.number_of_states):
                    if i == j:
                        continue
                    if minimization_table[i][j] is None:
                        for possible_input_value in self.input:
                            state_reached_for_i = None
                            state_reached_for_j = None
                            for k in range(self.number_of_states):
                                if possible_input_value in self.states_matrix[i][k]:
                                    state_reached_for_i = k
                                if possible_input_value in self.states_matrix[j][k]:
                                    state_reached_for_j = k
                            if minimization_table[state_reached_for_i][state_reached_for_j] is not None:
                                can_be_marked = True
                                minimization_table[i][j] = step_counter
                                break

        # Add New Unified States
        new_states = []
        for i in range(self.number_of_states):
            for j in range(self.number_of_states):
                if i >= j:
                    continue
                if minimization_table[i][j] is None:
                    state_for_i = None
                    state_for_j = None
                    for k in range(len(new_states)):
                        if i in new_states[k]:
                            state_for_i = k
                        if j in new_states[k]:
                            state_for_j = k
                    if state_for_i and state_for_j:
                        continue
                    if state_for_i is not None:
                        new_states[state_for_i].append(j)
                    elif state_for_j is not None:
                        new_states[state_for_j].append(i)
                    else:
                        new_states.append([i, j])

        # Add Old States
        for i in range(self.number_of_states):
            for j in range(self.number_of_states):
                if i >= j: 
                    continue
                i_already_appears = False
                j_already_appears = False
                for state in new_states:
                    if i in state:
                        i_already_appears = True
                    if j in state:
                        j_already_appears = True
                if not i_already_appears:
                    new_states.append([i])
                if not j_already_appears:
                    new_states.append([j])
        print(new_states)

        new_states_matrix = [[[] for i in range(len(new_states))] for j in range(len(new_states))]
        for i in range(len(new_states)):
            for j in range(len(new_states)):
                # Find a transition between state i and state j and add it to the new matrix
                for state1 in new_states[i]:
                    for state2 in new_states[j]:
                        if len(self.states_matrix[state1][state2]) != 0:
                            for el in self.states_matrix[state1][state2]:
                                if el not in new_states_matrix[i][j]:
                                    new_states_matrix[i][j].append(el)
        self.states_matrix = new_states_matrix

        new_initial_states = []
        new_final_states = []
        for i in range(len(new_states)):
            for state in new_states[i]:
                if state in self.initial_states and state not in new_final_states:
                    new_initial_states.append(i)
                    break

        for i in range(len(new_states)):
            for state in new_states[i]:
                if state in self.final_states and state not in new_final_states:
                    new_final_states.append(i)
                    break

        self.initial_states = new_initial_states
        self.final_states = new_final_states
        self.number_of_states = len(new_states)
        
        unreachable_states = []
        for state in range(self.number_of_states):
            can_be_reached = False
            for other_state in range(self.number_of_states):
                if state == other_state:
                    continue
                else:
                    if len(self.states_matrix[other_state][state]) != 0:
                        can_be_reached = True
            if not can_be_reached:
                unreachable_states.append(state)

        i = 0
        while i < len(self.states_matrix):
            if i in unreachable_states:
                self.states_matrix.pop(i)
                i -= 1
            i += 1

        for state in unreachable_states:
            if state in self.final_states:
                self.final_states.remove(state)
            if state in self.initial_states:
                self.initial_states.remove(state)

if __name__ == '__main__':
    automata_dict = read_automata(sys.argv[1])
    automata = DFA(automata_dict["states_matrix"], automata_dict["initial_states"], automata_dict["final_states"])
    automata.minimize()
    print("NEW ADJACENCY MATRIX:")
    for row in automata.states_matrix:
        print(row)
    print(f"NEW INITIAL STATES: {automata.initial_states}")
    print(f"NEW FINAL STATES: {automata.final_states}")
