# Intro to AI assignment 1

## Main - game.py

run [game](https://github.com/odedyec/IntroToAI/blob/master/assignment1/game.py).py to run the program

In game.py, the global variables, K and agents, should be set to None if it is desired to get input from the terminal.
Otherwise, set the variables with values.

E.g., If you want to start the game with a human agent, change line 7 from

```Python
agents = []
```

to
```Python
agents = [Human(0)]
```

## Agents

All agents should inherit from the BaseAgent class in [agent.py](https://github.com/odedyec/IntroToAI/blob/master/assignment1/agent.py)

A new agent must implement the "choose_next_option(self, sim)" method. The method returns the next state to go to.

An agent is initialized with an initial state

### Human agent
The [human_agent.py](https://github.com/odedyec/IntroToAI/blob/master/assignment1/human_agent.py) asks the user to input the next state to go to
```Python
    def choose_next_option(self, sim=HurricaneSimulator()):
        print('You are at: ', sim.state)
        next_state = input("Choose next step:")
        return int(next_state)
````
