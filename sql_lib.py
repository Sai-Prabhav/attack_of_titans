import psycopg2
import discord
import numpy
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    database="d1stpqngp1fuph", user='tawuenamkzawue', password=os.getenv("PASSWD"), host="ec2-52-214-125-106.eu-west-1.compute.amazonaws.com", port='5432'
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM test1")
print(cursor.fetchall())

# functions to fetch data from database


def get_base(id):

    cursor.execute("SELECT base FROM test1 WHERE id = %s", (id,))
    return numpy.array(cursor.fetchone()[0], dtype=int)


def set_base(id, base):

    cursor.execute("UPDATE test1 SET base = %s WHERE id = %s",
                   (base.tolist(), id))
    connection.commit()


def get_armor(id):

    cursor.execute("SELECT armorID FROM test1 WHERE id = %s", (id,))
    return armour(cursor.fetchone()[-1])


def set_armor(id, armor):

    cursor.execute(
        "UPDATE test1 SET armorID = %s WHERE id = %s", (armor.id, id))
    connection.commit()


def get_weapon(id):

    cursor.execute("SELECT weaponID FROM test1 WHERE id = %s", (id,))
    weapon = weapon(cursor.fetchone())
    return weapon


def set_weapon(id, weapon):

    cursor.execute(
        "UPDATE test1 SET weaponID = %s WHERE id = %s", (weapon.id, id))
    connection.commit()


def get_inventory(id):

    cursor.execute("SELECT inv FROM test1 WHERE id = %s", (id))
    item_list = cursor.fetchone()
    item = {}
    for x in item_list:
        item[x[0]] = x[1]

    return item


def set_inventory(id, item):
    lists = []
    for keys, values in item:
        lists.append([keys, values])

    cursor.execute(
        "UPDATE test1 SET itemID = array%s WHERE id = %s", (str(lists), id))
    connection.commit()


def get_level(id):

    cursor.execute("SELECT level FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_level(id, level):

    cursor.execute("UPDATE test1 SET level = %s WHERE id = %s", (level, id))
    connection.commit()


def get_hp(id):

    cursor.execute("SELECT hp FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_hp(id, hp):

    cursor.execute("UPDATE test1 SET hp = %s WHERE id = %s", (hp, id))
    connection.commit()


def get_money(id):

    cursor.execute("SELECT money FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_money(id, money):

    cursor.execute("UPDATE test1 SET money = %s WHERE id = %s", (money, id))
    connection.commit()


def get_xp(id):

    cursor.execute("SELECT xp FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_xp(id, xp):

    cursor.execute("UPDATE test1 SET xp = %s WHERE id = %s", (xp, id))
    connection.commit()


def get_strength(id):

    cursor.execute("SELECT strength FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_strength(id, strength):

    cursor.execute(
        "UPDATE test1 SET strength = %s WHERE id = %s", (strength, id))
    connection.commit()


def get_numb_kills(id):

    cursor.execute("SELECT numb_kills FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_kills(id, numb_kills):

    cursor.execute(
        "UPDATE test1 SET numb_kills = %s WHERE id = %s", (numb_kills, id))
    connection.commit()


def get_numb_stone(id):

    cursor.execute("SELECT numb_stones FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_stone(id, numb_stones):

    cursor.execute(
        "UPDATE test1 SET numb_stones = %s WHERE id = %s", (numb_stones, id))
    connection.commit()


def get_numb_wood(id):

    cursor.execute("SELECT numb_wood FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_numb_wood(id, numb_wood):

    cursor.execute(
        "UPDATE test1 SET numb_wood = %s WHERE id = %s", (numb_wood, id))
    connection.commit()


def get_quest(id):

    cursor.execute("SELECT quest FROM test1 WHERE id = %s", (id,))
    return quest(cursor.fetchone()[0])


def set_quest(id, quest):

    cursor.execute("UPDATE test1 SET quest = %s WHERE id = %s", (quest.id, id))
    connection.commit()


def get_quest_progress(id):

    cursor.execute("SELECT quest_progress FROM test1 WHERE id = %s", (id,))
    return cursor.fetchone()[0]


def set_quest_progress(id, quest_progress):

    cursor.execute(
        "UPDATE test1 SET quest_progress = %s WHERE id = %s", (quest_progress, id))
    connection.commit()


class user:
    def __init__(self, userID):
        if not isUser(userID):
            base = numpy.zeros([10, 10], dtype=int)  # 0 reperesent empty space
            base[5, 5] = 1  # 1 represents the bed
            create_account(userID, discord.get_user(userID).name, [], base)
        self.userID = userID
        self.name = discord.get_user(userID).name
        self.inventory = get_inventory(userID)
        self.level = get_level(userID)
        self.xp = get_xp(userID)
        self.hp = get_hp(userID)
        self.max_hp = 100+10*self.level
        self.base = get_base(userID)
        self.strength = get_strength(userID)
        self.armor = get_armor(userID)
        self.weapon = get_weapon(userID)
        self.money = get_money(userID)
        self.numb_kills = get_numb_kills(userID)
        self.numb_wood = get_numb_wood(userID)
        self.numb_stone = get_numb_stone(userID)
        self.quest = get_quest(userID)
        self.quest_progress = get_quest_progress(userID)


class armor:
    def __init__(self, armorID):
        self.id = armorID
        self.name = armor_list[armorID]["name"]
        self.defence = armors_list[armorID]["defence"]
        self.recipe = armor_list[armorID]["recipe"]


class weapon:
    def __init__(self, weaponID):
        self.id = weaponID
        self.name = weapon_list[weaponID]["name"]
        self.damage = weapon_list[weaponID]["damage"]
        self.recipe = weapon_list[weaponID]["recipe"]


class quest:
    def __init__(self, questID):
        self.id = questID
        self.name = quest_list[questID]["name"]
        self.description = quest_list[questID]["description"]
        self.reward = quest_list[questID]["reward"]
