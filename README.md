# HtN_BE_Challenge_Submission

Goals were to create a script to setup and intially load the database based on an input JSON file, then design an API to update and retrieve information from the database.

#### Note about Load Database.py 
Load_Database.py expects the file "HTN_2023_BE_Challenge_Data.json" in the cwd (where its run from, not necessarily where its located)

### Language / Tools:
Using Python since I have used python libraries with json and REST in the past, also memory efficiency and class structure are not neccesities, no technical limitation encouraging use of C/C++
Will try SQLite for database since it was recommended and easy to install

### Database schema:
Three Tables:

Table A (name, contact information etc.)

User_id	(primary key) | Name | Company | email | phone |

- Primary Key: Userid = dictionary index / place in original json -> incase people have the same name / company, email and phone may change / be updated

Table B (Skill Ratings)

Skill_id (primary_key) | User_id | Skill_Name | Rating |

- Different total number of skills than everything else, will need a different primary id to track -> new table
- Link to table A with User_id for user info queries

Table C (Skills data)
Skill_Name (Primary_id)	| Frequency

- Make a separate table to keep track of skill frequencies
- Frequency will be calculated as we insert the JSON file, and updated as necessary

#### Table C Discussion:
Frequency could also be calculated without the use of Table C using a query like the one mentionned here: https://stackoverflow.com/questions/12344795/count-the-number-of-occurrences-of-a-string-in-a-varchar-field with Table B. However, since we know that the participants' skills are unlikely to change over time, and the majority of the participants' data is available initially, its more efficient to calculate frequency at the start with Python and update Table C as skills are modified rather than run a complicated and time consuming SQL query every time we need to access the frequency.
