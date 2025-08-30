# Rainfall density software
![rainfall_density_software]()

## Introduction
**The Rain Density Calculator** is a Python-based application built for engineers, hydrologists, and water resource professionals to record, calculate, and analyze rainfall density across defined surface areas. By integrating directly with Google Sheets as its database, the tool enables users to easily log, review, and process rainfall data. It offers a simple yet effective solution for managing rainfall density records and tracking changes over time.

## Features

- **Data Entry:** 
  * Enter new monthly rainfall records, including the year, month,  total rain volume, and the collection area.
- **On-the-fly Calculation:** 
  * Use a built-in calculator to compute rainfall density for any given volume and area without saving the data.
- **Data Persistence:** 
  * All entered data is securely saved and managed in a dedicated Google Sheet, providing a single source of truth.
- **Historical Overview:** 
  * View a list of past rainfall entries stored in your Google Sheet.
- **12-Month Average:** 
  * Automatically calculate and display the average rainfall density for the last 12 unique months with data.
- **Google Sheets Integration:** 
  * The program seamlessly handles the connection, creation, and population of your Google Sheet. It even provides a helpful hint on how to export your data as a CSV file for further analysis.
  

##  How to use the app.
![Main Menu Options](/images/rainfullDensityMenu.png)

Very smpile frindly use a Main Menu Options.

=== Rain Density Menu ===
1) Add monthly entry (compute & save)
2) Density calculator (no save)
3) Show past entries
4) Show 12-month average density
5) Export help (CSV)
0) Exit

#### Option 1: Add monthly entry

    Enter year, month, rainfall volume (mm/h), and area (m²).

    The program calculates density (mm/h per m²).

    Confirm to save → entry is stored in Google Sheets.

#### Option 2: Density calculator

    Quick calculation only (does NOT save to Google Sheets).

#### Option 3: Show past entries

    Displays saved entries (default: last 25).

#### Otion 4: 12-month average density

    Computes the average density from the most recent 12 unique months.

#### Option 5: Export help (CSV)

    Explains how to download your Google Sheet as a CSV file (for use in Excel, MATLAB, or hydrology software).

#### Option 0: Exit

    Quit the program.


## Future Features.
This project is designed to be extendable. Possible future improvements include:
- **SQL Database Integration**
    * Replace Google Sheets with an SQL database for more robust data storage, faster queries, and better scalability.
- **Daily Data Entry**
    * Expand the system to support daily rainfall records (instead of only monthly), enabling more detailed analysis.
- **Advanced Averages**
    * Add functionality to calculate both:
        * The average density for each individual month (across multiple years), and--
        * The rolling average over every 12 months.
- **Enhanced Frontend Experience**
    * Improve the user interface with a more intuitive and visually appealing dashboar.  
  
## Program sturcture digram  
   ![Program sturcture digram ](/images/rainDensityDiagram.png)


## Testing  
* ### Browser Testing  
     * | Browser       | Operation system | Responsiveness     |
       | :-----------: |:----------------:| :-----------------:|
       |     chrome    |   Windows 11     |    Very good       |
       |      Edge     |   Windows 11     |    Very good       |
       |     FireFox   |   Windows 11     |    Very good       |


* 
* ### Bug Fixes
  *  First bug, I forgot to put the *creds.json* inside the *.gitignore* will led to GitHub blocked the push, I tried to remove the credentials file from Git’s history using the the command:
      * git rm --cached creds.json
      * echo "creds.json" >> .gitignore
      * git add .gitignore
      * git commit -m "Remove creds.json from repo and add to .gitignore" , did't work, later I had to delete the repositoy and start agian.
  * *TypeError:* during the test of appen_entry function, wrong spelled keyword arrument saved_at insted of save_at.  
  
  * All data been deleted during testing **get_entries** function the resasen was first row in the google sheet sheet **row 1** did't exactly matches your **HEADERS** list which lead to activeat the if statment `if existing != HEADERS:
        ws.clear()`.
  * Inside the function `add_rainfall_record(ws)`, had a bug because it didn't validate the user's input. A user could enter "1" or "12345," and the program would accept it as a valid number, The new code fixes this by using a `while True:` loop and the condition `1000 <= year <= 9999`.
  * In the function `get_entries(ws):` Fixed data parsing bug by adding .strip() and .replace(",", ".") to handle whitespace and alternative decimal separators in input files.
  * **Wrong condition** - `if not last12_entries:`  triggered if NO entries were found, but the real issue is having fewer than 12 months therefore i ahd to channge it to : `if len(last12_entries) < 12:
    print("Not enough data to calculate.\n")
    return`
  * Fixed ealry deployment failure: Resolved SyntaxError from a stray character ('a') in run.py that crashed the Heroku app on startup.
   
    ![SyntaxError: ivalid syntax](/images/syntaxErrorIvalidSyntax.png)  

* ### Validation Testing
  * **PEP8 :** No errors founded.  
  
  * ![PEP8 Python Validator](/images/pythonValidator.png)
  



## Deployment

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.
- [rainfall-density-software](https://rainfall-density-software-7020b1171ad7.herokuapp.com/)
- [Google worksheet / rain_data](https://docs.google.com/spreadsheets/d/13GlGRDWNzIjLu406VNskZgQTsLugodR5KFMti6b02GE/edit?usp=sharing) The worksheet link.

## Credits.
- [Love Sandwiches project](https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode), the core structure of project, IDE configuration, Python virtual environment setup, API integration, and Heroku deployment 
- My mentor [Spencer Barriball](https://www.linkedin.com/in/spencerbarriball/), guide me through project, valid advice to develop the prroject and better code writing habits.
- [Kasia Bogucka](https://www.youtube.com/watch?v=nNXmC6Tq0qw) portfolio Project 3 The guide to MVP.
- [Code-Institute](https://github.com/Code-Institute-Org/p3-template)  p3-template.
- [Bro code](https://www.youtube.com/@BroCodez) python course.
- [Python Simplified](https://www.youtube.com/@PythonSimplified) OOP Class Inheritance and Private Class Members - Python for Beginners.
- [Abdelrahman Gamal](https://www.youtube.com/@AbdelrahmanGamal) كورس بايثون كامل للمبتدئين | Python for Beginners.
- [AI - Chatgpt](https://chatgpt.com/?model=auto) comment editing, function written descriptionp.
- [AI - DeepSeek](https://chat.deepseek.com/)functionality explanations, comment editing, readme file editing.
- [Python Crash Course: A Hands-on, Project-based Introduction to Programming by Eric Matthe](https://www.amazon.se/-/en/Eric-Matthes/dp/1593279280) User input and while loops, the CVS file format, Files and exceptions.
- [draw.io  diagrams ](https://www.drawio.com/)