# BMI Calculator: a body mass index calculation app

'BMI Calculator' is a command-line-interface (CLI) health app hosted as an app on Heroku, written in Python.

## Purpose 
The objective of this app is to provide the user with a guidence to reach and maintain healthy body weight. Through calculation of
body mass index, the application will update the user about the current body weight range and let's the user track the changes over 
time.

## Requirement Gathering and Planning

Before starting the coding for this project, I took the time to think about how to set up the architecture of this app, the layout of the output on the console and the functionality required to provide a good user experience. As the CI study material advised, I kept it simple,
and I tried to follow a 'linear' logic.

![Wireframe logic](documentation/wireframelogic.png)

## User Demographics, Stories and Needs

### Target Demographic
This app is useful for anyone wanting to track and control their body mass index and through that, their health.
Abnormal bodyweight is linked with several illness and diseases, when one decides to make change for the better, the use of this application
could be the first step towards a healthier lifestyle.

 Some examples of such people are: 

- Family history: people who's family has a history of diabetes, heart disease, obesity.
- Sedentary lifestyle: People at full time work and with familiy duties who won't have time for their own activities, always low
on energy. 
- Eating disorder/ body image issues: people who are following extreme diets, trends, pursuing the lowest possible body weight.

### User Stories

|As a body mass index calculator user, I want to... | So that... |
|--------|--------|
| ...check my body mass index. | ...I will have an indicator of my generic health. |
| ...know that in what weight category do I fall. | ...I would know if I have to gain, maintain or lose weight.|
| ...receive specific information with regards of my weight. | ...I will have a clear number to gain or lose. |
| ...I want to save my calculation. | ...I can start tracking my weight change, bmi change over time. |
| ...to be able to re-do the calculation. | ...in case any of my details were not accurate, I could repeat the calculation. |
| ...to be able to delete my last calculation, results. | ...no one else could access my details, or I just want to repeat it at a different time. |
| ...have a clear and intuitive method of navigating through the app via the command line. | ...I can easily navigate and use the app. |

## Technologies Used

### Language Used

+ Python


### Frameworks, Libraries & Programs Used

1. Google Sheet: 
+ Google sheet was used to connect with the app in order to store data on a spreadsheet.

2. Google Cloud Platform
- to set up API's.

3. Google Sheets API

4. Google Drive API

5. GitHub
- Github was used to store the project after being pushed

6. VS Code Editor
- To write and run the code VS Code editor was used which is Code Institute's cloud based IDE platform.

### Data Model

The data model and the use of 'CRUD' operations are central to the functioning of this CLI app. The data is stored in a Google Sheet and is not lost between sessions. 

### Validation
- There are different types of validation depending on the user input type: 

![Data Validation](documentation/datavalidation1.png)

![Data Validation](documentation/datavalidation2.png)

1. Validation of negative values 
    - This checks whether the user has entered a negative value
2. Validation for string
    - This checks if the users' input is a string
3. Validation for blank
    - This checks if the user did put any value at all


#### To be implemented
- Determining a range of input both for weight and height values to avoid extreme results at the calculation

## Features

1. Main Menu
2. Weight input - with example
3. Height input - with example
4. BMI Result
5. BMI Category
6. Weight to lose/gain - if applies
7. Delete last entry
8. End program/ restart calculation

### Main Menu

![Main menu](documentation/programstart.png)

### Weight, height input - with example

![Weight input](documentation/userinputfields.png)

### BMI Result, category

![Bmi result](documentation/processeddata.png)

### Weight to lose/gain - if applies

![Weight loss](documentation/weighttolose.png)

### Delete last entry, end program

![Last entry](documentation/laststep.png)



## Testing

I took a test-as-you-go approach - testing after each change to ensure that my desired outcome was achieved. 

I also completed an end-to-end test covering these aspects, at milestones throughout the project:

- Test each user journey from start to finish
- Test going home from every input possible
- Test every input with invalid inputs, empty inputs and extreme values (where applicable)



| Feature | Action | Outcome |
|----------|----------|----------|
| Weight input    | Correct value    | Program moves to next step   |
| Weight input    | Negative value   | Error message displayed, program back to start   |
| Weight input    | Blank/ string   | Error message displayed, program back to start   |
| Height input    | Correct value   | Program moves to next step, calculation triggered   |
| Height input    | Negative value   | Error message displayed, program asks to re-enter data   |
| Height input    | Blank/ string   | Error message displayed, program asks to re-enter data   |
| Last entry     | Delete last entry - no   | Last entry and result will be saved in google sheets   |
| Last entry    | Delete last entry - yes  | Last entry and result will be deleted from google sheets    |
| Recalculate    | Calculate again - yes   | Program returns to the start point   |
| Recalculate   | Calculate again - no  | Program ends  |


### Important
- At this stage there are still no high or low values set to avoid extreme, non realistic results.
- The calculation will go ahead even if someone would put in 500 kg's as body weight or 3.78 as height.
![Extreme values](documentation/extremevalues.png)

-Looking at other bmi calculators online this seems to be a common problem...

(https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmi-m.htm)

![Extreme bmi](documentation/extremebmi.png)

(https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/metric_bmi_calculator/bmi_calculator.html)

![Extreme bmi2](documentation/extremebmi2.png)

- For future improvement I'm looking for the pricipal that could be implemented to avoid extreme results.
- An alternative solution would be to display a second, confirmation message for the user just before triggering the calculation.

### Code Validation
PEP8 validation using the Code Institute Python Linter was completed at milestones throughout the project and once right at the end. Mutiple errors of indentation, blank line whtitespace and long lines were found.

![Pip8 errors](documentation/pip8linterbugs.png)

Fixed the errors mentioned above by staying with the current set of code. With more time avilable another approach would have been to re-factor some of the code.

![Fixed errors](documentation/fixedbugs.png)

### Browser compatibility
Tested the application on **Chrome**, **Safari**, **Firefox**.
Appearance normal, functions working.

### Unfixed Bugs

Not that I am aware of at this stage.


## Deployment

This project was deployed to [Heroku](https://id.heroku.com/login): a hosting platform and is accessible via the mock terminal displayed on the [dedicated app page here](https://bmi-calculator-6b92d479472a.herokuapp.com/). 

These are the steps I took to set up my infrastructure and deploy my app:

1. Created a blank [Google Sheet](https://docs.google.com/spreadsheets/d/1dEQo7Hksi_dG7rFAgZyFmY7vDs_IfEl-ca-bAwBe-nA/edit?gid=1680754323#gid=1680754323) to store my data with the name 'bmi_calculator'.
2. Created a new project on the [Google Cloud Platform](https://console.cloud.google.com/welcome?project=portfolioprojectthree) by clicking 'New Project' from the project selection dropdown in the top menu bar.
3. Navigated to the 'Portfolioprojectthree' project page and clicked on 'APIs & Services' in the left hand burger menu. 
4. From here I enabled the 'Google Drive API' and navigated to the 'Credentials' section. I set the API being used as the 'Google Drive API' and the type of data I'll be accessing to 'Application Data'. I answered 'No' to the question asking me if I would be using one or more of a specific set of other services.
5. Next I set up the Service Account details with a name and the editor role, leaving everything else blank.
6. When this was created I clicked on the service account on the next page, and the 'Keys' tab, where I created a new JSON key file which I downloaded to my computer.
7. Next, I enabled the Google Sheets API. This was just a case of searching for this API on from the 'APIs & Services' page and clicking 'Enable'. Nothing further was required.
8. I created a new repository on my GitHub from the [Code Institute template](https://github.com/Code-Institute-Org/p3-template) and named it 'Portfolio-project-three'.
9. I opened this repo on my IDE and uploaded the JSON key file from earlier, renaming it 'creds.json'. This was then added to the gitignore file so that the credentials are not sent to GitHub.
10. The service account details from the creds.json file, listed as 'client_email' were added to the Google Sheet as a user to enable the app to read and write data from and to it. 
11. On Heroku, in the settings, a config var named 'CREDS' was created and the contents of the creds.json file were added to the value field, to enable Heroku to access the app. 
12. I added another config var called 'PORT' set to '8000' here too. 
13. Further dependencies required outside of those in the requirements.txt file found in my repository, were added via buildpacks on Heroku, again found in the settings. Firstly, 'python' and then 'nodejs' in that order.
14. Next I clicked on the 'Deploy' tab and connected my github repository code to the Heroku app. I clicked 'Manually deploy' and Heroku deployed the app for me. Once this was done, the link to the app appeared and could be clicked to go to the deployed app.

## Credits

### APIs and Third Party Libraries
1. [Google Sheets API: 'gspread'](https://docs.gspread.org/en/v6.0.0/) - This was installed to provide access to the associated spreadsheet which will hold all the data for BMI calculator.
2. [Date/Time Module: 'datetime'](https://docs.python.org/3/library/datetime.html) - This was installed to provide dates to work with, so a history of body weight and body mass index change can be made.

### BMI 
1. Calculation and formula of body mass index was taken from (https://www.diabetes.ca/resources/tools---resources/body-mass-index-(bmi)-calculator#:~:text=Body%20Mass%20Index%20is%20a,range%20is%2018.5%20to%2024.9.)
2. BMI chart to determine categories was taken from (https://calculatorsworld.com/health/bmi-chart-men-women-metric/#google_vignette)

### Sources of Learning
I referred back to the Love Sandwiches Walkthrough Project set up videos to remind me how to set up the APIs, credentials and files before starting coding.


### Acknowledgement 
Grateful for the help and the input from my mentor **Can Sücüllü**.
He always gave a different perspective on the issues and with his experience
and eyes for details I was guided in the right direction to make this project happen.







