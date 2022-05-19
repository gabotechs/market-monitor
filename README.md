# Market Monitor

### Real time dashboard for monitoring stocks and crypto, with twitter sentiment analysis and useful market insights.

<p align="center"> <img alt="" src="docs/dashboard.png"> </p>

# Install

Currently, only installation through docker is supported, so this steps assume that
you have docker installed in your machine. If you don't have it installed, check this 
link https://docs.docker.com/get-docker/

- Clone the project `git clone https://github.com/GabrielMusat/market-monitor.git`
- Navigate to the projects dir `cd market-monitor`
- Create your `.env` file. You can copy-paste `.env.example` and change the values.
It should contain this info:
```python
# INFLUXDB_TOKEN can be anything, but if you are going to expose the dashboard
# over a network, you may want to make this a secure string.
INFLUXDB_TOKEN="some-token"
# INFLUXDB_ADMIN_PASSWORD is the password that will be used to access the dashboard
# as the "admin" user.
INFLUXDB_ADMIN_PASSWORD="some-pass"
# SYMBOLS is a comma sepparated list with the symbols you want to monitor
SYMBOLS="AAPL,TSLA,MSFT,GOOG,NVDA,AMD,NET"
# (optional) TWITTER_TOKEN is the bearer token of your twitter application
TWITTER_TOKEN="your-apps-bearer-token"
```
> **_Note:_** Currently, the maximum number of symbols is 10
- Execute `docker compose up -d`, this will run this project in the background
- On your browser, go to http://localhost:8086 and login with username "admin" and
the password from your `.env` file under the `INFLUXDB_ADMIN_PASSWORD` key
- Once logged in, in the navigation bar at the left, go to "Boards", click on "Create Dashboard"
and on "Import Dashboards" in the dropdown. The file you want to import lives in the root directory
of this project, and its name is `dashboard.json`
- Once imported, a new dashboard named "Market" should be available

# Update

- Inside the cloned project directory, pull the latest changes `git pull`
- rebuild and launch the docker images `docker compose up --build -d`

# Twitter sentiment analysis

If you configure the `TWITTER_TOKEN` in your `.env` file, you will get most recent tweets
from some well known accounts and perform sentiment analysis using AI on them. In order to
get one `TWITTER_TOKEN` you must create a developer account and an application.

In this link https://developer.twitter.com/apps you will find how to create one application.
Once you have your application created, in the developer portal, select your application and
go to the "Keys and tokens" tab. The token you want is the "Bearer Token" under "Authentication tokens"

# Customize

This project follows a plugin architecture, where it's easy to develop new plugins and extend
the data collection features with just a few lines of code. You can see [here](src/metric_collectors)
the current plugins that collect data from Yahoo finance api and Twitter.

Plugins are hooked up with the metrics collector [here](src/main.py). The data collected by 
the plugins will be available to be displayed in the **InfluxDB** dashboard, which uses the
**flux** query language to gather and display data.

You can read more about **InfluxDB** and **flux** here https://docs.influxdata.com/influxdb/v2.2/


# Disclaimer

This project is for educational purposes only, use it at your own risk. The contributors
of this project assume no responsibility for your trading decisions or results. We advise
you to not risk any money that you are afraid to lose.