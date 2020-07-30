import matplotlib.pyplot as plt
import csv

from selenium import webdriver
from datetime import datetime

LOG_BASE_ADD = "config/log_"


class IGBot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="config/geckodriver.exe")

    # returns the number of followers
    def get_followers_number(self, user_name):
        self.driver.get("https://www.instagram.com/" + user_name)
        num = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span") \
            .get_attribute("title")
        self.close()
        return num

    # it closes the WebDriver connection
    def close(self):
        self.driver.quit()


# it returns a string that contains the current date and time
def time_stamp():
    dt = datetime.now()
    return dt.strftime("%d/%m/%Y %H:%M:%S")


# it saves in a log file the number of followers with a time stamp
def log_routine(num_of_followers, user_name):
    try:
        log_file = open(LOG_BASE_ADD + username + ".txt", "a")
    except FileNotFoundError:
        log_file = open(LOG_BASE_ADD + username + ".txt", "w")

    log_file.write(time_stamp() + "," + num_of_followers + "\n")
    log_file.close()


# it reads a CSV file and draws a plot using the values saved on that file
def draw_plot_from_txt_file():
    with open(LOG_BASE_ADD + username + ".txt") as file:
        csv_reader = csv.reader(file)
        dates = []
        num_followers = []
        for row in csv_reader:
            dates.append(row[0][0:5])
            num_followers.append(int(row[1].replace('.', '')))
    draw_plot(dates, num_followers)


# it draws a plot that shows on x axis the x_values and on the y axis the y_values
def draw_plot(x_values, y_values):

    plt.yticks(y_values)
    plt.grid()
    plt.plot(x_values, y_values, 'b-o')
    plt.ylabel("Followers")
    plt.xlabel("Date")

    plt.show()

# the beginning of the program

# username of the account you want to analyse
username = input("Insert the username you want to track: ")

bot = IGBot()
n_followers = bot.get_followers_number(username)
log_routine(n_followers, username)
draw_plot_from_txt_file()

input("Press any key to exit!")
