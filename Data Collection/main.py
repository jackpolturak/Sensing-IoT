import json
import requests
from secrets import spotify_user_id
from requests.models import Response
from refresh import Refresher
from google_sheets import Add_to_sheets
import time
from datetime import date, datetime 
import urllib.request
from generate_weekly_art import generate_and_send
import pyrebase


class get_current_song:
	def __init__(self):
		self.user_id = spotify_user_id
		self.spotify_token = ""
		self.fitbit_token = ""
		self.minutes_listening =[""]


	def get_current(self):

		print("Finding Currently Song & Audio Features....")
		query_currently_playing = 'https://api.spotify.com/v1/me/player/currently-playing'
		query_audio_features = 'https://api.spotify.com/v1/audio-features/'
		
		
		response_currently_playing = requests.get(query_currently_playing,
									headers={'Content-Type': 'application/json',
									'Authorization': 'Bearer {}'.format(self.spotify_token)})


		
		if response_currently_playing.status_code == 204:
			print("--------------------No Response--------------------")


		elif response_currently_playing.status_code !=204:

			
			print("Response found......")

			response_json_currently_playing = response_currently_playing.json()
			
			is_playing = response_json_currently_playing['is_playing']
			
			if is_playing == True:

				track_id = response_json_currently_playing['item']['id']
				track_name = response_json_currently_playing['item']['name']
				artists = [artist for artist in response_json_currently_playing['item']['artists']]
				is_playing = response_json_currently_playing['is_playing']
				link = response_json_currently_playing['item']['external_urls']['spotify']
				artist_names = ', '.join([artist['name'] for artist in artists])


				response_audio_features = requests.get(query_audio_features + track_id, 
											headers={'Content-Type': 'application/json',
											'Authorization': 'Bearer {}'.format(self.spotify_token)})


				
				response_json_audio_features = response_audio_features.json()

				danceability = response_json_audio_features['danceability']
				energy = response_json_audio_features['energy']
				key = response_json_audio_features['key']
				loudness = response_json_audio_features['loudness']
				mode = response_json_audio_features['mode']
				speechiness = response_json_audio_features['speechiness']
				acousticness = response_json_audio_features['acousticness']
				instrumentalness = response_json_audio_features['instrumentalness']
				liveness = response_json_audio_features['liveness']
				valence = response_json_audio_features['valence']
				tempo = response_json_audio_features['tempo']



				#STORE TIME
				today = date.today()
				today_date = today.strftime("%Y-%m-%d")

				now = datetime.now()
				time = now.strftime("%H:%M:00")

				print(time)

				data_row = [today_date, time, track_name, artist_names, track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo]
				

				#SAVE ARTWORK INTO FOLDER:
				search = 'https://api.spotify.com/v1/tracks/{}'.format(track_id)
				response_search = requests.get(search,
											headers={'Content-Type': 'application/json',
											'Authorization': 'Bearer {}'.format(self.spotify_token)})


				response_search_json = response_search.json()
				#640x640 image url, change the list value 0 to get other sizes
				image_url = response_search_json['album']['images'][0]['url']

				urllib.request.urlretrieve(image_url, "images_test/{}.jpg".format(track_id))
				urllib.request.urlretrieve(image_url, "most_recent.jpg".format(track_id))
				self.upload_recent_art()

				print(data_row)

				upload_caller = Add_to_sheets
				upload_caller.next_available_row(data_row)

			if is_playing == False:
				print("Song detected but paused")


	def upload_recent_art(self):

		#--------------------------SEND TO FIREBASE--------------------------
		config = {
			"apiKey": "AIzaSyCWO48_gM16IgYULLWMdjFz0-QNEALx0TY",
			"authDomain": "portfolio-eadae.firebaseapp.com",
			"databaseURL": "https://portfolio-eadae.firebaseio.com",
			"projectId": "portfolio-eadae",
			"storageBucket": "portfolio-eadae.appspot.com",
			"messagingSenderId": "191242670825",
			"appId": "1:191242670825:web:c9fed1f21b47f8d665d678",
			"measurementId": "G-13Y0YS4MKE",
			"serviceAccount": "serviceAccountKey.json"
		}

		firebase_storage = pyrebase.initialize_app(config)
		storage = firebase_storage.storage()
		print("Sending to firebase.....")
		storage.child("most_recent.jpg").put("most_recent.jpg")






	
	def call_refresh(self):
		print("Refreshing Tokens...")
		refreshCaller = Refresher()
		self.spotify_token = refreshCaller.spotify_refresh()

		self.fitbit_token = refreshCaller.fitbit_refresh()
		self.get_current()






sampling_minutes = 0
while True:
	sampling_minutes +=1

	# 1 >>>> REFRESH SPOTIFY TOKEN, SAMPLE AUDIO FEATURES, UPLOAD DATA TO SHEETS + SAVE TRACK ART
	a = get_current_song()
	a.call_refresh()
	
	# 2 >>>>REFRESH FITBIT TOKEN,SAMPLE HEARTRATE, UPLOAD TO SHEETS
	b = Add_to_sheets()
	b.refresh_fitbit()
	time.sleep(60)

	# 3>>>>> IF A WEEK HAS PASSED (10080 mins in a week)
	#GENERATE ALBUM COVER ARTWORK FROM 
	if sampling_minutes % 10080 == 0:
		c = generate_and_send()
		c.generate_art()








