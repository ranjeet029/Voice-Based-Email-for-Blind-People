import mysql.connector
from flask import session

class user_operation:
    def connection(self):
        con=mysql.connector.connect(host="127.0.0.1",port="3306",user="root",password="root",database="v_mail")
        return con
# -----------------------Connection Established------------------------------------------------------------
    # ------------------user-------------------------------------------------
    def user_signup(self,name,email,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into user (name,email,password) values(%s,%s,%s)"
        record=[name,email,password]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()

    def user_login(self,email,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select name,email from user where email=%s and password=%s"
        record=[email,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        rc=mycursor.rowcount
        if(rc==0):
            return 0
        else:
            session['name']=row[0][0]
            session['email']=row[0][1]
            return 1
        
    def user_send_mail(self,receiver,subject,message):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into mail (name,sender,receiver,subject,message) values(%s,%s,%s,%s,%s)"
        record=[session['name'],session['email'],receiver,subject,message]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()

    def user_inbox_mails(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select mail_id,name,sender,receiver,subject,message,created_at from mail where receiver=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row