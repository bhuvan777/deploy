import mysql.connector

def DataValue(email):
    mydb = mysql.connector.connect(
        host="eventtow.cfex2mlqblie.ap-south-1.rds.amazonaws.com",
        user="root",
        password="10578014",
        port="3306",
        database="eventtow")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user where email=%s", [email])
    result = mycursor.fetchone()
    return result

