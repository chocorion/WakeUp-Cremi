#!/usr/bin/env python3

from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

username = input("Username : ")
password = input("Password : ")

CREMI_ROOMS_URL = "https://{}:{}@services.emi.u-bordeaux.fr/exam/js/getResult.php?Form[CPU]=%27%%27&Form[core]=%27%%27&Form[screen]=%27%%27&Form[GPU]=%27%%27&Form[os]=%27%%27&Form[comment]=%27commentaire%27&Form[reservable]=%27%%27&host_name=&host_nb=&page=wol".format(username, password)

machines = dict()

if __name__ == "__main__":
    display = Display(visible=0, size=(100, 100))
    display.start()
    driver = webdriver.Firefox()
    driver.get(CREMI_ROOMS_URL)
    
    sourceCode = driver.page_source

    driver.quit()
    display.stop()

    soup = BeautifulSoup(sourceCode, features="lxml")

    for room in soup.findAll("tr", attrs={"class": "display"}):
        room_name = room.find("div", attrs={"class": "hidden"})["id"].split('_')[1]
        machines[room_name] = list()

        for machine in room.findAll("input", attrs={"class": "host"}):
            machines[room_name].append((str(machine.next_sibling).replace('\xa0', ''), int(machine["id"])))

    with open("machines.py", "w") as file:
        file.write("machines = ")
        file.write(str(machines))
        