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
   
  This application is a Rain Density Calculator that stores data in Google Sheets. It lets you log rainfall data, calculate density, and analyze trends over time.  
### 1. **Startup**  
   
     * When the program runs, it connects to a Google Sheet called rain_data.
     * If the worksheet (sheet1) doesn’t exist, it creates one automatically.
     * A header row is prepared with these columns:  
        - year | month | rain_volume(mm/h) | area_m2 | density | save_at.

### 2. **Main Menu**   
   
  ![Main Menu Options](/images/rainfullDensityMenu.png)  
  
### 3. **Menu Options**
   
=== Rain Density Menu ===
1) Add monthly entry (compute & save)
2) Density calculator (no save)
3) Show past entries
4) Show 12-month average density
5) Export help (CSV)
6) Exit

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
    
### 4. **Error Handling**

  *  If credentials are missing/invalid or internet is down → the program exits with a friendly error message.
  *  Invalid inputs (non-numbers, out of range values) trigger a retry until valid data is entered.  
  *  Invalid menu choices print an error and return to the menu.
 
 


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
  
## Program sturcture diagram  
   ![Program sturcture digram ](/images/rainDensityDiagram.png)  


## Testing  
* ### Browser Testing  
     * | Browser       | Operation system | Responsiveness     |
       | :-----------: |:----------------:| :-----------------:|
       |     chrome    |   Windows 11     |    Very good       |
       |      Edge     |   Windows 11     |    Very good       |
       |     FireFox   |   Windows 11     |    Very good       |


* ### Manual Testing.  
   


| Feature Tested                                 | Test Input                                  | Expected Result                                               | Actual Result                                        | Pass/Fail |
| ---------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------- | --------- |
| **Add monthly entry**                          | Year: 2025, Month: 5, Volume: 120, Area: 40 | Entry saved in Google Sheets, density = 3.0 mm/h per m²       | Entry saved correctly, density displayed as expected | ✅ Pass    |
| **Add monthly entry (invalid year)**           | Year: `abcd`                                | Error message shown, retry prompt                             | Error handled, program requested correct input       | ✅ Pass    |
| **Add monthly entry (invalid month)**          | Month: 15                                   | Error message shown, retry prompt                             | Error handled, program requested correct month       | ✅ Pass    |
| **Add monthly entry (invalid area)**           | Area: -20                                   | Error message shown, retry prompt                             | Error handled, program requested valid area          | ✅ Pass    |
| **Density calculator**                         | Volume: 100, Area: 50                       | Density = 2.0 mm/h per m², no save to sheet                   | Correct density displayed, nothing saved             | ✅ Pass    |
| **Show past entries**                          | Select option 3                             | Display last entries from Google Sheets                       | Correct entries shown                                | ✅ Pass    |
| **12-month average density**                   | Select option 4 (with ≥12 entries in sheet) | Average density displayed correctly                           | Correct result displayed                             | ✅ Pass    |
| **12-month average density (not enough data)** | Select option 4 (with <12 entries)          | Message: "Not enough data to calculate."                      | Correct message displayed                            | ✅ Pass    |
| **Export help**                                | Select option 5                             | Instructions to download CSV shown                            | Instructions displayed correctly                     | ✅ Pass    |
| **Exit program**                               | Select option 0                             | Program exits with goodbye message                            | Program exited, copyright message shown              | ✅ Pass    |
| **Heroku deployment**                          | Run app via Heroku URL                      | Program loads, menu visible, all functions work same as local | Application works correctly on Heroku                | ✅ Pass    |

     




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
  
     ![PEP8 Python Validator](/images/pythonValidator.png)
  



## Deployment  
This project is deployed using Heroku with GitHub integration.

1. Prerequisites  
   * A Herok account. 
   * A linked GitHub repository containing this project.
   * creds.json (Google Service Account credentials) already added securely as Config Vars (not uploaded to the repo).  
  
2. Connect GitHub to Heroku.  
   * Log in to my Heroku Dashboard
   * Click New → Create new app.
   * Choose a unique App name and your region, then click Create app.
   * Search for your repository *(rainfall_density_software)* and click Connect.  

3. Set Config Vars  
   This project requires authentication for Google Sheets via service account credentials.
   Instead of uploading creds.json directly, you must add its content as an environment variable:  
   * Go to your Heroku app → Settings → Config Vars.
   * Click Reveal Config Vars.  
      * Keys: CREDS , PORT
      * Values: creds.json information, 4- digit number  

4. Add Buildpacks
   * Navigate to Settings → Buildpacks.
   * Add the following buildpacks in order:
      * heroku/python
      * heroku/nodejs  
  
5. Deploy the App  
   * In the Deploy tab, I selected the branch I wanted to deploy (main).  
   * Clicked Deploy Branch.  
   * I Waited until the build finishes successfully.  
   * Click Open App to launch your deployed application.  
   * 
6. Enable Automatic Deploys  
   *  In the Deploy tab, enable Automatic deploys from GitHub.
   *  This ensures every push to my GitHub repository, will automatically trigger a new Heroku build.


- 🌐 **Live App on Heroku:** [rainfall-density-software](https://rainfall-density-software-7020b1171ad7.herokuapp.com/) 
- 📊 **Sample Data on Google Sheets:** [Google worksheet / rain_data](https://docs.google.com/spreadsheets/d/13GlGRDWNzIjLu406VNskZgQTsLugodR5KFMti6b02GE/edit?usp=sharing) The worksheet link.






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