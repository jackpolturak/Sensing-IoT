from time import time
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from refresh import Refresher
import requests


#IMPROT SPREADSHEETS FOR DATA APPENDAGE
sa = gspread.service_account(filename="client_secret.json")
sh = sa.open("current_track_info")
wks = sh.worksheet("dataset")

wks_refresh = sh.worksheet("refresh_token")
val = wks_refresh.acell('A1').value



class Add_to_sheets:
	def __init__(self):

		self.fitbit_token = ""
		self.heart_rows = list(wks.col_values(18))
		self.number_of_heart_rows = str(len(self.heart_rows))
		self.number_of_song_rows = str(len(list(wks.col_values(1))))


	

	def next_available_row(self):
		print("Adding to sheets...")
		number_of_rows = list(wks.col_values(2))
		next_available_row = str(len(number_of_rows)+1)
		next_available_index = str(len(number_of_rows))
		wks.update("A{}".format(next_available_row), "{}".format(next_available_index))
		wks.update("B{}".format(next_available_row), [self])



	def fill_heartrate(self):

		#Find next available heartrate cell
		heart_rows = list(wks.col_values(18))
		

		number_of_heart_rows = str(len(heart_rows))

		next_available_heart_cell = str(len(heart_rows)+1)


		#define the length of whole google sheet data
		number_of_song_rows = str(len(list(wks.col_values(1))))
		#Corresponding time value son
		time_value_corresponding_song = wks.acell('C{}'.format(next_available_heart_cell)).value

		

		#get fitbit data form API
		fit_bit_heartrate_today = requests.get('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json',
										headers={'Authorization': 'Bearer {}'.format(self.fitbit_token), 'accept': 'application/json'})

		response =fit_bit_heartrate_today.json()
		#print(response)
		dataset =response['activities-heart-intraday']['dataset']
		#print("Todays heartrate dataset: ",dataset)




		for i in range(len(dataset)):
			time_value_heart  = response['activities-heart-intraday']['dataset'][i]['time']

			heart_rate  = response['activities-heart-intraday']['dataset'][i]['value']

			if time_value_heart == time_value_corresponding_song:
				#Add heatrate to spreadsheet
				wks.update("R{}".format(next_available_heart_cell), heart_rate)




	
	def refresh_fitbit(self):
		refreshCaller = Refresher()
		self.fitbit_token = refreshCaller.fitbit_refresh()
		self.fill_heartrate()
		

