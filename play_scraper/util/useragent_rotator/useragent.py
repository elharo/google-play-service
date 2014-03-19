__author__ = 'Grainier Perera'
import random
import requests


def get_available_agents(url):
    agents_list = requests.get(url).content
    available_agents = [agent.rstrip('\r') for agent in agents_list.split('\n')]
    return available_agents
    pass


def get_random_agent(url):
    available_agents = get_available_agents(url)
    random.seed()
    random_agent = available_agents[random.randint(0, len(available_agents) - 1)]
    if random_agent == '':
        random_agent = get_random_agent(url)
        pass
    return random_agent
    pass
