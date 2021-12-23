from PIL import Image, ImageEnhance
import pyrebase
import glob
import os
import math
from math import ceil, floor


#--------------------------GENERATE & SAVE ART#--------------------------


class generate_and_send():

    def __init__(self) -> None:
        pass


    def generate_art(self):

        images = glob.glob("images_test/*.jpg")

        frame_width = 1920
        images_per_row =15
        padding = 0

        #This should return 640
        img_width, img_height = Image.open(images[0]).size
        sf = (frame_width-(images_per_row-1)*padding)/(images_per_row*img_width)
        scaled_img_width = ceil(img_width*sf)
        scaled_img_height = ceil(img_height*sf)

        number_of_rows = ceil(len(images)/images_per_row)
        frame_height = ceil(sf*img_height*number_of_rows) 


        new_im = Image.new('RGB', (frame_width, frame_height), color = (231, 226, 215))

        i,j=0,0
        for num, im in enumerate(images):
            if num%images_per_row==0:
                i=0
            im = Image.open(im)
            #Here I resize my opened image, so it is no bigger than im_width, im_height
            im.thumbnail((scaled_img_width,scaled_img_height))
            #Iterate through a 4 by 4 grid with (im_width) spacing, to place my image
            y_cord = (j//images_per_row)*scaled_img_height
            new_im.paste(im, (i,y_cord))
            print(i, y_cord)
            i=(i+scaled_img_width)+padding
            j+=1
            
            new_im.save("weekly_art.jpg")

        self.send_art()

        
    def send_art(self):
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

        storage.child("weekly_art.jpg").put("weekly_art.jpg")







