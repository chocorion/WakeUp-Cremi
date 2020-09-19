#!/usr/bin/env python3

import requests, getpass, sys
from machines import machines

CREMI_MACHINE_URL = "https://{}:{}@services.emi.u-bordeaux.fr/exam/js/getWake.php?h={}&wmode=std&"

def selectRoom():
    print("Available rooms : ")

    rooms = list(machines.keys())
    for index, room in enumerate(rooms):
        print("({:2}) -> {:14} [{:2} machines]".format(index, rooms[index], len(machines[room])))

    return rooms[int(input("\nWhat is your choice ? "))]
    

if __name__ == "__main__":
    if len(sys.argv) == 2:
        for room in machines.keys():
            if sys.argv[1] in room:
                choice = room
                break
    else:
        choice = selectRoom()

    print("You have chosen : " + choice)

    print("\n")
    username = input("Username : ")
    password = getpass.getpass(prompt="Password: ", stream=None) 
    print("\n")

    for (machine, machine_id) in machines[choice]:
        r = requests.get(CREMI_MACHINE_URL.format(username, password, machine_id))
        if r.status_code == 200:
            print("Wake up {}...".format(machine))
        else:
            print("Problem with {}, status code -> {} !".format(machine, r.status_code))