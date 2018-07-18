import numpy as np
import random
import sys
import time


def find_in_ordering(ordering, target):
    return ordering.get(target)

def find_in_list(ordering, target):
    ind = 0
    for i in range(len(ordering)):
        if ordering[i] == target:
            ind = i
    return ind

def generate_init_state(n):
    # generate a random mapping of wizard indices to ordering position
    return {wizard: random_int for (wizard, random_int) in zip(range(n),np.random.choice(n, n, replace=False))}

def generate_constraints(input_file):
    fin = open(input_file, "r")

    num_wiz_in_input = int(fin.readline().split()[0])
    num_constraints = int(fin.readline().split()[0])

    storage = []
    wizard_set = set()
    for line in range(num_constraints):
        newcomp = fin.readline().split()
        storage.append(newcomp)
    for i in range (len(storage)):
        for wizard in storage[i]:
            wizard_set.add(wizard)

    wizard_list = list(wizard_set)
    constraints = []
    for line in storage:
        constraints.append([find_in_list(wizard_list, line[0]),
                            find_in_list(wizard_list, line[1]),
                            find_in_list(wizard_list, line[2])
                            ])
    return wizard_list, num_wiz_in_input, constraints

def convert_to_names(wizard_names, ordering):
    # convert from wizard indices back into wizard names
    ret = ["null" for i in range(len(wizard_names))]
    for i in range(len(wizard_names)):
        ret[ordering[i]] = wizard_names[i]
    return " ".join(ret)

class WizardProblem:
    def __init__(self, num_wizards, constraints, initial_state, epsilon = 0.1):
        self.num_wiz = num_wizards
        self.cons = constraints
        self.state = initial_state
        self.epsilon = epsilon
        self.unsatisfied_cons = self.unsatisfied()

    def choose_action(self):
        loop = True
        while loop:
            # find the wizards corresponding to a random unsatisfied constraint
            constraint = self.unsatisfied_cons[np.random.randint(len(self.unsatisfied_cons))]
            first_loc = find_in_ordering(self.state, constraint[0])
            second_loc = find_in_ordering(self.state, constraint[1])
            third_loc = find_in_ordering(self.state, constraint[2])

            # check how the constraint is not satisfied
            if first_loc < third_loc < second_loc:
                possible_actions = self.generate_actions(constraint[0], constraint[1], constraint[2], first_loc, second_loc, third_loc)
                if possible_actions:
                    loop = False
            elif second_loc < third_loc < first_loc:
                possible_actions = self.generate_actions(constraint[1], constraint[0], constraint[2], first_loc, second_loc, third_loc)
                if possible_actions:
                    loop = False
            else:
                raise RuntimeError("You should not be here. Something went wrong.")

        # choose a random action
        if random.random() < self.epsilon:
            action = possible_actions[np.random.randint(2)]
        else:
            # do the optimal action
            action_vals = [(self.calc_action_val(act), act) for act in possible_actions]
            sorted_actions = sorted(action_vals, key= lambda x: -x[0])
            action = sorted_actions[0][1]
        self.epsilon = max(.03, self.epsilon * .9999)
        return action

    def generate_actions(self, constraint0, constraint1, constraint2, first_loc, second_loc, third_loc):
        first_swaps = [(constraint2, constraint0)]
        second_swaps = [(constraint2, constraint1)]
        return first_swaps + second_swaps

    def calc_action_val(self, action):
        new_state = self.apply_action(action)
        return self.value(new_state)

    def value(self, state):
        num_fails = 0
        for constraint in self.cons:
            first_loc = find_in_ordering(state, constraint[0])
            second_loc = find_in_ordering(state, constraint[1])
            third_loc = find_in_ordering(state, constraint[2])
            if first_loc < third_loc < second_loc or second_loc < third_loc < first_loc:
                num_fails += 1
        return -num_fails

    def unsatisfied(self):
        # create a list of the unsatisfied constraints
        unsatisfied = []
        for constraint in self.cons:
            first_loc = find_in_ordering(self.state, constraint[0])
            second_loc = find_in_ordering(self.state, constraint[1])
            third_loc = find_in_ordering(self.state, constraint[2])
            if first_loc < third_loc < second_loc or second_loc < third_loc < first_loc:
                unsatisfied.append(constraint)
        return unsatisfied

    def apply_action(self, action):
        # non-destructive method which returns what the state would be if the given action was applied
        state_copy = dict(self.state)
        x = action[0]
        y = action[1]
        state_copy[x], state_copy[y] = self.state.get(y), self.state.get(x)
        return state_copy

    def do_action(self, action):
        self.state = self.apply_action(action)
        self.unsatisfied_cons = self.unsatisfied()

def solve_problem(problem, max_time):
    start = time.time()
    val = -1
    # run until all constraints are met or we have exceeded our max time
    while time.time() - start < max_time and val < 0:
        act = problem.choose_action()
        problem.do_action(act)
        val = problem.value(problem.state)
        # to help monitor how the program is doing
        print(str(val) + " | " + str(problem.epsilon))

    return val, problem.state, time.time() - start

def main(argv):
    start = time.time()
    while True:
        wizard_names, num_wizards, cons = generate_constraints(argv[0])
        problem = WizardProblem(num_wizards, constraints=cons, initial_state=generate_init_state(num_wizards))
        val, result, t = solve_problem(problem, max_time=np.sqrt(len(cons)) * 10)
        if val >= 0:
            print("SUCCESS")
            print(convert_to_names(wizard_names, result))
            print("ITERATION TIME: " + str(time.time() - start))
            break
        else:
            print("FAILURE IN: " + str(t) + " FOR " + str(val) + " CONSTRAINTS")
    print("TOTAL TIME: " + str(time.time() - start))

if __name__ == '__main__':
    main(sys.argv[1:])
