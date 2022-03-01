import requests
import typer
import inquirer
from yaspin import yaspin
import pyfiglet
import datetime
from tabulate import tabulate

API_KEY="XXXXXXXXXXXXXXXXXX"

units = dict(
  metric="°C",
  imperial="°F"
)

def weatherDataToTable(data, unit):
  day=datetime.datetime.fromtimestamp(data['dt'])
  return [f"{day:%d.%m.%Y}", minMaxTemp(data, unit)]

def fetchWeeklyWeather(lon, lat, unit):
  params = dict(
    lon=lon,
    lat=lat,
    units= unit,
    exclude="current,hourly,minutely,alerts",
    appid= API_KEY
  )
  API_URL = "http://api.openweathermap.org/data/2.5/onecall"
  response = requests.get(url=API_URL, params=params)
  return response.json()["daily"]

@yaspin(text="Fetching weather data...")
def fetchWeather(city, country, unit):
  params = dict(
    q=f"{city},{country}",
    units= unit,
    appid= API_KEY
  )
  API_URL = "http://api.openweathermap.org/data/2.5/weather"
  response = requests.get(url=API_URL, params=params)
  lon=response.json()["coord"]["lon"]
  lat=response.json()["coord"]["lat"]
  return fetchWeeklyWeather(lon, lat, unit)

def minMaxTemp(data, unit):
  return "{}{} to {}{}".format(round(data["temp"]["min"]), units[unit], round(data["temp"]["max"]), units[unit])

def main(
  city: str = typer.Option(..., prompt=True),
  country: str = typer.Option(..., prompt=True)
):
  unit = inquirer.list_input("Metric or imperial?", choices=['metric', 'imperial'])
  weatherData=fetchWeather(city, country, unit)
  print(pyfiglet.figlet_format(minMaxTemp(weatherData[0], unit)))
  tabledata = map(lambda x: weatherDataToTable(x, unit), weatherData)
  headers = ["Date", "Temperature range"]
  print(tabulate(tabledata, headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    typer.run(main)
