import mysql.connector as mc

def getNew():
    db = mc.connect(
    host ="localhost",
    user ="root",
    passwd ="1234"
    )

    MyCursor1 = db.cursor()
    MyCursor2 = db.cursor()

    a=MyCursor1.execute("CREATE DATABASE IF NOT EXISTS formParia")
    b=MyCursor2.execute("CREATE DATABASE IF NOT EXISTS formShahrad")

    
    MyCursor1.execute("show databases")
    result1=MyCursor1.fetchall()
    print(result1)

    MyCursor2.execute("show databases")
    result2=MyCursor2.fetchall()
    print(result2)

    db1 = mc.connect(
    host ="localhost",
    user ="root",
    passwd ="1234",
    database='formParia'
    )
    print(db1)

    db2 = mc.connect(
    host ="localhost",
    user ="root",
    passwd ="1234",
    database='formShahrad'
    )
    print(db2)

    MyCursor1 = db1.cursor()
    MyCursor2 = db2.cursor()

    MyCursor1.execute("create table formParia.resultParia (first_name NVARCHAR(50) ,last_name NVARCHAR(100) , phone_num NVARCHAR(11) , gender ENUM('Male','Female') , marital_status ENUM('Single','Married'), favorites VARCHAR(255))")
    MyCursor2.execute("create table formShahrad.resultShahrad (first_name NVARCHAR(50) ,last_name NVARCHAR(100) , phone_num NVARCHAR(11) , gender ENUM('Male','Female') , marital_status ENUM('Single','Married'), favorites VARCHAR(255))")
    MyCursor1.close()
    MyCursor2.close()
    db.close()
if __name__=="__main__":
    getNew()
