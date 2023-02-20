import sqlite3
import json
from flask import Flask

app = Flask(__name__)

def All_Users_query():
    conn = sqlite3.connect("HTN_BE_Challenge.db")
    #TODO make sure connection was sucessful
    curs = conn.cursor()
    res = curs.execute("SELECT * FROM Personal_Info")
    personal_info_values = res.fetchall()
    personal_info_formatted = []
    temp_dict = {}
    for person in personal_info_values:
        temp_dict["user_id"] = person[0]
        temp_dict["name"] = person[1]
        temp_dict["company"] = person[2]
        temp_dict["email"] = person[3]
        temp_dict["phone"] = person[4]
        personal_info_formatted.append(temp_dict.copy())

    res = curs.execute("SELECT * FROM User_Skills")
    skill_values = res.fetchall()
    temp_dict = {}
    temp_list = []
    prev_user_id = 0
    for skill_index in skill_values:
        if (prev_user_id == skill_index[1]):
            temp_dict["skill"] = skill_index[2]
            temp_dict["rating"] = skill_index[3]
            temp_list.append(temp_dict.copy())
        else:
            personal_info_formatted[prev_user_id]["skills"] = temp_list.copy()
            prev_user_id = skill_index[1]
            temp_list = []
            temp_dict["skill"] = skill_index[2]
            temp_dict["rating"] = skill_index[3]
            temp_list.append(temp_dict.copy())

    personal_info_formatted[prev_user_id]["skills"] = temp_list.copy()

    output_json = json.dumps(personal_info_formatted)
    return output_json


@app.route('/')
def Placeholder():
    return 'Hello'

@app.get('/users')
def All_Users():
    All_users = All_Users_query()
    return All_users