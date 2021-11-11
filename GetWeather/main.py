from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
import requests

# delhi key = "202396"
 
class City():

  text = "Delhi"
  secondary_text = "India"
  tertiary_text = "202396"

  current = {
    "WeatherText": "",
    "WeatherIcon": "",
    "DateTime": "22/22/22 22:22:22+05:30",
    "Temperature": "",
    "RealFeelTemperature": "",
    "DewPoint": "",
    "CloudCover": "",
    "RelativeHumidity": "",
    "IndoorRelativeHumidity": "",
    "Wind": "",
    "WindGust": "",
    "UVIndex": "",
    "Visibility": "",
    "Pressure": "",
    "Precipitation": "",
    "SunRise": "",
    "SunSet": "",
    "MoonRise": "",
    "MoonSet": ""
  }

  forecast = {
  	"Date": "",
  	"WeatherText": "",
  	"MinTemp": "",
  	"MaxTemp": "",
  	"MinRealFeel": "",
  	"MaxRealFeel": "",
  	"HrsOfSun": "",
  	"AirQuality": "",
  	"UVIndex": ""
  }

  day_forecast = {
  	"Icon": "",
  	"Text": "",
  	"PrecpProb": "",
  	"ThunderProb": "",
  	"RainProb": "",
  	"SnowProb": "",
  	"IceProb": "",
  	"CloudCover": "",
  	"Wind": "",
  	"WindGust": ""
  }

  night_forecast = {
  	"Icon": "",
  	"Text": "",
  	"PrecpProb": "",
  	"ThunderProb": "",
  	"RainProb": "",
  	"SnowProb": "",
  	"IceProb": "",
  	"CloudCover": "",
  	"Wind": "",
  	"WindGust": ""
  }

class ConfirmCity(ThreeLineAvatarIconListItem):
	divider = None
	check = ObjectProperty(None)

class GetWeather(MDApp):
	api_key = "wIbO7AmIwOQLzaXAq5XY73kxXsjHhaVO"
	dialog = None
	selected_city = City()

	def build(self):
		return Builder.load_file("design.kv")

	def call_api(self, api):
		try:
			toast("SEARCHING...")
			data = requests.get(api)
			if data.status_code != 200:
				raise ValueError
			return data.json()
		except:
			toast("Error!!!")

	def searched(self, searched_text):
		
		if len(searched_text) == 0:
			toast("Enter something first")
				
		else:
			searched_cities = self.call_api(f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={self.api_key}&q={searched_text}")
			if not searched_cities :
				return
			list_cities = []
			for i in range(len(searched_cities)):
				list_cities.append(
					ConfirmCity(
						text = searched_cities[i]["LocalizedName"],
						secondary_text = searched_cities[i]["Country"]["LocalizedName"],
						tertiary_text = searched_cities[i]["Key"],
						)
					)

			list_cities[0].check.active = True
			self.selected_city.text = list_cities[0].text
			self.selected_city.secondary_text = list_cities[0].secondary_text
			self.selected_city.tertiary_text = list_cities[0].tertiary_text
			print(self.selected_city.text)

			if not self.dialog:
				self.dialog = MDDialog(
					title = "Select Your City",
					type = "confirmation",
					items = list_cities,
					auto_dismiss = False,
					size_hint = (.9, .5),
					buttons = [MDFlatButton(text = "Ok", on_release = self.update_main_screen_data),],
					)
				self.dialog.open()

	def close_dialog(self, *args):
		if self.dialog:
			self.dialog.dismiss()
			self.dialog = None

	def select_city(self, instance_check, city_item):
		instance_check.active = True
		self.selected_city.text = city_item.text
		self.selected_city.secondary_text = city_item.secondary_text
		self.selected_city.tertiary_text = city_item.tertiary_text
		print(self.selected_city.text)

		check_list = instance_check.get_widgets(instance_check.group)
		for check in check_list:
			if check != instance_check:
				check.active = False

	def update_main_screen_data(self, *args):
		self.close_dialog()

		current_data = self.call_api(f"http://dataservice.accuweather.com/currentconditions/v1/{self.selected_city.tertiary_text}?apikey={self.api_key}&details=true")
		forecast_data = self.call_api(f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{self.selected_city.tertiary_text}?apikey={self.api_key}&details=true&metric=true")
		if not current_data or not forecast_data:
			return

		#Write here Logic to fill data in the city obj
		self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		self.selected_city.current['WeatherIcon'] = str(current_data[0]['WeatherIcon']) if current_data[0]['WeatherIcon']>=10 else "0"+str(current_data[0]['WeatherIcon'])
		# self.selected_city.current['Temperature'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']
		# self.selected_city.current['WeatherText'] = current_data[0]['WeatherText']

		
		self.root.ids.city_info.text = f"{self.selected_city.text}, {self.selected_city.secondary_text}"
		self.root.ids.current_weather_text.text = self.selected_city.current['WeatherText']
		self.root.ids.current_weather_icon.source = f"https://developer.accuweather.com/sites/default/files/{self.selected_city.current['WeatherIcon']}-s.png"
		self.root.ids.current_temp.text = f"{self.selected_city.current['Temperature']} \u00B0C"
		self.root.ids.current_datetime.text = self.selected_city.current['DateTime']
		self.root.ids.current_real_feel_temp.text = f"{self.selected_city.current['RealFeelTemperature']} \u00B0C"
		self.root.ids.current_dew_point.text = f"{self.selected_city.current['DewPoint']} \u00B0C"
		self.root.ids.current_cloud_cover.text = f"{self.selected_city.current['CloudCover']} %"
		self.root.ids.current_relative_humidity.text = f"{self.selected_city.current['RelativeHumidity']} %"
		self.root.ids.current_indoor_relative_humidity.text = f"{self.selected_city.current['IndoorRelativeHumidity']} %"
		self.root.ids.current_wind.text = f"{self.selected_city.current['Wind']} km/hr"
		self.root.ids.current_wind_gust.text =  f"{self.selected_city.current['WindGust']} km/hr"
		self.root.ids.current_uv_index.text = self.selected_city.current['UVIndex']
		self.root.ids.current_visibility.text = f"{self.selected_city.current['Visibility']} km"
		self.root.ids.current_pressure.text = f"{self.selected_city.current['Pressure']} mb"
		self.root.ids.current_precipitation.text = f"{self.selected_city.current['Precipitation']} mm"
		self.root.ids.current_date.text = self.selected_city.current['DateTime'].split()[0]
		self.root.ids.sun.text = f"Rise:{self.selected_city.current['SunRise']}\nSet:{self.selected_city.current['SunSet']}\n{self.selected_city.current['DateTime'].split()[1][-6:]}"
		self.root.ids.moon.text = f"Rise:{self.selected_city.current['MoonRise']}\nSet:{self.selected_city.current['MoonSet']}\n{self.selected_city.current['DateTime'].split()[1][-6:]}"
		self.root.ids.forecast_date.text = self.selected_city.forecast['Date']
		self.root.ids.forecast_weather_text.text = self.selected_city.forecast['WeatherText']
		self.root.ids.forecast_min_temp.text = f"{self.selected_city.forecast['MinTemp']} \u00B0C"
		self.root.ids.forecast_max_temp.text = f"{self.selected_city.forecast['MaxTemp']} \u00B0C"
		self.root.ids.forecast_min_real_feel.text = f"{self.selected_city.forecast['MinRealFeel']} \u00B0C"
		self.root.ids.forecast_max_real_feel.text = f"{self.selected_city.forecast['MaxRealFeel']} \u00B0C"
		self.root.ids.forecast_hrs_of_sun.text = self.selected_city.forecast['HrsOfSun']
		self.root.ids.forecast_air_quality.text = self.selected_city.forecast['AirQuality']
		self.root.ids.forecast_uv_index.text = self.selected_city.forecast['UVIndex']
		self.root.ids.day_forecast_date.text = self.selected_city.forecast['Date']
		self.root.ids.day_forecast_icon.source = f"https://developer.accuweather.com/sites/default/files/{self.selected_city.day_forecast['Icon']}-s.png"
		self.root.ids.day_forecast_text.text = self.selected_city.day_forecast['Text']
		self.root.ids.day_forecast_precp_prob.text = f"{self.selected_city.day_forecast['PrecpProb']} %"
		self.root.ids.day_forecast_thunder_prob.text = f"{self.selected_city.day_forecast['ThunderProb']} %"
		self.root.ids.day_forecast_rain_prob.text = f"{self.selected_city.day_forecast['RainProb']} %"
		self.root.ids.day_forecast_snow_prob.text = f"{self.selected_city.day_forecast['SnowProb']} %"
		self.root.ids.day_forecast_ice_prob.text = f"{self.selected_city.day_forecast['IceProb']} %"
		self.root.ids.day_forecast_cloud_cover.text = f"{self.selected_city.day_forecast['CloudCover']} %"
		self.root.ids.day_forecast_wind.text = f"{self.selected_city.day_forecast['Wind']} km/hr"
		self.root.ids.day_forecast_wind_gust.text = f"{self.selected_city.day_forecast['WindGust']} km/hr"
		self.root.ids.night_forecast_date.text = self.selected_city.forecast['Date']
		self.root.ids.night_forecast_icon.source = f"https://developer.accuweather.com/sites/default/files/{self.selected_city.night_forecast['Icon']}-s.png"
		self.root.ids.night_forecast_text.text = self.selected_city.night_forecast['Text']
		self.root.ids.night_forecast_precp_prob.text = f"{self.selected_city.night_forecast['PrecpProb']} %"
		self.root.ids.night_forecast_thunder_prob.text = f"{self.selected_city.night_forecast['ThunderProb']} %"
		self.root.ids.night_forecast_rain_prob.text = f"{self.selected_city.night_forecast['RainProb']} %"
		self.root.ids.night_forecast_snow_prob.text = f"{self.selected_city.night_forecast['SnowProb']} %"
		self.root.ids.night_forecast_ice_prob.text = f"{self.selected_city.night_forecast['IceProb']} %"
		self.root.ids.night_forecast_cloud_cover.text = f"{self.selected_city.night_forecast['CloudCover']} %"
		self.root.ids.night_forecast_wind.text = f"{self.selected_city.night_forecast['Wind']} km/hr"
		self.root.ids.night_forecast_wind_gust.text = f"{self.selected_city.night_forecast['WindGust']} km/hr"




if __name__ == "__main__":
	GetWeather().run()
