from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import getpass
from selenium.webdriver.common.by import By
import json
from pathlib import Path
sem_data = []
user_data = []

def gradesScraper():
    email = str(input("Email: "))
    pswd = getpass.getpass('Password:')
    

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



gradesScraper()