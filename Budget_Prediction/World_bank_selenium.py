# Importing Libraries
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv

#Loading Home Page
driver = webdriver.Chrome()
driver.get("https://data.worldbank.org/")
for i in range(3):  # You may need to adjust the number of iterations based on your requirements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
#for clicking projects and operations option
driver.find_element(By.XPATH, "//li/a[@href='https://projects.worldbank.org/']").click()
# Switch to the new window
windows = driver.window_handles
driver.switch_to.window(windows[1])
time.sleep(5)
#for clicking project lists option
WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//div/a[@href='https://projects.worldbank.org/en/projects-operations/projects-list']"))).click()
time.sleep(3)
# sectorsList = ['Agricultural credit']
sectorsList = ['Agricultural credit','Health','Electric power and other energy adjustment', 'Primary Education','Tertiary Education','Urban water supply','Waste Management','Financial sector development','Roads and highways']
# Create a CSV file to store the data
csv_file = open('world_bank_projects.csv','w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Sector','Project Title', 'Project ID','Project Status','Year','Closing Year','Duration(in months)','Commitment Amount(in million)'])
for sector in sectorsList:
    # for selecting country-India
    driver.find_element(By.XPATH, value="(//a[text()='Country'])[1]").click()
    time.sleep(3)

    search_box = driver.find_element(By.XPATH, "//input[@id='primary_inputs-1']")
    search_box.click()
    search_box.send_keys("Ind")

    check_box_of_india = driver.find_element(By.XPATH, "(//div[@class='_loop_checkbox']/input[@class='_loop_primary_checkbox'])[9]")
    check_box_of_india.click()
    time.sleep(3)


    # for selecting status-closed
    status_opt = driver.find_element(By.XPATH, "//a[text()='Status']")
    status_opt.click()
    closed=driver.find_element(By.XPATH, "(//div[@class='_loop_checkbox']/input[@class='_loop_primary_checkbox'])[6]").click()
    time.sleep(3)

    # for selecting the required sectors
    driver.find_element(By.XPATH, "//a[text()='Sector']").click()
    search_sector = driver.find_element(By.XPATH, "(//ul[@class='sidebar-list ng-tns-c4-3 ng-star-inserted'])[5]/ul/div/input")
    search_sector.click()
    time.sleep(1)

    search_sector.send_keys(sector)
    sector_opt=driver.find_element(By.XPATH,"(//ul[@class='sidebar-list ng-tns-c4-3 ng-star-inserted'])[5]/ul/li/div/input")
    sector_opt.click()
    time.sleep(2)
    go_button=driver.find_element(By.XPATH,"//button[@class='go-btn']").click()
    time.sleep(3)


    #scrolling the page
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    project_names = driver.find_elements(By.XPATH, "//td/a[@class='project-list-link']")

    project_ids = driver.find_elements(By.XPATH, "//td[@data-th='Project ID:']")
    project_CommitmentAmount = driver.find_elements(By.XPATH, "//td[@data-th='Commitment Amount:']")
    project_status = driver.find_elements(By.XPATH,"//td[@data-th='Status:']")
    approval_year = driver.find_elements(By.XPATH, "//td[@data-th='Approval Date:']")

    titles = []
    for title in project_names:
        t = title.text
        titles.append(t)
    print("Titles: ",titles)

    # Getting Project status list
    prj_status = []
    for status in project_status:
        prj_status.append(status.text)
    print("Status : ",prj_status)

    # Approval Date list
    Approval = []
    for date in approval_year:
        Approval.append(date.text)
    print("Approval : ",Approval)
    # Commitment Amount
    commitment_amount = []
    for money in project_CommitmentAmount:
        commitment_amount.append(money.text)
    print("Commitment Amount :",commitment_amount)

    # Getting Closed Dates By iterating the Id's
    ids_list = []
    for id in project_ids:
        x = id.text
        ids_list.append(x)
    closing_dates_raw = []
    for id in ids_list:
        url = f"https://projects.worldbank.org/en/projects-operations/project-detail/{id}"
        driver.get(url)
        time.sleep(5)
        for i in range(1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        date = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div/ul[4]/li[2]/p")))
        closing_dates_raw.append(date.text)

    # Convert 'N/A' to a default date in the closing dates
    closing_dates = []
    for date_str in closing_dates_raw:
        if date_str.lower() == 'n/a':
            closing_dates.append(
                datetime.datetime.now())  # Replace 'N/A' with the current date or another default value
        else:
            closing_dates.append(datetime.datetime.strptime(date_str, '%B %d, %Y'))
    print("ids : ", ids_list)
    print("Closing Dates :", closing_dates)

    # Convert Approval date strings to datetime objects
    approval_dates = [datetime.datetime.strptime(date_str, '%B %d, %Y') for date_str in Approval]

    # Convert Closing date strings to datetime objects
    # closing_dates = [datetime.datetime.strptime(date_str, '%B %d, %Y') for date_str in closing_dates]

    duration_list = []

    # Calculate and print the duration between approval and closing dates in months
    for approval_date, closing_date in zip(approval_dates, closing_dates):
        duration = closing_date - approval_date
        duration_in_months = (duration.days // 30)  # Assuming an average of 30 days in a month
        # print("Approval Date:", approval_date.strftime('%Y-%m-%d'))
        # print("Closing Date: ", closing_date.strftime('%Y-%m-%d'))
        # print("Duration: ", duration_in_months, "months")
        duration_list.append(duration_in_months)

    # Write the data to the CSV file
    for name, project_id, status, approve,close,duration,Amount_allocated in zip(titles,ids_list, prj_status, Approval, closing_dates,duration_list,commitment_amount):
        csv_writer.writerow([sector, name, project_id, status, approve,close.strftime('%Y-%m-%d'),duration,Amount_allocated])

    driver.get("https://projects.worldbank.org/en/projects-operations/projects-list")
    time.sleep(5)

for act in sectorsList:
    driver.find_element(By.XPATH, value="(//a[text()='Country'])[1]").click()
    time.sleep(3)

    search_box = driver.find_element(By.XPATH, "//input[@id='primary_inputs-1']")
    search_box.click()
    search_box.send_keys("Ind")

    check_box_of_india = driver.find_element(By.XPATH, "(//div[@class='_loop_checkbox']/input[@class='_loop_primary_checkbox'])[9]")
    check_box_of_india.click()
    time.sleep(3)


    # for selecting status-closed
    status_opt = driver.find_element(By.XPATH, "//a[text()='Status']")
    status_opt.click()
    closed=driver.find_element(By.XPATH, "(//div[@class='_loop_checkbox']/input[@class='_loop_primary_checkbox'])[5]").click()
    time.sleep(3)

    # for selecting the required sectors
    driver.find_element(By.XPATH, "//a[text()='Sector']").click()
    search_sector = driver.find_element(By.XPATH, "(//ul[@class='sidebar-list ng-tns-c4-3 ng-star-inserted'])[5]/ul/div/input")
    search_sector.click()
    time.sleep(1)

    search_sector.send_keys(act)
    sector_opt=driver.find_element(By.XPATH,"(//ul[@class='sidebar-list ng-tns-c4-3 ng-star-inserted'])[5]/ul/li/div/input")
    sector_opt.click()
    time.sleep(2)
    go_button=driver.find_element(By.XPATH,"//button[@class='go-btn']").click()
    time.sleep(3)


    #scrolling the page
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    project_names = driver.find_elements(By.XPATH, "//td/a[@class='project-list-link']")

    project_ids = driver.find_elements(By.XPATH, "//td[@data-th='Project ID:']")
    project_CommitmentAmount = driver.find_elements(By.XPATH, "//td[@data-th='Commitment Amount:']")
    project_status = driver.find_elements(By.XPATH,"//td[@data-th='Status:']")
    approval_year = driver.find_elements(By.XPATH, "//td[@data-th='Approval Date:']")

    titles = []
    for title in project_names:
        t = title.text
        titles.append(t)
    print("Titles: ",titles)

    # Getting Project status list
    prj_status = []
    for status in project_status:
        prj_status.append(status.text)
    print("Status : ", prj_status)

    # Approval Date list
    Approval = []
    for date in approval_year:
        Approval.append(date.text)
    print("Approval : ", Approval)
    # Commitment Amount
    commitment_amount = []
    for money in project_CommitmentAmount:
        commitment_amount.append(money.text)
    print("Commitment Amount :", commitment_amount)

    # Getting Closed Dates By iterating the Id's
    ids_list = []
    for id in project_ids:
        x = id.text
        ids_list.append(x)
    closing_dates_raw = []
    for id in ids_list:
        url = f"https://projects.worldbank.org/en/projects-operations/project-detail/{id}"
        driver.get(url)
        time.sleep(5)
        for i in range(1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        date = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div/ul[4]/li[2]/p")))
        closing_dates_raw.append(date.text)

    # Convert 'N/A' to a default date in the closing dates
    closing_dates = []
    for date_str in closing_dates_raw:
        if date_str.lower() == 'n/a':
            closing_dates.append(
                datetime.datetime.now())  # Replace 'N/A' with the current date or another default value
        else:
            closing_dates.append(datetime.datetime.strptime(date_str, '%B %d, %Y'))
    print("ids : ", ids_list)
    print("Closing Dates :", closing_dates)

    # Convert Approval date strings to datetime objects
    approval_dates = [datetime.datetime.strptime(date_str, '%B %d, %Y') for date_str in Approval]

    # Convert Closing date strings to datetime objects
    # closing_dates = [datetime.datetime.strptime(date_str, '%B %d, %Y') for date_str in closing_dates]

    duration_list = []

    # Calculate and print the duration between approval and closing dates in months
    for approval_date, closing_date in zip(approval_dates, closing_dates):
        duration = closing_date - approval_date
        duration_in_months = (duration.days // 30)  # Assuming an average of 30 days in a month
        # print("Approval Date:", approval_date.strftime('%Y-%m-%d'))
        # print("Closing Date: ", closing_date.strftime('%Y-%m-%d'))
        # print("Duration: ", duration_in_months, "months")
        duration_list.append(duration_in_months)

    # Write the data to the CSV file
    for name, project_id, status, approve, close, duration, Amount_allocated in zip(titles, ids_list, prj_status,Approval, closing_dates,duration_list, commitment_amount):
        csv_writer.writerow([act, name, project_id, status, approve, close.strftime('%Y-%m-%d'), duration, Amount_allocated])

    driver.get("https://projects.worldbank.org/en/projects-operations/projects-list")
    time.sleep(5)



csv_file.close()

# Load the GDP data
gdp_data = pd.read_csv('India_GDP_1960-2022.csv')

# Load the World Bank data
data = pd.read_csv('world_bank_projects.csv')

# Convert 'Year' column to a common format in both dataframes
gdp_data['Year'] = gdp_data['Year'].astype(int)
data['Year'] = pd.to_datetime(data['Year'], errors='coerce').dt.year

# Merge the two dataframes on the 'Year' column
merged_data = pd.merge(data, gdp_data, on='Year', how='left')

# Save the merged data to a new CSV file
merged_data.to_csv('Final_data.csv',index=False)

# Read the CSV file into a DataFrame
df = pd.read_csv('Final_data.csv')

# 'Commitment Amount' column
commitment_amount = df['Commitment Amount(in million)']

# Drop the 'Commitment Amount' column from the original position
df = df.drop('Commitment Amount(in million)', axis=1)

# Add the 'Commitment Amount' column to the end of the DataFrame
df['Commitment Amount(in million)'] = commitment_amount

# Save the modified DataFrame to a new CSV file
df.to_csv('World_Bank.csv', index=False)

# Close the browser
driver.quit()
