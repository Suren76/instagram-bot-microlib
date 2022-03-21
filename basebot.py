from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
import random
import json
import requests
import os


class InstagramBot:
    __driver: WebDriver = webdriver.Chrome("/home/suren/Driver/chromedriver")
    __BASE_URL = "https://www.instagram.com"

    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.__run()

    def __run(self):
        self.__driver.get(self.__BASE_URL)

    def close(self):
        self.__driver.close()
        self.__driver.quit()

    def __save_cookie(self, path="cookiesfile.json"):
        filehandler = open(path, 'w+')
        json.dump(self.__driver.get_cookies(), filehandler)

    def __load_cookie(self, path="cookiesfile.json"):
        with open(path, 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            self.__driver.add_cookie(cookie)

    def login(self):
        username = self.__driver.find_element(By.NAME, "username")
        username.clear()
        username.send_keys(self.__username)
        # username.send_keys(Keys.RETURN)
        password = self.__driver.find_element(By.NAME, "password")
        password.clear()
        password.send_keys(self.__password)
        button = self.__driver.find_element(By.XPATH, "//div[3]/button")
        button.click()
        sleep(3)
        self.__save_cookie()

    def login_with_cookies(self):
        print("login")
        self.__load_cookie()

    def __scroll(self, times):
        for i in range(times):
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(random.randrange(1, 3))

    def like_post(self, post_id):
        print(post_id)
        self.__driver.get(self.__BASE_URL + "/p/" + str(post_id))
        self.__driver.find_element(By.XPATH, "//span[1]/button").click()
        sleep(random.randrange(1, 5))

    def find_by_hashtag(self, hashtag: str, data_type=id):
        # data_type-ին կեշես մի դևի էն չի
        self.__scroll(10)

        self.__driver.get(self.__BASE_URL + "/explore/tags/" + str(hashtag))

        top_posts = self.__driver.find_element(By.CLASS_NAME, "EZdmt").find_elements(By.TAG_NAME, "a")
        top_posts_links = [item.get_attribute("href") for item in top_posts]

        new_posts = self.__driver.find_element(By.XPATH, "//main/article/div[2]/div").find_elements(By.TAG_NAME, "a")
        new_posts_links = [item.get_attribute("href") for item in new_posts]

        if data_type == "link":
            return top_posts_links, new_posts_links

        top_posts_ids = [link.split("/p/")[1][:-1] for link in top_posts_links]
        new_posts_ids = [link.split("/p/")[1][:-1] for link in new_posts_links]

        return top_posts_ids, new_posts_ids

    def download_content(self, link):
        self.__driver.get(link+"?__a=1")

        json_data = json.loads(self.__driver.find_element(By.XPATH, "/html/body/pre").text)["items"][0]

        if not os.path.isdir(f"{json_data['user']['username']}"):
            os.mkdir(f"{json_data['user']['username']}")

        if json_data["media_type"] == 1:
            image_url = json_data["image_versions2"]["candidates"][0]["url"]
            image = requests.get(image_url).content

            with open(f"{json_data['user']['username']}/{json_data['user']['username']}_{json_data['code']}.png", "wb") as file:
                file.write(image)

        if json_data["media_type"] == 2:
            video_url = json_data["video_versions"][0]["url"]
            video = requests.get(video_url, stream=True).content

            with open(f"{json_data['user']['username']}/{json_data['user']['username']}_{json_data['code']}.mp4", "wb") as file:
                file.write(video)

        if json_data["media_type"] == 8:
            media_list = json_data["carousel_media"]

            os.mkdir(f"{json_data['user']['username']}/{json_data['code']}")

            for item in media_list:
                if item["media_type"] == 1:
                    image_url = item["image_versions2"]["candidates"][0]["url"]
                    image = requests.get(image_url).content

                    with open(f"{json_data['user']['username']}/{json_data['code']}/{json_data['user']['username']}_{json_data['code']}.png", "wb") as file:
                        file.write(image)

                if item["media_type"] == 2:
                    video_url = item["video_versions"][0]["url"]
                    video = requests.get(video_url, stream=True).content

                    with open(f"{json_data['user']['username']}/{json_data['code']}/{json_data['user']['username']}_{json_data['code']}.mp4", "wb") as file:
                        file.write(video)

    def follow_user(self, user):
        self.__driver.get(user)

        if not self.__driver.find_element(By.CLASS_NAME, "jIbKX"):
            return print("already followed")

        self.__driver.find_element(By.XPATH, "//div/span/span[1]/button").click()

    def unfollow_user(self, user):
        self.__driver.get(user)

        if not self.__driver.find_element(By.CLASS_NAME, "-fzfL"):
            return print("not followed")

        self.__driver.find_element(By.XPATH, "//div/span/span[1]/button").click()
        sleep(1)
        self.__driver.find_element(By.XPATH, "//div[3]/button[1]").click()

    def send_message_to_user(self, user, text):
        self.__driver.get(user)

        self.__driver.find_element(By.XPATH, "//div[1]/div[1]/div/div[1]/button").click()
        sleep(5)
        self.__driver.find_element(By.XPATH, "//div/div/div[2]/textarea").send_text(str(text))
        self.__driver.find_element(By.XPATH, "//div/div[2]/div/div/div[3]/button").click()

    def driver(self):
        return self.__driver

