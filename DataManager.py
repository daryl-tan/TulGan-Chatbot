from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

connection = psycopg2.connect(
    user="fmxuapnxvhmaid",
    password="4a1050e297e63812a1f849adc372f784f1a4a61129a9cf7da5af3fcc5f94fe9f",
    host="ec2-3-231-16-122.compute-1.amazonaws.com",
    port="5432",
    database="dd2192jcv4qfvc"
)

insert_query = '''
            INSERT INTO Queries (date, query, tag, relevant)
            VALUES (%s, %s, %s, %s)
            '''

class DataManager():
    def __init__(self):
        self.cursor = connection.cursor()

    def store(self, inpt, tag, relevance=True):
        self.cursor.execute(insert_query, 
            (
                date.today(),
                inpt,
                tag,
                relevance
            )
        )
        connection.commit()

    def viewTable(self):
        self.cursor.execute(
            '''
            SELECT * FROM Queries
            '''
        )

        df = pd.DataFrame(self.cursor.fetchall(), 
            columns=['Date', 'Query', 'Tag', 'Relevance']
            )

        df.to_csv('data/data.csv')
        return df

    def sendEmail(self, TO):
        FROM = "wtvdummyacc@gmail.com"
        self.analyze()
        
        data = MIMEMultipart()
        data['From'] = FROM
        data['To'] = TO
        data['Subject'] = "Query Analysis"
        body = f"Query Analysis as of {date.today()}"

        data.attach(MIMEText(body, 'plain'))
        filename = "fig.png"
        attachment = open("data/fig.png", "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        data.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(FROM, "Dummy2020")
        s.sendmail(FROM, TO, data.as_string())
        s.quit()
 
    def analyze(self):
        df = self.viewTable()

        df_tag = df[["Tag", "Query"]] \
            .groupby('Tag') \
            .count() \
            .head(10)
        sns.set()
        plt.bar(x=df_tag.index, height=df_tag.Query)
        plt.xlabel('Tag')
        plt.ylabel('Frequency of Query')
        plt.title('Query Analysis')
        plt.savefig('data/fig.png')