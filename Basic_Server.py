import sqlite3
import json
from flask import Flask, request

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

def Specific_User_query(Input_User):
    conn = sqlite3.connect("HTN_BE_Challenge.db")
    #TODO make sure connection was sucessful
    curs = conn.cursor()

    Query_string = "SELECT * FROM Personal_Info WHERE user_id = '" + str(Input_User) + "'"

    res = curs.execute(Query_string)
    personal_info_values = res.fetchone()
    personal_info_formatted = []
    temp_dict = {}
    temp_dict["user_id"] = personal_info_values[0]
    temp_dict["name"] = personal_info_values[1]
    temp_dict["company"] = personal_info_values[2]
    temp_dict["email"] = personal_info_values[3]
    temp_dict["phone"] = personal_info_values[4]
    personal_info_formatted.append(temp_dict.copy())

    Query_string = "SELECT * FROM User_Skills WHERE user_id = '" + str(Input_User) + "'"
    res = curs.execute(Query_string)
    skill_values = res.fetchall()
    temp_dict = {}
    temp_list = []
    for skill_index in skill_values:
        temp_dict["skill"] = skill_index[2]
        temp_dict["rating"] = skill_index[3]
        temp_list.append(temp_dict.copy())

    personal_info_formatted[0]["skills"] = temp_list.copy()

    output_json = json.dumps(personal_info_formatted)
    return output_json

def Update_User_query(Input_User, Input_Dict):
    conn = sqlite3.connect("HTN_BE_Challenge.db")
    #TODO make sure connection was sucessful
    curs = conn.cursor()
    #input_dict = json.loads(Input_JSON)

    #Update Personal Info
    if "name" in Input_Dict:
        Query_string = "UPDATE Personal_Info SET name = '" + Input_Dict["name"] +  "' WHERE user_id = '" + str(Input_User) + "'"
        curs.execute(Query_string)
        conn.commit()
    if "company" in Input_Dict:
        Query_string = "UPDATE Personal_Info SET company = '" + Input_Dict["company"] +  "' WHERE user_id = '" + str(Input_User) + "'"
        curs.execute(Query_string)
        conn.commit()
    if "email" in Input_Dict:
        Query_string = "UPDATE Personal_Info SET email = '" + Input_Dict["email"] +  "' WHERE user_id = '" + str(Input_User) + "'"
        curs.execute(Query_string)
        conn.commit()
    if  "phone" in Input_Dict:
        Query_string = "UPDATE Personal_Info SET phone = '" + Input_Dict["phone"] +  "' WHERE user_id = '" + str(Input_User) + "'"
        curs.execute(Query_string)
        conn.commit()

    #assuming skills inputted as "skills"[ {"skill":"skill_name1", "rating": rating_value1} ] NOT {"skill":"skill_name", "rating": rating_value}
    if "skills" in Input_Dict:
        Input_skills_list = Input_Dict["skills"]
        Current_skills_list = []

        Query_string = "SELECT * FROM User_Skills WHERE user_id = '" + str(Input_User) + "'"
        res = curs.execute(Query_string)
        Skill_values = res.fetchall()

        for skill_index in Skill_values:
            Current_skills_list.append(skill_index[2])

        for skill_index in Input_skills_list:
            print(skill_index)
            if skill_index["skill"] in Current_skills_list:
                #Update Existing Skill
                Query_string = "UPDATE User_Skills SET rating = " + str(skill_index["rating"]) +  " WHERE user_id = '" + str(Input_User) + "' AND Skill_name = '" + skill_index["skill"] +"'"
                curs.execute(Query_string)
                conn.commit()
            else:
                #Add new Skill
                #Get max skill id
                Query_string = "SELECT MAX(Skill_id) FROM User_Skills"
                res = curs.execute(Query_string)
                max_id = res.fetchone()

                Query_string = "INSERT INTO User_Skills VALUES ( " + str(max_id[0] + 1) + ", " + str(Input_User) + ", '" + skill_index["skill"] + "', " + str(skill_index["rating"]) + ")"
                curs.execute(Query_string)
                conn.commit()

                #Update Skills Info Table
                #Check if it exists
                Query_string = "SELECT * FROM Skills_Info"
                res = curs.execute(Query_string)

                #Add an '_C' to distinguish variables that take values from Skills Info aka Table C
                All_skills_dict_C = {}
                All_skill_values_C = res.fetchall()
                #Retrieve Current Skills and their frequency
                for skill_index_all_C in All_skill_values_C:
                    All_skills_dict_C[skill_index_all_C[1]] = skill_index_all_C[2]

                if skill_index["skill"] in All_skills_dict_C.keys():
                    #Update Frequency if it Exists
                    Query_string = "UPDATE Skills_Info SET Frequency = " + str(All_skills_dict_C[skill_index["skill"]] + 1) +  " WHERE Skill_Name = '" + skill_index["skill"] +"'"
                    curs.execute(Query_string)
                    conn.commit()
                else:
                    Query_string = "SELECT MAX(Skill_Number) FROM Skills_Info"
                    res = curs.execute(Query_string)
                    max_id = res.fetchone()

                    Query_string = "INSERT INTO Skills_Info VALUES ( " + str(max_id[0] + 1) + ", '" + skill_index["skill"] + "', 1 )"
                    curs.execute(Query_string)
                    conn.commit()

@app.route('/')
def Placeholder():
    return 'Hello'

@app.get('/users')
def All_Users():
    All_users_output = All_Users_query()
    return All_users_output

@app.route('/test', methods=['GET', 'POST'])
@app.route('/users/<int:user_id>', methods=['GET', 'PUT'])
def Get_Specific_User(user_id):
    if request.method == 'PUT':
        Update_json = request.get_json()
        Update_User_query(user_id, Update_json)

    Specific_user_output = Specific_User_query(user_id)
    return Specific_user_output

@app.route('/test', methods=['GET', 'PUT'])
def test():
    if request.method == 'GET':
        return "get"
    elif request.method == 'PUT':
        print ("before processing")
        data = request.get_json()
        print(data)
        return "put"
