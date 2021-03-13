import mysql.connector
def DataValue(email , contact, event, place):
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
    sql = "INSERT INTO website_customer_contact_info (email, mobile, event_info, place_info) VALUES (%s,%s,%s,%s)"
    val = (email, contact, event, place)
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")
    return 1

