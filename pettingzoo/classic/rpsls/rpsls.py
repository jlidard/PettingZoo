from gym.spaces import Discrete
import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector

rock = 0
paper = 1
scissors = 2
lizard = 3
spock = 4
MOVES = ["ROCK", "PAPER", "SCISSORS", "LIZARD", "SPOCK"]
NUM_ITERS = 100


class env(AECEnv):
    """Two-player environment for rock paper scissors lizard spock.
    The observation is simply the last opponent action."""

    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.num_agents = 2
        self.agents = list(range(0, self.num_agents))
        self.agent_order = list(range(0, self.num_agents))

        self.action_spaces = {agent: Discrete(5) for agent in self.agents}
        self.observation_spaces = {agent: Discrete(5) for agent in self.agents}

        self.display_wait = 0.0
        self.reinit()

    def reinit(self):
        self._agent_selector = agent_selector(self.agent_order)
        self.agent_selection = self._agent_selector.next()
        self.rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: 0 for agent in self.agents}
        self.num_moves = 0

    def render(self, mode="human"):
        print("Current state: Agent1: {} , Agent2: {}".format(MOVES[self.state[0]], MOVES[self.state[1]]))

    def observe(self, agent):
        # observation of one agent is the state of the other
        return self.state[1 - agent]

    def close(self):
        pass

    def reset(self, observe=True):
        self.reinit()
        if observe:
            return self.observe(0)

    def step(self, action, observe=True):
        agent = self.agent_selection
        if np.isnan(action):
            action = 0
        elif not self.action_spaces[agent].contains(action):
            raise Exception('Action for agent {} must be in Discrete({}).'
                            'It is currently {}'.format(agent, self.action_spaces[agent].n, action))
        self.state[self.agent_selection] = action

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            self.rewards[0], self.rewards[1] = {
                (rock, rock): (0, 0),
                (rock, paper): (-1, 1),
                (rock, scissors): (1, -1),
                (rock, lizard): (1, -1),
                (rock, spock): (-1, 1),

                (paper, rock): (1, -1),
                (paper, paper): (0, 0),
                (paper, scissors): (-1, 1),
                (paper, lizard): (-1, 1),
                (paper, spock): (1, -1),

                (scissors, rock): (-1, 1),
                (scissors, paper): (1, -1),
                (scissors, scissors): (0, 0),
                (scissors, lizard): (1, -1),
                (scissors, spock): (-1, 1),

                (lizard, rock): (-1, 1),
                (lizard, paper): (1, -1),
                (lizard, scissors): (-1, 1),
                (lizard, lizard): (0, 0),
                (lizard, spock): (1, -1),

                (spock, rock): (1, -1),
                (spock, paper): (-1, 1),
                (spock, scissors): (1, -1),
                (spock, lizard): (-1, 1),
                (spock, spock): (0, 0),
            }[(self.state[0], self.state[1])]

            self.num_moves += 1
            self.dones = {agent: self.num_moves >= NUM_ITERS for agent in self.agents}

        self.agent_selection = self._agent_selector.next()
        if observe:
            return self.observe(self.agent_selection)
