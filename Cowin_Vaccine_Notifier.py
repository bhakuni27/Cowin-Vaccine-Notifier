# Import libraries
import argparse
import sys
import time
import requests
import json
import tkinter as tk
from tkinter import messagebox

# Checks the command line arguments and displays the correct usage
parser = argparse.ArgumentParser()
parser.add_argument("-p","--pincode", dest="pinCode", help="Pincode of your area")
parser.add_argument("-D","--date", dest="date", help="Date of the day you want to check for vaccine slot availability.")
parser.add_argument("-a","--age", dest="age", help="Your age", type=int)
parser.add_argument("-d","--dose", dest="dose", help="Dose number 1 or 2", type=int)
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

# Checks exit conditions
if args.dose not in [1,2]:
    print("Dose number INCORRECT")
    sys.exit(1)  
if args.age < 18:
    print("Minimum Age is 18.")
    sys.exit(1)
presentDate = time.strptime(time.strftime("%d-%m-%Y", time.localtime()), "%d-%m-%Y")
enteredDate = time.strptime(args.date, "%d-%m-%Y")
if enteredDate < presentDate:
    print("Please check the entered date(Date's from past are unacceptable)")
    sys.exit(1)    


#Parameters for the API call
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}
query = {
   'pincode': args.pinCode,
    'date' : args.date
}

#Helper function
def display_box(msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo('Vaccine Slot Available', msg)

#curx of the code
while(True):
    print("Last check at " + time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime()))
    response = requests.request(
       "GET",
       url,
       headers=headers,
       params=query
    )
    
    data = json.loads(response.text)
    
    if "error" in data:
        print('\033[1m '+data["error"]+' \033[0m')
        sys.exit(1)
    counter1 = 0
    counter2 = 0
    if len(data["sessions"]):
        msg = ""
        for i in range(len(data["sessions"])):
            if args.age >= data["sessions"][i]["min_age_limit"] and args.age < 45:
                counter1 += 1
                if args.dose == 1:
                    if data["sessions"][i]["available_capacity_dose1"] > 0:
                        msg = msg + "\n\nCenter Name : " + data["sessions"][i]["name"] + "\nVaccine : " + data["sessions"][i]["vaccine"] + "\nFee Type : " + data["sessions"][i]["fee_type"] + "\nVaccine Available : " + str(data["sessions"][i]["available_capacity_dose1"])
                    elif data["sessions"][i]["available_capacity_dose1"] == 0:
                        print("Vaccine slot unavailable at center \033[1m "+data["sessions"][i]["name"]+" \033[0m ")
                        counter2 += 1
                elif args.dose == 2:
                    if data["sessions"][i]["available_capacity_dose2"] > 0:
                        msg = msg + "\n\nCenter Name : " + data["sessions"][i]["name"] + "\nVaccine : " + data["sessions"][i]["vaccine"] + "\nFee Type : " + data["sessions"][i]["fee_type"] + "\nVaccine Available : " + str(data["sessions"][i]["available_capacity_dose2"])
                    elif data["sessions"][i]["available_capacity_dose2"] == 0:
                        print("Vaccine slot unavailable at center \033[1m "+data["sessions"][i]["name"]+" \033[0m ")  
                        counter2 += 1       
            elif args.age >= 45 and data["sessions"][i]["min_age_limit"] != 18:
                counter1 += 1
                if args.dose == 1:
                    if data["sessions"][i]["available_capacity_dose1"] > 0:
                        msg = msg + "\n\nCenter Name : " + data["sessions"][i]["name"] + "\nVaccine : " + data["sessions"][i]["vaccine"] + "\nFee Type : " + data["sessions"][i]["fee_type"] + "\nVaccine Available : " + str(data["sessions"][i]["available_capacity_dose1"])
                    elif data["sessions"][i]["available_capacity_dose1"] == 0:
                        print("Vaccine slot unavailable at center \033[1m "+data["sessions"][i]["name"]+" \033[0m ")   
                        counter2 += 1             
                elif args.dose == 2:
                    if data["sessions"][i]["available_capacity_dose2"] > 0:
                        msg = msg + "\n\nCenter Name : " + data["sessions"][i]["name"] + "\nVaccine : " + data["sessions"][i]["vaccine"] + "\nFee Type : " + data["sessions"][i]["fee_type"] + "\nVaccine Available : " + str(data["sessions"][i]["available_capacity_dose2"])
                    elif data["sessions"][i]["available_capacity_dose2"] == 0:
                        print("Vaccine slot unavailable at center \033[1m "+data["sessions"][i]["name"]+" \033[0m ")  
                        counter2 += 1      
        if len(msg) > 0:
            display_box(msg)
            sys.exit(0)  
            
    if counter1 != 0 and counter1 == counter2:
        print("\033[1m Vaccine slots all BOOKED for "+args.date+". Please try for another date.\033[0m")
        sys.exit(0) 
                    
    time.sleep(7)
