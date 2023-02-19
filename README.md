# HtN_BE_Challenge_Submission
###Language / Tools:
Using Python since I have used python libraries with json and REST in the past, also memory efficiency and class structure are not neccesities, no technical limitation encouraging use of C/C++
Will try SQLite for database since it was recommended and easy to install

###Database schema:
Three Tables:

	a) name, contact information etc.

User_id	(primary key) | Name | Company | email | phone |

-Primary Key: Userid = dictionary index / place in original json -> incase people have the same name / company, email and phone may change / be updated

	b) Skill Ratings

Skill_id (primary_key) | User_id | Skill_Name | Rating |

-Different total number of skills than everything else, will need a different primary id to track -> new table
-Link to table A with User_id for user info queries

c) Skills data
Skill_Name (Primary_id)	| Frequency

-Make a separate table to keep track of skill frequencies
-Calculate skill frequency field with a query like this: https://stackoverflow.com/questions/12344795/count-the-number-of-occurrences-of-a-string-in-a-varchar-field
-Frequency will be calculated from table B, but no need to link them with a common field