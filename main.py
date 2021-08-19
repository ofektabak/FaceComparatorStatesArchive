# This is a sample Python script.
import webbrowser

import selenium
import tkinter as tk
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from shutil import which
import time
from functools import partial



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Get Search line and return an array of images using a crawler
def AssembleURL(searchline):
    return "https://www.archives.gov.il/catalogue/group/1?kw=%D7%99%D7%A6%D7%97%D7%A7%20%D7%A8%D7%91%D7%99%D7%9F&mode=images&start_period=1994-01-01T00:00:00Z&end_period=2020-12-28T00:00:00Z&itemsPerPage=32"
    return f"https://www.archives.gov.il/catalogue/group/1?kw={searchline}&mode=images"


def GetImages(searchline):
    Images = []

    # Put the target Url here in list:
    URLS = [AssembleURL(searchline)]
    # Initialize Driver
    chrome_path = which('chromedriver')
    opt = Options()
    # opt.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=opt)
    driver.maximize_window()
    for url in URLS:

        driver.get(url)

        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="popup-trigger position-relative"]')))

        for a in driver.find_elements_by_xpath('//div[@class="popup-trigger position-relative"]/img'):
            Images.append(a.get_attribute('src'))
        try:
            while True:
                a = WebDriverWait(driver, 25).until(
                    EC.presence_of_element_located((By.XPATH, '(//a[@aria-label="Next"])[1]')))
                a.click()
                time.sleep(2)
                for a in driver.find_elements_by_xpath('//div[@class="popup-trigger position-relative"]/img'):
                    Images.append(a.get_attribute('src'))

        except:
            pass
    for i in range(len(Images)):
        Images[i] = str(Images[i]).replace("_s_", "_l_")

    return Images


# get 2 urls and return a true or false depending on the api result
def IsSamePerson(ourpersonurl, totesturl):
    url = 'https://api-us.faceplusplus.com/facepp/v3/compare'
    data = {'api_key': 'pUp0RKdkX1tvRCUi1gYf5UhC6kchX1DI',
            'api_secret': 'LJJ5johbabJkJuI1Q-YeCHhUF5DrF8jb',
            'image_url1': ourpersonurl,
            'image_url2': totesturl,
            }
    response = requests.post(url, data=data)
    response_json = response.json()
    if not 'confidence' in response_json:
        return False
    if response_json['confidence'] > response_json['thresholds']['1e-5']:
        return True
    else:
        return False


# Define a callback function

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=("Helvetica", 10))
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def searchbutton():
    ourface_url = mf_person_url.get()
    tosearch = mf_searchline.get()
    if ourface_url == "" and tosearch == "":
        popupmsg("Please fill the following lines:\n"
                 "Person url\n What to search?")
        return 0
    elif ourface_url == "":
        popupmsg("Please fill the following lines:\n"
                 "Person url")
        return 0
    elif tosearch == "":
        popupmsg("Please fill the following lines:\n"
                 "What to search?")
        return 0
    else:
        results = []
        url_array = GetImages(tosearch)
        for testurl in url_array:
            if testurl == 'https://www.archives.gov.il/Archives/0b071706802fd9dd/Files/0b071706850eb453/00071706.81.D2.01.4F_thumb_l_wide.jpg':
                print("111")
            if IsSamePerson(ourface_url, testurl):
                results.append(testurl)
        df = pd.DataFrame(results, columns=['results'])
        df.to_csv(r'./results.csv', index=False, header=True, mode='a')
        print(df)
        print(results)

        if len(results) == 0:
            popupmsg("no matching results found")
        else:
            tempwin = tk.Tk()
            scrollbar = tk.Scrollbar(tempwin)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            mylist = tk.Listbox(tempwin, yscrollcommand=scrollbar.set)
            mylist.bind('<<ListboxSelect>>', partial(openurl, mylist))

            for i in range(len(results)):
                mylist.insert(tk.END, f"{i + 1}. {results[i]} ")

            mylist.pack(side=tk.LEFT, fill=tk.BOTH)
            scrollbar.config(command=mylist.yview)
            tempwin.mainloop()


def button_test():
    results = []
    for i in range(100):
        results.append(
            'https://www.archives.gov.il/Archives/0b071706802fd9dd/Files/0b071706850eb453/00071706.81.D2.01.4F_thumb_l_wide.jpg')

    if len(results) == 0:
        popupmsg("no matching results found")
    else:

        tempwin = tk.Tk()
        scrollbar = tk.Scrollbar(tempwin)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        mylist = tk.Listbox(tempwin, yscrollcommand=scrollbar.set)
        mylist.bind('<<ListboxSelect>>', partial(openurl,mylist))

        for i in range(len(results)):
            mylist.insert(tk.END, f"{i+1}. {results[i]} ")

        mylist.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=mylist.yview)
        tempwin.mainloop()

# execute the searching
# show the results in a new frame

def openurl(input,input2):
    print(input)
    print(input2)
    index = input.curselection()[0]
    item = input.get(index)
    print(item)
    newindex = item.find('https://', 0, len(item))

    if 'https://' in item:
        webbrowser.open_new(item[newindex:])
def main():
    personurl = input("Please insert a person face url to search by")
    print(personurl)

    print("to exit enter -1 in the search line\n")
    # while exit != -1:
    #     # results = []
    #     # searchline = input("What do you wish to search?:\n")
    #     # url_array = GetImages(searchline)
    #     # for testurl in url_array:
    #     #     if testurl == 'https://www.archives.gov.il/Archives/0b071706802fd9dd/Files/0b071706850eb453/00071706.81.D2.01.4F_thumb_l_wide.jpg':
    #     #         print("111")
    #     #     if IsSamePerson(personurl, testurl):
    #     #         results.append(testurl)
    #     # df = pd.DataFrame(results, columns=['results'])
    #     # df.to_csv(r'./results.csv', index=False, header=True, mode='a')
    #     # print(df)
    #     # print(results)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.title('נושאים במדעי הרוח הדיגיטיליים - חיפוש מבוסס פנים')
    mf_headline = tk.Label(root, text="Search By Face", font=("Helvetica", "22", "bold", "underline"))
    mf_labelsearch = tk.Label(root, text="What do you wish to search?: ", font=("Helvetica", "16", "bold", "underline"))
    mf_labelperson = tk.Label(root, text="Person URL: ", font=("Helvetica", "16", "bold", "underline"))

    mf_person_url = tk.Entry(root, width=50, font=("Helvetica", "16"))
    mf_searchline = tk.Entry(root, width=50, font=("Helvetica", "16"))
    mf_searchbutton = tk.Button(root, text="Search", command=searchbutton, font=("Helvetica", "28", "bold",))

    # mf_headline.pack
    # mf_person_url.pack(fill=tk.X,side =tk.LEFT,expand = True)
    # mf_searchline.pack(fill=tk.X,side =tk.LEFT,expand = True)
    # mf_searchbutton.pack(fill=tk.X,side =tk.LEFT,expand = True)
    mf_labelperson.place(x=20, y=150)
    mf_labelsearch.place(x=20, y=320)
    mf_searchbutton.place(x=350, y=500)
    mf_person_url.place(x=325, y=153)
    mf_searchline.place(x=325, y=323)
    mf_headline.place(x=300, y=50)

    root.mainloop()
    # main()
