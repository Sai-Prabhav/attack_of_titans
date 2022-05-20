from sql_lib import battle


class weapon:
    def __init__(self, damage):
        self.damage = damage


class agent:
    def __init__(self, name,hp, damage):
        self.name=name
        self.hp = hp
        self.weapon = weapon(damage)


agent1 = agent("hi1",200, 15)
agent2 = agent("bye",100, 12)

print(battle(agent1, agent2)[0], battle(agent1, agent2)[1].name)
