from basebot import *

username = "street_work.out"
password = "-_qwerty7890"

user = InstagramBot(username, password)
sleep(5)
# user.login()
user.login_with_cookies()
sleep(3)
top, new = user.find_by_hashtag("goris")
sleep(3)
print(len(top))
sleep(3)
# for i in range(len(top)):
#     user.like_post(top[i])
# sleep(5)

print(1)
user.close()
print(2)
quit()
