# **🎬 Media Hub** 


## Project Description

Media Hub exist as a perfect resource tool to find and store all genres of media. 



## Project Requirements
### Libraries to install:
- Flask
- Requests
- os
- SQLAlchemy
- JSON
- Pandas
- Googlesearch
- pprint


### APIs used:
- Google Books
- Kitsupy
- The moviedb API
- Youtube music API
- Tasty
- Edamama API

## How to setup and run
Before running the program, please make sure you have the required packages installed on your machine. 
Please also note that the some of the APIs require authentication from the user, so setup is required. 
Download a zip file of our code and unzip it. 
You can run the program from your computer terminal, a python IDLE, or a source-code editor (such as Visual Studio Code). 
If you want run the program with the python command, you need to open a command-line and enter the following:

==python3 main.py==

Please note: You must be in the directory that the file is in to run it. 

### Contributors
- Aubrey Robinson
- Ini Davies
- Kyle Oliver
- Mark Karomo




### Additional info
Registration for Api keys is required for the following Apis
1. **Google books**
- Set up a Google developer account
[Set up here](https://console.developers.google.com/)
- Make an app
- Enable books Api
- copy the api secret key and create an environment variable in the format below:
- Run sudo nano ~/.bashrc
- Scroll to the bottom and paste this code snippet:
- export BOOK_API_KEY=["your api key"]
- Press ctrl/cmd + x to exit out
- When prompted press y to save
- Type source ~/.bashrc and run it in the terminal

2. **The movie database API**
- Set up a movie db account.
- Register for an api key
[Set up here](https://developers.themoviedb.org/3/getting-started/introduction)
- copy the api secret key and create an environment variable in the format below:
- Run sudo nano ~/.bashrc
- Scroll to the bottom and paste this code snippet:
- export BOOK_API_KEY=["your api key"]
- Press ctrl/cmd + x to exit out
- When prompted press y to save
- Type source ~/.bashrc and run it in the terminal


==PS: Ensure you are working in the correct directory==
