from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    stations = pd.read_csv("data_small/stations.txt", skiprows=17)
    stations = stations[["STAID", "STANAME                                 "]]
    # .to_html() method takes the table like structure of the dataframe and converts it to its html equivalent.
    return render_template('home.html', data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def about(station, date):
    # zfill() automatically fills any str(num here) with n(arg) number of zeros.
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"Station": station,
            "Date": date,
            "Temperature": temperature}


@app.route('/api/v1/yearly/<station>/<year>')
def annual(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    # Series.str can be used to access the values of the series as strings and apply several methods to it.
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    print(result)
    return result


@app.route('/api/v1/<station>')
def station(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # attribute "orient=" changes how the dict is structured.
    result = df.to_dict(orient="records")
    return result


if __name__ == '__main__':
    app.run(debug=True)
