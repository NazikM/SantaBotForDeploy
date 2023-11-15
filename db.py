import sqlite3
import random
con = sqlite3.connect("santaBot.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS santaBot(id INTEGER PRIMARY KEY AUTOINCREMENT, group_name TEXT, name TEXT, name_id TEXT, organizer BOOLEAN, wish_list TEXT)")


def addToDB(group_name, name, name_id, organizer):
    cur.execute("INSERT INTO santaBot (group_name, name, name_id, organizer) VALUES (?, ?, ?, ?)", (group_name, name, name_id, organizer))
    con.commit()


def checkGroupExists(group_name):
    cur.execute("SELECT 1 FROM santaBot WHERE group_name = ?", (group_name,))
    result = cur.fetchone()
    return result is not None


def checkUserExists(name_id):
    cur.execute("SELECT 1 FROM santaBot WHERE name_id = ?", (name_id,))
    result = cur.fetchone()
    return result is not None


def checkUserExistsInGroup(name_id, group_name):
    cur.execute("SELECT 1 FROM santaBot WHERE name_id = ? AND group_name = ?", (name_id, group_name))
    result = cur.fetchone()
    return result is not None


def checkOrganizerByUserID(name_id):
    cur.execute("SELECT organizer FROM santaBot WHERE name_id = ? AND organizer = 1", (name_id,))
    result = cur.fetchone()
    return result is not None


def getGroupNameByUserID(name_id):
    cur.execute("SELECT group_name FROM santaBot WHERE name_id = ?", (name_id,))
    result = cur.fetchone()
    if result is not None:
        return result[0]  # Повертаємо перший стовпець (group_name)
    else:
        return None  # Якщо запис не знайдено, повертаємо None


def getNamesByGroup(group_name):
    cur.execute("SELECT name FROM santaBot WHERE group_name = ?", (group_name,))
    results = cur.fetchall()
    user_names = [name[0] for name in results]
    return user_names


def getNameIdByName(name, group_name):
    cur.execute("SELECT name_id FROM santaBot WHERE name = ? AND group_name = ?", (name, group_name))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None


def getOrganizerGroup(group_name):
    cur.execute("SELECT name_id FROM santaBot WHERE group_name = ? AND organizer = 1", (group_name,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None



def addWishListByUserID(name_id, wish_list):
    cur.execute("UPDATE santaBot SET wish_list = ? WHERE name_id = ?", (wish_list, name_id))
    con.commit()


def getWishListByName(name, group_name):
    cur.execute("SELECT wish_list FROM santaBot WHERE name = ? AND group_name = ?", (name, group_name))
    result = cur.fetchone()
    print(result)
    if result and result[0]:
        return result[0]  # Повертаємо значення поля `wish_list`
    else:
        return "Я чекаю щось чудове, я тобі довіряю🤗"


def deleteRecordsByGroupName(group_name):
    cur.execute("DELETE FROM santaBot WHERE group_name = ?", (group_name,))
    con.commit()


def close_db():
    cur.close()
    con.close()