import sqlite3

connect_ = sqlite3.connect('../Backend/UDIS.db')
cursor_ = connect_.cursor()

cursor_.execute("DROP TABLE all_courses")

cursor_.execute("""
            CREATE TABLE all_courses
            (sub_code text UNIQUE, course_name text, prof_name text, credits int)""")