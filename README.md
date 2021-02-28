Full fledge Flask app (Python) where the user enters a player and Linear Regression is used to predict the player's PPG in the coming season. The web service used to host is Heroku.
The data was gathered from https://www.landofbasketball.com/.

View the website here! -> https://nba-machine-learning.herokuapp.com

**Tutorial On Deploying**:

1. Download Git from https://git-scm.com/

2. Go to https://signup.heroku.com/t/platform?c=70130000001xDpdAAE&gclid=CjwKCAiA1eKBBhBZEiwAX3gqlzjIi4nefhuRwjQW4oDljJPn5Z4s_oOQRUJcrUJzyndyJ3j52LCiwBoCpb4QAvD_BwE & make an account

3. Download the Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli#download-and-install

4. Go to https://dashboard.heroku.com/apps and create an app.

4. Open cmd/terminal

5. CD to the directory of your project

6. Create a virtualenv ("virtualenv {name of environment}" ) & activate it ("{nameofenv}\Scripts\activate") OR use a conda virtual environment

7. Login using "heroku login" or "heroku login -i" if the former doesn't work

8. Pip install flask, gunicorn, and the necessary modules

9. Run "pip freeze > requirements.txt", this is so Heroku knows your app is a Python app

10. Run "echo (or touch if on Mac/Linux) web: gunicorn app: app (change it if the app is called something besides 'app') > Procfile"

11. Run "git init" to create an empty Git repository

12. Run "git add . " to add all of the files to the repo

13. Run "git commit -m {message} ". If you ever make any other commits (updating/deleting/adding files), rerun this and change the message.

13. Run "git remote -v" to see where you can push to

14. Finally, run "git push heroku master". Now copy the given URL and you are done!
