import mysql.connector
def DataValue(name, email, date_info, event_info, place_info, price_info, allow):
    mydb = mysql.connector.connect(
        host="eventtow-restore.cfex2mlqblie.ap-south-1.rds.amazonaws.com",
        user="root",
        password="10578014",
        port="3306",
        database="eventtow")
    mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM user where email=%s", [email])
    # result = mycursor.fetchone()
    # return result
    sql = "INSERT INTO web_customer ( name_info,email,date_info, event_info, place_info, price_info,allow) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (name, email, date_info, event_info, place_info, price_info, allow)
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")
    return 1

