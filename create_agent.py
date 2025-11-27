import pygame
from human_agent import HumanAgent
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from expectimax_agent import ExpectimaxAgent

def create_agent(mode, player_type):
    if mode == "Human":
        return HumanAgent(player_type)
    if mode == "Random":
        return RandomAgent(player_type)
    if mode == "Minimax":
        return MinimaxAgent(player_type, depth=3)
    if mode == "Expectimax":
        return ExpectimaxAgent(player_type, depth=3)
    raise ValueError("Unknown agent type: " + mode)
