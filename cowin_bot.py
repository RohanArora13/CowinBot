from keep_alive import keep_alive
import requests
import json
import time
import sqlite3
from sqlite3 import Error
import os
import random
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Host: cdn-api.co-vin.in
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0
# Accept: application/json, text/plain, */*
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate, br
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI3OWE4YzJhOC1hMjU1LTRhNjktYTQ5Yi0yYjk0NzQ3NDVhYTEiLCJ1c2VyX2lkIjoiNzlhOGMyYTgtYTI1NS00YTY5LWE0OWItMmI5NDc0NzQ1YWExIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5MDI5OTk1MTc4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjU1OTc3ODAwNTIzOTQwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjo4OC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94Lzg4LjAiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0wOFQxODo0NjoxMC41MzNaIiwiaWF0IjoxNjIwNDk5NTcwLCJleHAiOjE2MjA1MDA0NzB9.hbBEbYy8xn7Kmbsy2I6Gl_SyYMQHqnNSUWTVlVGC_Kk
# Origin: https://selfregistration.cowin.gov.in
# Connection: keep-alive
# Referer: https://selfregistration.cowin.gov.in/


#{'center_id': 606906, 'name': 'DAHISAR COVID JUMBO -10', 'address': 'Dahisar', 
# 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R North Corporation - MH',
#  'pincode': 400068, 'lat': 19, 'long': 72, 'from': '09:00:00', 'to': '17:00:00', 'fee_type': 'Free',
#  'sessions': [{'session_id': '13109ccd-0f24-482d-9eab-147174ab0f37', 'date': '15-05-2021', 'available_capacity': 0,
#  'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM',
#  '03:00PM-05:00PM']}]}


db_name = "center.db"
table="already_send"
# Dynamically setting API to check Centers for next 4 days 
check_date = []
dt = int(str(datetime.date.today())[-2:])
for i in range(4):
    check_date.append(dt+i)

def create_database(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(table_name):
    global db_name
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    table_command = """
    CREATE TABLE {tableName} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        center_no INTERGER NOT NULL,
        date DATE NOT NULL)
     """.format(tableName=table_name)

    cur.execute(table_command)
    con.close()
    print('table created')




def checkDBandTable():
    global db_name,table

    con = sqlite3.connect(db_name)

    # checking database
    if not (os.path.isfile(db_name)):
        print('creating database')
        try:
            create_database(db_name)
        except:
            print('error creating databases')

     # commit the changes to db
    con.commit()
    # close the connection
    con.close()
    # checking table

    con = sqlite3.connect(db_name)
    
    c = con.cursor()
    # get the count of tables with the name
    c.execute( ''' SELECT count(name) FROM sqlite_master  WHERE type ='table' AND name ='{tableName}' '''.format(dbName=db_name , tableName = table) )

    # if the count is 1, then table exists
    if c.fetchone()[0] == 1:
            print('Table exists.')

    else:
            print('creating table .')
            try:
                create_table(table)

            except BaseException as e:
                print("error creating table")
                print(str(e))

        

    # commit the changes to db
    con.commit()
    # close the connection
    con.close()


def updateDB(center_no,checkDate):
    global db_name,table
    con = sqlite3.connect(db_name)
    c = con.cursor()

    #  CREATE TABLE {tableName} (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     center_no INTERGER NOT NULL,
    #     date DATE NOT NULL)

    c.execute( ''' INSERT OR IGNORE INTO {tableName} (center_no,date)  VALUES ('{center_no}','{date}') '''.format(
        tableName = table,
        center_no=center_no,
        date=datetime.date(2021, 5, checkDate))
        )

    con.commit()
    con.close()


#{'center_id': 606906, 'name': 'DAHISAR COVID JUMBO -10', 'address': 'Dahisar', 
# 'state_name': 'Maharashtra', 'district_name': 'Mumbai', 'block_name': 'Ward R North Corporation - MH',
#  'pincode': 400068, 'lat': 19, 'long': 72, 'from': '09:00:00', 'to': '17:00:00', 'fee_type': 'Free',
#  'sessions': [{'session_id': '13109ccd-0f24-482d-9eab-147174ab0f37', 'date': '15-05-2021', 'available_capacity': 0,
#  'min_age_limit': 45, 'vaccine': 'COVISHIELD', 'slots': ['09:00AM-11:00AM', '11:00AM-01:00PM', '01:00PM-03:00PM',
#  '03:00PM-05:00PM']}]}

#sending mail
def send_mail(one_center,checkDate):
    print('sending mail')

    fromaddr = "rsachannel11@gmail.com"

    #people to send
    toaddr = ["prathameshvhanmane@gmail.com","rohanarora1313@gmail.com","rihit555@digdig.org","amitarora399@gmail.com","karandikarshreyash@gmail.com","Barcelonapratik@gmail.com","saurabhvirola@gmail.com",""]

    #dropped_df=final_df.drop(['State'], axis=1)

    sess = one_center['sessions']
    session = sess[0]

    #print(one_center)

    body = "Hii Rohan Cowin Bot Update,<br>"+"-------Vaccine Available at------<br>"+"center = "+str(one_center["name"])+"<br>address = "+str(one_center["address"])+"<br>available_capacity = "+str(session["available_capacity"])+"<br>fee_type = "+str(one_center["fee_type"])+"<br>vaccine company = "+str(session["vaccine"])+"<br>age_limit = "+str(session["min_age_limit"])+"<br>date= "+str(session["date"])+"<br>slots = "+str(session["slots"])

    print(body)
    for dest in toaddr:
        try:
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = dest
            msg['Subject'] = "CoWinBot Vaccine Available at - "+str(one_center['name'])
            msg.attach(MIMEText(body, 'html'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromaddr, "wtckvmwhgkhuakth")
            text = msg.as_string()
            s.sendmail(fromaddr, dest, text)
            s.quit()
            time.sleep(2)
        except:
            print('mail sent failed to '+str(dest))
            pass
    
    print('mail sent')

    updateDB(one_center['center_id'],checkDate)




def send_message(age,isFree,one_center,checkDate):
    global db_name,table
    #print(one_center)
    #print(checkDate)

    #checking in DB

    center_no = one_center['center_id']
    

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM {table} WHERE center_no = {center_no} AND date ={date}'.format(
        table = table,
        center_no = center_no,
        date = datetime.date(2021, 5, checkDate)
    ))

    row = cur.fetchall()
    conn.commit()
    conn.close()

    if len(row) <= 0:
        print("There are no results for this query")
        # send mail
        send_mail(one_center,checkDate)

    else:
        print('entry found')



    # center_id
    # check db if already send for today


def send_error_message(info):
    print(info)

    fromaddr = "rsachannel11@gmail.com"

    #people to send
    toaddr = ["rohanarora1313@gmail.com","rihit555@digdig.org"]

    body="COWIN BOT ERROR "+info

    for dest in toaddr:
        try:
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = dest
            msg['Subject'] = "CoWinBot Error"
            msg.attach(MIMEText(body, 'html'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(fromaddr, "wtckvmwhgkhuakth")
            text = msg.as_string()
            s.sendmail(fromaddr, dest, text)
            s.quit()
            time.sleep(2)
        except:
            print('mail sent failed')
            pass



def call_api(checkDate):

    resp = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=395&date='+str(checkDate).zfill(2)+'-05-2021',headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "content-type":"text",
    "Accept-Language":"en-US",
    "Origin":"https://selfregistration.cowin.gov.in",
    "Connection":"keep-alive",
    "Referer":"https://selfregistration.cowin.gov.in/",
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI3OWE4YzJhOC1hMjU1LTRhNjktYTQ5Yi0yYjk0NzQ3NDVhYTEiLCJ1c2VyX2lkIjoiNzlhOGMyYTgtYTI1NS00YTY5LWE0OWItMmI5NDc0NzQ1YWExIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5MDI5OTk1MTc4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjU1OTc3ODAwNTIzOTQwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjo4OC4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94Lzg4LjAiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0wOFQxODo0NjoxMC41MzNaIiwiaWF0IjoxNjIwNDk5NTcwLCJleHAiOjE2MjA1MDA0NzB9.hbBEbYy8xn7Kmbsy2I6Gl_SyYMQHqnNSUWTVlVGC_Kk"
    })

    print(resp.url)

    if resp.status_code != 200:
        # This means something went wrong.
        # retry after 5 mins and send message
        if(resp.status_code != 401):
            send_error_message('GET /tasks/ {} date={}'.format(resp.status_code,checkDate))
            time.sleep(100)
            check_API()
        
    else:
        json_data = resp.json()
        centerLoop(json_data,checkDate)


def check_API():
    global check_date

    #loop throught dates
    for date in check_date:
        call_api(date)
        #todo remove 

    time.sleep(random.randint(100,150))
    check_API()



def centerLoop(full_list,checkDate):
    
    #print center 1
    #print(json_dict_list[0])

    center_dict_list = full_list.get('centers')

    # loop
    for one_center in center_dict_list:
        print('checking center')
        #print(one_center)

        #print(one_center['center_id'])

        session = one_center['sessions']
        " Free or Paid "
        money = one_center['fee_type']
        isFree = False
        if(money.lower() == "free"):
            isFree = True
        else:
            isFree = False

        session_dict = session[0]

        # 'available_capacity': 0, 'min_age_limit': 45

        available =  session_dict['available_capacity']
        age = session_dict['min_age_limit']

        #checking avaiable and sending message etc

        if available > 0 and age <=18:
            print('vaccine avaiable')
            print('ae'+str(age))
            send_message(age,isFree,one_center,checkDate)
            #todo remove
        else:
            print('not found')

#send_mail('','')

#keep_alive()

checkDBandTable()
check_API()
#send_error_message('Bot Started ....')


# if resp.status_code != 200:
#     # This means something went wrong.
#     # retry after 10 mins
#     raise Exception('GET /tasks/ {}'.format(resp.status_code))
# else:
#     json_string=resp.json()

#     # list of all centers in dict
#     json_dict_list = json_string.get('centers')

#     #total centers
#     #print(len(json_dict_list))

#     #print center 1
#     #print(json_dict_list[0])

#     # get dict
#     #print(len(json_dict_list))
#     one_center = json_dict_list[4]

#     session = one_center['sessions']
#     " Free or Paid "
#     money = one_center['fee_type']
#     #print(money)
#     session_dict = session[0]
#     #print (session_dict)

#     # 'available_capacity': 0, 'min_age_limit': 45,
#     #print (session_dict['available_capacity'])
#     #print (session_dict['min_age_limit'])
#     centerLoop(json_string)

