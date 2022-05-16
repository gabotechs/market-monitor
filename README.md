# Market Monitor

### Real time dashboard for monitoring stocks / crypto market.

<p align="center"> <img alt="" src="docs/dashboard.png"> </p>

# Install

Currently, only installation through docker is supported, so this steps assume that
you have docker installed in your machine. If you don't have it installed, check this 
link https://docs.docker.com/get-docker/

- Clone the project `git clone https://github.com/GabrielMusat/market-monitor.git`
- Navigate to the projects dir `cd market-monitor`
- Create your `.env` file. You can copy-paste `.env.example` and change the values.
It should contain this info:
```dotenv
# INFLUXDB_TOKEN can be anything, but if you are going to expose the dashboard
# over a network, you may want to make this a secure string.
INFLUXDB_TOKEN=some-token
# INFLUXDB_ADMIN_PASSWORD is the password that will be used to access the dashboard
# as the "admin" user.
INFLUXDB_ADMIN_PASSWORD=some-pass
# SYMBOLS is a comma sepparated list with the symbols you want to monitor
SYMBOLS=AAPL,TSLA,MSFT,GOOG,NVDA,AMD,NET
```
> note: Currently, the maximum number of symbols is 10
- Open a terminal and execute `docker compose up -d`, this will run this project in the background
- On your browser, go to http://localhost:8086 and login with username "admin" and
the password you declared in your `.env` file under the `INFLUXDB_ADMIN_PASSWORD` key
- Once logged in, in the navigation bar in the left, go to "Boards", click on "Create Dashboard"
and on "Import Dashboards" in the dropdown. The file you want to import lives in the root directory
of this project, and its name is `dashboard.json`
- Once imported, a new dashboard named "Market" should be available

# Update

- Inside the cloned project directory, pull the latest changes `git pull`
- rebuild and launch the docker images `docker compose up --build -d`
