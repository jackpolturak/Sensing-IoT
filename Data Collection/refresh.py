from os import replace
from secrets import refresh_token, base_64 
import requests
import json
from requests.structures import CaseInsensitiveDict
import gspread
from oauth2client.service_account import ServiceAccountCredentials



#IMPORT GSPREAD FOR FITBIT TOKEN REFRESH
sa = gspread.service_account(filename="client_secret.json")
sh = sa.open("current_track_info")
wks = sh.worksheet("dataset")

wks_refresh = sh.worksheet("refresh_token")
val = wks_refresh.acell('A1').value



class Refresher:

	def __init__(self):
		self.refresh_token = refresh_token
		self.base_64 = base_64

		
	def spotify_refresh(self):

		query = "https://accounts.spotify.com/api/token"

		response = requests.post(query,
								 data={"grant_type": "refresh_token",
									   "refresh_token": refresh_token},
								 headers={"Authorization": "Basic " + base_64})


		response_json = response.json()
		return response_json['access_token']

	
	def fitbit_refresh(self):

		#GET OLD REFRESH TOKEN FROM GOOGLE SHEETS
		old_refresh = self.read_refresh()


		#EXCHANGE REFRESH TOKEN AND GET NEW ACCESS TOKEN 
		url = "https://api.fitbit.com/oauth2/token"
		headers = CaseInsensitiveDict()
		headers["Authorization"] = "Basic MjNCSFpKOmZmZjlmNzhiN2MxM2I4ZmFkZWUwY2M0NTNlMmNlZDFl"
		headers["Content-Type"] = "application/x-www-form-urlencoded"
		data = "grant_type=refresh_token&refresh_token={}".format(old_refresh)
		resp = requests.post(url, headers=headers, data=data)
		json_response_bytes = resp.content
		json_response_string= json.loads(json_response_bytes)
		fitbit_refresh_token_new = json_response_string['refresh_token']
		#REPLACE GOOGLE SHEETS WITH NEW REFRESH TOKEN 
		self.replace_refesh(fitbit_refresh_token_new)
		return json_response_string['access_token']


	def read_refresh(self): 
		#Read current fitbit refresh token 
		current_refresh = wks_refresh.acell('A1').value
		return current_refresh


	def replace_refesh(self, data):
		#Replace fibit token
		wks_refresh.update('A1', '{}'.format(data))
		return
