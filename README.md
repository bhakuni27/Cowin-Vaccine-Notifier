# Cowin Vaccine Notifier

This notify's you, with an on-screen dialog box, as soon as the vaccine dose slot is available in the centers of the pin code and date you have chosen. The dialog box shows you the center name, vaccine name, fee type and the doses available there.


## Prerequisites

Assuming you already have python3 and pip installed. Following are the dependencies:
+ tkinter
```sh
pip install tk
```
+ requests
```sh
pip install requests
```

## Usage

Use the following command to execute the code.
```sh
python3 Cowin_Vaccine_Notifier.py -p <pincode> -D <dd-mm-yyyy> -a <age> -d <dose number> 
```
OR
```sh
python3 Cowin_Vaccine_Notifier.py --pincode <pincode> --date <dd-mm-yyyy> --age <age> --dose <dose number> 
```

