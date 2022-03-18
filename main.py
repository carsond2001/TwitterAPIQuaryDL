import os
import subprocess
import time
import re
import requests
from itertools import chain
import json


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

# Function that searches twitter and returns a list of json data
def search_twitter(query, tweet_fields, bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# Cleans the list so that it only includes twitter links
def linkClean(list):
    list1 = []
    for string in list:
        for char in string:
            if char != "\\":
                list1.append(string)
            else:
                split_string = string.split("\\", 1)
                substring = split_string[0]
                list1.append(substring)
    list2 = []
    for i in list1:
        if i not in list2:
            list2.append(i)
    print(list2)

def thumbnailGrabber(video_input_path, img_output_path):
    dir_list = os.listdir(video_input_path)
    for file in dir_list:
        try:
            subprocess.call(['ffmpeg', '-i', file, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
        except:
            continue

if __name__ == '__main__':
    token = "TOKEN GOES HERE"
    qry = input("What do u wanna mass download?: ")
    mainList = []
    for i in range(100):
        end = search_twitter(qry, "", token)
        end = str(end)
        print(Find(end))
        mainList.append(Find(end))
        print("-----------------------------------")
        time.sleep(1)
    main_flatten_list = list(chain.from_iterable(mainList))
    print(main_flatten_list)
    print("Length before dupe clean: " + str(len(main_flatten_list)))
    mainListCleaned = []
    for i in main_flatten_list:
        if i not in mainListCleaned:
            mainListCleaned.append(i)
    print("Length before dupe clean: " + str(len(mainListCleaned)))
    listlinkfix = []
    for string in mainListCleaned:
        if "https" in string:
            os.system("youtube-dl " + string)
        else:
            continue
    thumbnailGrabber("C:/Users/Carson/PycharmProjects/TwitterVideoMassDownload","C:/Users/Carson/PycharmProjects/TwitterVideoMassDownload/Thumbnails")
    print(listlinkfix)
