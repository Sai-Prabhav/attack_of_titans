import psycopg2
import discord
import discord.ext.commands as commands
import numpy
import os
import asyncio
from dotenv import load_dotenv
from time import sleep


load_dotenv()


connection = psycopg2.connect(
    database="d1stpqngp1fuph", user='tawuenamkzawue', password=os.getenv("PASSWD"), host="ec2-52-214-125-106.eu-west-1.compute.amazonaws.com", port='5432'
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM test2")
print(cursor.fetchall())

# hard coded data
armours = {
    0: {
        "id": 0,
        "name": None,
        "defense": 0,
        "recipe": None
    },
    1: {
        "id": 1,
        "name": ["wooden armour"],
        "defense": 25,
        "recipe": [
            {
                "id": 1,  # id of stone
                "quantity": 15
            },
            {
                "id": 0,  # id of wood
                "quantity": 30
            }
        ]
    },
    2: {
        "id": 2,
        "name": " stone armour",
        "defense": 50,
        "recipe": [
            {
                "id": 3,  # id of hard stone
                "quantity": 45
            },
            {
                "id": 2,  # id of hard wood
                "quantity": 15
            }
        ]
    }
}
weapons = {
    0: {
        "id": 0,
        "name": None,
        "damage": 0,
        "recipe": None
    },
    1: {
        "id": 1,
        "name": "wooden sword",
        "damage": 10,
        "recipe": [
            {
                "id": 1,  # id of  stone
                "quantity": 15
            },
            {
                "id": 2,  # id of hard wood
                "quantity": 30
            }
        ]
    },
    2: {
        "id": 2,
        "name": " stone sword",
        "damage": 25,
        "recipe": [
            {
                "id": 3,  # id of hard stone
                "quantity": 45
            },
            {
                "id": 0,  # id of wood
                "quantity": 15
            }
        ]
    }

}
items = {
    0: {
        "id": 0,
        "name": ["wood"],
    },
    1: {
        "id": 1,
        "name": ["stone"],
    },
    2: {
        "id": 2,
        "name": ["hard wood"],
        "recipe": [
            {
                "id": 0,
                "quantity": 2

            }
        ]
    },
    3: {
        "id": 3,

        "name": ["hard stone"],
        "recipe": [
            {
                "id": 1,
                "quantity": 2
            }
        ]

    },
    4: {
        "id": 4,
        "name": ["fish"],
    },
    5: {
        "id": 5,
        "name": ["monster flesh"],
        "sell": 100
    },
    6: {
        "id": 6,
        "name": ["monster heart"],
    },
    7: {
        "id": 7,
        "name": ["life potion"],
        "sell": 50,
        "buy": 100,
        "use": lambda user: set_hp(user.id, user.max_hp)
    }

}

quests = {
    0: {
        "id": 0,
        "name": "no quest",
        "function": None,
        "description": None,
        "reward": None
    }
}


# functions to fetch data from database


class armour:
    def __init__(self, armourID):
        self.id = armourID
        self.name = armours[armourID]["name"]
        self.defense = armours[armourID]["defense"]
        self.recipe = armours[armourID]["recipe"]


class weapon:
    def __init__(self, weaponID):
        self.id = weaponID
        self.name = weapons[weaponID]["name"]
        self.damage = weapons[weaponID]["damage"]
        self.recipe = weapons[weaponID]["recipe"]


class quest:
    def __init__(self, questID):
        self.id = questID
        self.name = quests[questID]["name"]
        self.description = quests[questID]["description"]
        self.reward = quests[questID]["reward"]


class item:
    def __init__(self, itemID):
        self.id = itemID
        self.name = items[itemID]["name"]
        self.sell_price = items[itemID].get("sell")
        self.buy_price = items[itemID].get("buy")
        self.recipe = items[itemID].get("recipe")
        self.use = items[itemID].get("use")


print(item(4).name)


def isUser(id):
    cursor.execute("SELECT id FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone() is not None


def get_name(id):

    cursor.execute("SELECT name FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def get_base(id):

    cursor.execute("SELECT base FROM test2 WHERE id = %s", (id,))
    return numpy.array(cursor.fetchone()[0], dtype=int)


def set_base(id, base):

    cursor.execute("UPDATE test2 SET base = %s WHERE id = %s",
                   (base.tolist(), id))
    connection.commit()


def get_armour(id):

    cursor.execute("SELECT armourID FROM test2 WHERE id = %s", (id,))
    return armour(cursor.fetchone()[-1])


def set_armour(id, armour):

    cursor.execute(
        "UPDATE test2 SET armourID = %s WHERE id = %s", (armour.id, id))
    connection.commit()


def get_weapon(id):

    cursor.execute("SELECT weaponID FROM test2 WHERE id = %s", (id,))
    return weapon(cursor.fetchone()[-1])


def set_weapon(id, weapon):

    cursor.execute(
        "UPDATE test2 SET weaponID = %s WHERE id = %s", (weapon.id, id))
    connection.commit()


def get_inventory(id):

    cursor.execute("SELECT inv FROM test2 WHERE id = %s", (id,))
    item_list = cursor.fetchone()
    item = {}
    return item


def set_inventory(id, item):
    lists = []
    for keys, values in item:
        lists.append([keys, values])

    cursor.execute(
        "UPDATE test2 SET itemID = array%s WHERE id = %s", (str(lists), id))
    connection.commit()


def get_level(id):

    cursor.execute("SELECT level FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_level(id, level):

    cursor.execute("UPDATE test2 SET level = %s WHERE id = %s", (level, id))
    connection.commit()


def get_hp(id):

    cursor.execute("SELECT hp FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_hp(id, hp):

    cursor.execute("UPDATE test2 SET hp = %s WHERE id = %s", (hp, id))
    connection.commit()


def get_money(id):

    cursor.execute("SELECT money FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_money(id, money):

    cursor.execute("UPDATE test2 SET money = %s WHERE id = %s", (money, id))
    connection.commit()


def get_xp(id):

    cursor.execute("SELECT xp FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_xp(id, xp):

    cursor.execute("UPDATE test2 SET xp = %s WHERE id = %s", (xp, id))
    connection.commit()


def get_strength(id):

    cursor.execute("SELECT strength FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_strength(id, strength):

    cursor.execute(
        "UPDATE test2 SET strength = %s WHERE id = %s", (strength, id))
    connection.commit()


def get_numb_kills(id):

    cursor.execute("SELECT numb_kills FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_kills(id, numb_kills):

    cursor.execute(
        "UPDATE test2 SET numb_kills = %s WHERE id = %s", (numb_kills, id))
    connection.commit()


def get_numb_stone(id):

    cursor.execute("SELECT stone_mine FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_stone(id, numb_stones):

    cursor.execute(
        "UPDATE test2 SET stone_mine = %s WHERE id = %s", (numb_stones, id))
    connection.commit()


def get_numb_wood(id):

    cursor.execute("SELECT wood_chop FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_wood(id, numb_wood):

    cursor.execute(
        "UPDATE test2 SET wood_chop = %s WHERE id = %s", (numb_wood, id))
    connection.commit()


def get_quest(id):

    cursor.execute("SELECT questid FROM test2 WHERE id = %s", (id,))
    return quest(cursor.fetchone()[0])


def set_quest(id, quest):

    cursor.execute("UPDATE test2 SET questID = %s WHERE id = %s", (quest, id))
    connection.commit()


def get_quest_progress(id):

    cursor.execute("SELECT quest_progress FROM test2 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_quest_progress(id, quest_progress):

    cursor.execute(
        "UPDATE test2 SET quest_progress = %s WHERE id = %s", (quest_progress, id))
    connection.commit()


class user:
    def __init__(self, user):
        if not isUser(user.id):
            base = numpy.zeros([10, 10], dtype=int)  # 0 reperesent empty space
            base[5, 5] = 1  # 1 represents the bed
            self.userID = user.id
            self.name = user.name
            self.inventory = [[]]
            self.level = 1
            self.xp = 0
            self.hp = 90+10*self.level
            self.max_hp = 90+10*self.level
            self.base = base
            self.strength = 0
            self.armour = 0
            self.weapon = 0
            self.money = 0
            self.numb_kills = 0
            self.numb_wood = 0
            self.numb_stone = 0
            self.quest = 0
            self.quest_progress = 0
            return None
        self.userID = userID
        self.name = get_name(userID)
        self.inventory = get_inventory(userID)
        self.level = get_level(userID)
        self.xp = get_xp(userID)
        self.hp = get_hp(userID)
        self.max_hp = 90+10*self.level
        self.base = get_base(userID)
        self.strength = get_strength(userID)
        self.armour = get_armour(userID)
        self.weapon = get_weapon(userID)
        self.money = get_money(userID)
        self.numb_kills = get_numb_kills(userID)
        self.numb_wood = get_numb_wood(userID)
        self.numb_stone = get_numb_stone(userID)
        self.quest = get_quest(userID)
        self.quest_progress = get_quest_progress(userID)

    def __str__(self):
        return f"""
        Name: {self.name}
        Level: {self.level}
        XP: {self.xp}
        HP: {self.hp}/{self.max_hp}
        Strength: {self.strength}
        Armour: {armour(self.armour).name}
        Weapon: {weapon(self.weapon).name}
        Money: {self.money}
        Number of kills: {self.numb_kills}
        Number of wood: {self.numb_wood}
        Number of stone: {self.numb_stone}
        Quest: {quest(self.quest).name}
        Quest progress: {self.quest_progress}
        """

    def update(self):
        self.name = discord.get_user(userID).name
        self.inventory = get_inventory(userID)
        self.level = get_level(userID)
        self.xp = get_xp(userID)
        self.hp = get_hp(userID)
        self.base = get_base(userID)
        self.strength = get_strength(userID)
        self.armour = get_armour(userID)
        self.weapon = get_weapon(userID)
        self.money = get_money(userID)
        self.numb_kills = get_numb_kills(userID)
        self.numb_wood = get_numb_wood(userID)
        self.numb_stone = get_numb_stone(userID)
        self.quest = get_quest(userID)
        self.quest_progress = get_quest_progress(userID)


# sai = user(512354988157103763)
# print(sai)
