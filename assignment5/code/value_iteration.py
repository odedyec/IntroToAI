from copy import deepcopy


def single_epoch(sim):
    new_table = deepcopy(sim.utility)
    for state in sim.utility:
        if sim.is_state_terminal(state):
            new_table[state] = sim.get_terminal_reward(state)
            continue
        actions = sim.get_all_actions(state)
        best_action = -100000
        for action in actions:
            best_action = max(best_action, sim.get_utility_for_action(state, action))
        new_table[state] = best_action + sim.reward
    return sim.update_utility(new_table)


def value_iteration(sim, num_of_iterations, eps=0.1, show_delta=False):
    print("Starting value iteration for %d Epochs"%num_of_iterations)
    deltas = []
    while num_of_iterations:
        delta = single_epoch(sim)
        deltas.append(delta)
        if delta < eps:
            break
        num_of_iterations -= 1
    print("Finished value iteration after %d Epochs" % num_of_iterations)
    if show_delta:
        from matplotlib import pyplot as plt
        plt.plot(deltas)
        plt.show()


if __name__ == '__main__':
    class Simulator:
        def __init__(self):
            self.actions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            self.utility = {}
            self.deadzones = [(1, 1)]
            self.terminals = [(2, 3), (1, 3)]
            self.terminal_rewards = [100, -100]
            for i in range(3):
                for j in range(4):
                    state = (i, j)
                    # if state in self.deadzones:
                    #     continue
                    self.utility[state] = 0.
            self.reward = -3

        def update_utility(self, new_table):
            diff = 0.
            for key in new_table:
                diff += abs(new_table[key] - self.utility[key])
            self.utility = new_table
            return diff

        def get_utility_for_action(self, state, action):
            if state in self.deadzones:
                return 0
            reward_sum = 0.
            new_state = self.state_based_on_action(state, action)
            reward_sum += self.utility[new_state] * 0.8
            if abs(action[0]):
                action2 = (0, 1)
                action3 = (0, -1)
            else:
                action2 = (1, 0)
                action3 = (-1, 0)
            new_state = self.state_based_on_action(state, action2)
            reward_sum += self.utility[new_state] * 0.1
            new_state = self.state_based_on_action(state, action3)
            reward_sum += self.utility[new_state] * 0.1
            return reward_sum

        def get_all_actions(self, state):
            return self.actions

        def is_state_terminal(self, state):
            if state in self.terminals:
                return True
            return False

        def get_terminal_reward(self, state):
            for i in range(len(self.terminals)):
                    if state in [self.terminals[i]]:
                        return self.terminal_rewards[i]

        def state_based_on_action(self, state, action):
            if self.is_state_terminal(state):
                return state

            new_state = (state[0] + action[0], state[1] + action[1])
            if new_state in self.deadzones or new_state[0] > 2 or new_state[0] < 0 or new_state[1] < 0 or new_state[1] > 3:
                return state
            return new_state

        def print_as_table(self):
            s = ''
            for i in range(2, -1, -1):
                for j in range(4):
                    if (i, j) in self.deadzones:
                        s += '{} '.format('x').rjust(5)
                    else:
                        s += '{:4.0f} '.format(self.utility[(i,j)])
                s += '\n'
            print (s)



    sim = Simulator()
    sim.print_as_table()
    value_iteration(sim, 100, show_delta=True)
    sim.print_as_table()