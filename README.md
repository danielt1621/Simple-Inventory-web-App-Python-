# Simple-Inventory-web-App-Python-
A simple inventory app to manipulate data from .json file and show them on an html page using python and js.

User Manual:
   In order to get information on how the application works and other relevant information reagarding the setup of the project, make sure to read the documentation at notes.txt file.

Requirements:
  - Installed version of python in your system (+ pip install all the libraries included on the .py files).
  - Installed Apache24 server, or any other of your preferences (+ visual c++ redistributable if promted to download it). 

Things to know:
  - This project was made to cover my personal needs. 
  - In the uploaded files, all paths, credentials etc. have been removed, so make sure to adjust them with yours.
  - By understanding the layout of the application, you can edit it to match your own needs. Right now it serves
    an online inventory for an IT deparment, that runs locally as a service at port 5000 on a local web server.
  - For any help or explanation of the application, you can request my guidance at danielt1621@gmail.com.

Project Tree:
  - index.html:
      This presents the main page of the application. The layout is customized to serve my needs, and can be changed to serve yours. Tailwind CSS is used            inlined along with CSS and Javascipt is used to to handle event listeners, exporting data as pfd/xlsx etc. Make sure to adjust the layout and functions        based on your needs.
  - login.html:
      This is the log in page of the application. That communicates with server.py and index.html. The string to connect to the app is static and saved within       the serv.py file. You can implement a different approach to save credentials, such as environment variables and storing them into a database. 
  - inventory_data.json:
      In this file all the items that are submitted by the form, are saved in a json format. The 'server.py' script is responsible for interacting and                manipulating the data from this file. You could implement a different logic and instead of a json file, save all the data in a database like mySQL.
  - run_flask.bat:
      This file is used only because I decided to run the 'server.py' using the Windows scheduler. In case you want to follow this approach, make sure to            create a schedule made for your needs that starts the run_flask.bat file. You can get more information about this on the notes.txt file.
  - server.py:
      The server.py is responsible for most functions of the application.
      First of all it creates a desired localport that the python script will listen to.  In this case it's port 5000. Make sure your firewall listens to the        desired port .Then the server.py also stores details for login_password, it loads the inventory, it filters the inventory's data based on applied              cateogry filters, it checks for low sotck and out of sotck items. (For my needs I've used 2 cheking functions. One that checks for Consumable items and        one that checks for the rest categories.) Make sure to read the notes.txt file to get more information about the server.py script.
  - service.py:
      This script was used as a test, but in scenario I do not use it. It allows the user to run python scrpit as a windows service. Read the notes.txt file,        to gather more information about this one.
  - test_low_stock.py
      This script can be used combined with the server.py script, in order to test the functionality of the stock alrt emails. Instead of calling manually the       trgger_email(), you can just run this script to test it.
