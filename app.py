import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml

st.set_page_config(
    page_title="Data Science Bootcamp",
    page_icon=":dolphin:",
    layout="wide",
    initial_sidebar_state="expanded",
)
##database localhost connection
##@st.cache()
def get_database_connection():
    db = mysql.connect(host = "remotemysql.com",
                      user = "3UqmzRLpO8",
                      passwd = "UjLqejDHNn",
                      database = "3UqmzRLpO8",
                      auth_plugin='mysql_native_password')
    cursor = db.cursor()
    
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall() ## it returns a list of all databases present
    #print(databases)

    return cursor, db

cursor, db = get_database_connection()

cursor.execute("SHOW DATABASES")
databases = cursor.fetchall() ## it returns a list of all databases present
#st.write(databases)



def get_database_connection():
    db = mysql.connect(host = db_credintials['host'],
                      user = db_credintials['user'],
                      passwd = db_credintials['passwd'],
                      database = db_credintials['database'],
                      auth_plugin= db_credintials['auth_plugin'])
    cursor = db.cursor()

    return cursor, db





def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="c191012" and password=='c191012':
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from information where re_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                st.write(i[1])
                st.write(i[2])
                Accept=st.button('Accept',key=i[0])
                if Accept:
                    st.write('Accepted')
                    cursor.execute(f"Update information set status='Accepted' where id='{i[0]}'")
                    db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                    st.write('Rejected')
                    cursor.execute(f"Update information set status='Rejected' where id='{i[0]}'")
                    db.commit()

        else:
            st.sidebar.warning('Wrong Credintials')


def registration():
    id=uuid4()
    id=str(id)[:10]
    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        re_date=st.date_input('Registration Date')
        status='In Progress'
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO information (id,studentname,
                                                re_date,status) VALUES ('{id}','{sname}',
                                                '{re_date}','{status}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")
        

def status():
    id=st.text_input('Your Registration Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from information where id='{id}'")
        table=cursor.fetchall()
        st.write(table)








def main():
    cols1, cols2, cols3 = st.columns((1, 4, 1))
    cols2.title('Diploma in Data Science Admission Portal')
    cols2.write('Data Science Bootcamp')
    st.sidebar.header('Select your requirement')
        
    selected=st.sidebar.selectbox('',
                        ('Select',
                        'Admin Panel',
                        'Student Registration',
                        'Status Check'
                        ))
    if selected=='Admin Panel':
        admin()
    elif selected=='Student Registration':
        registration()
    elif selected=='Status Check':
        status()


   


if __name__ == '__main__':
    main()



