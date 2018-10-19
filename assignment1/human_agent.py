from agent import BaseAgent


class Human(BaseAgent):
    def choose_next_option(self):
        next_state = input("Choose next step:")
        return int(next_state)