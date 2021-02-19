# WEB APP
from flask import Flask, render_template, request
# DATA ANALYSIS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# MACHINE LEARNING
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
# MISC
import io
import urllib.parse
import base64


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():

    if request.method == "POST":

        inp_player = request.form["player"]

        fn = inp_player.split()[0].lower()
        ln = inp_player.split()[1].lower()

        df = pd.read_html(f"https://www.landofbasketball.com/nba_players_stats/{fn}_{ln}.htm")

        df = df[1]
        df = df.dropna(axis=0)
        df = df[:-1]

        try: 
            df = df[[x.startswith("2") for x in df[0]]] #only for players who have been traded MIDSEASON
        except:
            pass

        season = df[0]
        player_team = df.iloc[-1, 1]
        team_colors = {"Hawks": ["pastel red", "green/yellow"], "Celtics" : ["irish green", "desert"], "Nets" : ["black", "steel"], "Hornets" : ["dark blue", "teal"], "Bulls" : ["red", "black"],  "Cavaliers" : ["rose red", "deep blue"], "Mavericks" : ["royal blue", "navy blue"], "Nuggets" : ["midnight blue", "sunflower yellow"], "Pistons" : ["red", "royal"],  "Warriors": ["medium blue", "golden"], "Rockets" : ["red", "black"], "Pacers" : ["golden yellow", "marine"], "Clippers" : ["red", "blue"], "Lakers" : ["golden", "purple"], "Grizzlies" : ["denim", "navy"], "Heat" : ["red", "yellowish orange"], "Bucks" : ["pine green", "very light brown"], "Timberwolves" : ["midnight blue", "dull blue"], "Pelicans" : ["navy", "red"], "Knicks" : ["blue", "orange"], "Thunder" : ["deep sky blue", "blood orange"], "Magic" : ["light blue", "silver"], "76ers" : ["blue", "red"], "Suns" : ["purple", "orange"], "Trail Blazers" : ["red", "black"], "Kings" : ["purple", "grey"], "Spurs" : ["black", "silver"], "Raptors" : ["red", "black"], "Jazz" : ["navy", "green"], "Wizards" : ["navy", "red"]}

        color1, color2 = team_colors[player_team][0], team_colors[player_team][1]
 
        pts = df[4]
        pts = pts.astype(float)
 
        x = df.drop(df.columns[1], axis = 1)
        x = x.drop(columns=5)

        for item in x[0]:

            year = item.split("-")[0]
            year = int(year) 
            correct_year = year + 1
            x[0] = x[0].replace(item, correct_year)


        x = np.array(x)
        pts = np.array(pts)

        train_x, test_x, train_y, test_y = train_test_split(x, pts, test_size=0.2)

        regressor = LinearRegression()
        regressor.fit(train_x, train_y)

        y_pred = regressor.predict(test_x)
        y_pred = np.round(y_pred, 1)

        player_predicted_ppg = y_pred[-1]

        r_squared = f"R²: {round(r2_score(test_y, y_pred), 3)}"

        pred = f"I predict {fn.capitalize()} {ln.capitalize()} will average {str(player_predicted_ppg)} PPG"

        fig, ax = plt.subplots()
        ax.scatter(season, pts, c="xkcd:{}".format(color1), label = "Actual PPG", alpha=0.9)
        ax.scatter(season.iloc[-1], player_predicted_ppg, c="xkcd:{}".format(color2), label = "Predicted PPG", alpha=0.9)
        ax.set_xlabel("Season")
        ax.set_ylabel("Points Per Game")
        ax.set_xticks(season)
        plt.setp(ax.get_xticklabels(), rotation=90)
        ax.grid()
        ax.legend(loc = "best")
        fig.tight_layout()
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(season.iloc[0], np.max(pts), r_squared, fontsize = 13, bbox = props)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data = urllib.parse.quote(base64.b64encode(buf.read()).decode()) # base64 encode & URL-escape

        return render_template("index.html", text = "", plot_url=plot_data, pred=pred)
        
    else:        
        return render_template("index.html", text="Enter A Player")

@app.route("/about+me")
def about_me():
    return render_template("aboutme.html")

if __name__ == "__main__":
    app.run() #debug=True
