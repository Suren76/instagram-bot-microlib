from basebot import *

username = "street_work.out"
password = "-_qwerty7890"

user = InstagramBot(username, password)
sleep(5)
# user.login()
user.login_with_cookies()
user.download_content("https://www.instagram.com/p/CbIoREmLiLn/")

