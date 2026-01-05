
import mysql.connector
try:
    myconn = mysql.connector.connect(host = "localhost", user = "root",password ='123456',port='3306',
                            auth_plugin='mysql_native_password')  
  
    #printing the connection object   
    print(myconn)  
    print('connected-1')
except:
    print('not connected')
mycursor = myconn.cursor()

mycursor.execute("CREATE DATABASE afreendb")
print('database created successfully')