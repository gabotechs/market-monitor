# Market Monitor
Real time dashboard for monitoring stocks / crypto market. With useful insights
like most recent news, market sentiment analysis, etc...

# Install

Currently, only installation through docker is supported, so this steps assume that
you have docker installed in your machine. If you don't have it installed, check this 
link https://docs.docker.com/get-docker/

- Create your `.env` file, you can copy-paste `.env.example` and change the values.
It should contain this info:
```dotenv
INFLUXDB_TOKEN=some-token # This can be anything, but if you are going to expose the dashboard
                        # over a network, you may want to make this a secure string.
INFLUXDB_ADMIN_PASSWORD=some-pass # This is the password that will be used to access the dashboard
                                  # as an the "admin" user.
SYMBOLS=AAPL,TSLA,MSFT,GOOG,NVDA,AMD,NET # The symbols you want to monitor
```
- Open a terminal and execute `docker compose up`
- Open your browser, go to http://localhost:8086 and login with username "admin" and
the password you declared in your `.env` file
- Once logged in, in the navigation bar in the left go to "Boards", click on "Create Dashboard"
and on "Import Dashboards" in the dropdown. The file you want to import lives in the root directory
of this project, and its name is `dashboard.json`