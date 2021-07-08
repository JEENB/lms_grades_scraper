from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import getpass
from selenium.webdriver.common.by import By
import pandas as pd
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib

#### Tasks left
### Excetpion handelling: 1) Password or email-id error
### 2) emailing grades error

sem_data = []
user_data = []
email = str(input("Email: "))
pswd = getpass.getpass('Password: ')

def gradesScraper():
    
    

    driver = webdriver.Chrome("./chromedriver.exe")
    driver.get("https://registration.ashoka.edu.in/")

    # driver.implicitly_wait(30)

    #Allocate email fierld and enter email 
    email_Field = driver.find_element_by_id("identifierId")
    email_Field.send_keys(email)
    email_Field.send_keys(Keys.RETURN)
    time.sleep(5)

    #allocate password field and enter
    pswd_field = driver.find_element_by_name("password")
    pswd_field.send_keys(pswd)
    pswd_field.send_keys(Keys.RETURN)
    time.sleep(8)

    #redirect to grades page
    grades_link = "https://registration.ashoka.edu.in/Contents/CourseManagement/StudentCourseReport_Student.aspx"
    driver.get(grades_link)

    
    for table in driver.find_elements_by_xpath('//*[contains(@id,"tblListViewCR1")]//tr'):
        data = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
        user_data.append(data)
    
    
    
    for table in driver.find_elements_by_xpath('//*[contains(@id,"tblListViewCR2")]//tr'):
        grades = [item.text for item in table.find_elements_by_xpath(".//*[self::td or self::th]")]
        sem_data.append(grades)


    #quit driver
    time.sleep(3)
    driver.quit()

    return sem_data, user_data
    # #checking if file exists or not and dumping into json
    # file = Path("output.json")
    # if file.exists():
    #     print("required file exists")
    #     print(sem_data)
    #     return sem_data 
    # else:
    #     json_obj = json.dumps(sem_data, indent = 4)
    #     print("no file exists writting to json")
    #     with open("output.json", "w") as file:
    #         file.write(json_obj)
    #     return 0



if __name__ == "__main__":
    gradesScraper()

    first_name = email.split('.')

    # appending data into grades list for published courses
    grades_list = []
    for data in reversed(sem_data):
        if len(data) == 1:
            break
        if len(data) == 6:
            if data[3]=='--' or data [4]=='--' or data[5] =='--':
                print("{}: Grade not published".format(data[2]))
            else:
                grades_list.append([data[2], data[1], data[3], data[4], data[5]])
    
    if len(grades_list) > 0:
        # converting the grades list into pandas dataframe
        df = pd.DataFrame(grades_list, columns=['Course', 'Course Code', 'Grade', 'Credit', 'GPA'])


        #emailing the df using your own email

        msg = MIMEMultipart()
        msg['Subject'] = "Grades Update"
        msg['From'] = email


        html = """\
        <html>
        <head></head>
        <body>
            <p> Hi {0},</p>
            <p> Your Grades for the following courses have been published.</p>
            {1}
            <p> Thank You!! </p>
        </body> 
        </html>
        """.format(first_name[0].capitalize(),df.to_html())

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # uncomment if interested in the actual smtp conversation
        # s.set_debuglevel(1)
        # do the smtp auth; sends ehlo if it hasn't been sent already
        s.login(email, pswd)

        s.sendmail(email,email, msg.as_string())
        s.quit()
        
