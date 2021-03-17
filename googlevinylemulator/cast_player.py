# pylint: disable=invalid-name
#from googlevinylemulator import app
import time

import spotify_token as st  # pylint: disable=import-error
import spotipy  # pylint: disable=import-error

import pychromecast
from pychromecast.controllers.spotify import SpotifyController

class CastPlayer:

    def __init__(self, cast_item_name = "Basement Desk Speaker") -> None:
        self.cast_item_name = cast_item_name
        self.cast_item = self.get_cast_item(cast_item_name)
        self.mc = self.cast_item.media_controller 
        self.client = None
        self.spotify_device_id = None
        self.shuffle = False
        self.sp = None
        self.spotify_device_id = None
        #Look at spotify_example to see how to set up the spotify controller.

    #Look at Spotipy to see what controls I have.
    #Need to use spotipy to get the client.

    def get_cast_item(self, cast_item_name):
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[cast_item_name])
        cast_item = chromecasts[0]
        # Wait for connection to the chromecast
        cast_item.wait()
        return cast_item

    def connect_spotify(self):
        """Connects everything needed in order to get spotify to work.
        """
        # Launch the spotify app on the cast we want to cast to
        #Depends on spotipy.spotipy client for access token and expires
        
        #create a spotify token
        data = st.start_session(self.read_username(), self.read_password())
        access_token = data[0]
        expires = data[1] - int(time.time())

        # Create a spotify client
        self.client = spotipy.Spotify(auth=access_token)

        # Launch the spotify app on the cast we want to cast to
        self.sp = SpotifyController(access_token, expires)
        self.cast_item.register_handler(self.sp)
        self.sp.launch_app()

        if not self.sp.is_launched and not self.sp.credential_error:
            #Try to start up another play, wait 2-3 seconds, then get control again.
            self.cast_item.media_controller.play_media(self.help_url, "audio/mp3")
            #wait a second
            self.cast_item.wait()
            self.cast_item.register_handler(self.sp)
            self.sp.launch_app()
            #print("Failed to launch spotify controller due to timeout")
            #sys.exit(1)
        if not self.sp.is_launched and self.sp.credential_error:
            print("Failed to launch spotify controller due to credential error")

        devices_available = self.client.devices()

        # Match active spotify devices with the spotify controller's device id
        for device in devices_available["devices"]:
            if device["id"] == self.sp.device:
                self.spotify_device_id = device["id"]
                print("Spotify found the device.")
                break

        #Error if device could not be found.
        if not self.spotify_device_id:
            print('No device with id "{}" known by Spotify'.format(self.sp.device))
            print("Known devices: {}".format(devices_available["devices"]))

        return
    #def connect_cast_and_spotify(self):


    def play_pause(self):
        """Will pause the music if it is playing, will start the music if it is paused.
        """
        if self.mc.status.player_state == "PLAYING":
            #self.mc.pause()
            self.client.pause_playback(self.spotify_device_id)
        if self.mc.status.player_state == "PAUSED":
            #self.mc.play()
            self.client.start_playback(self.spotify_device_id)
        return

    #Not seeing a way to mute.
    #def mute(self):
    #    mc = self.cast_item.media_controller

    #This looks exactly the same as getting the cast item. Not sure if anything else needs to happen.
    def change_speaker(self, cast_item_name):
        """Will move to the next song in a playlist or album.
        """
        self.cast_item = self.getCastItem(cast_item_name)
        
        #TODO: Handle this using some of the code in Connect_spotify.

        self.client.transfer_playback(new_device_id)
        return

    def next(self):
        """Will move to the next song in a playlist or album.
        """
        self.client.next_track(self.spotify_device_id)
        return

    def previous(self):
        """Will move to a previous song in a playlist or album.
        """
        self.client.previous_track(self.spotify_device_id)
        return

    def stop(self):
        """Will pause the playback in Spotify if a song is playing..
        """
        if self.mc.status.player_state == "PLAYING":
            self.client.pause_playback(self.spotify_device_id)
        return

    def volume(self, volume_percent):
        """Will set volume on Spotify to the amount in 'volume_percent'.
        """
        self.client.volume(volume_percent, self.spotify_device_id)
        return

    def shuffle(self):
        """Will set shuffle on and off, based on the current state. Then passes
        that setting over to Spotify.
        """
        if self.shuffle == True:
            self.shuffle = False
        else:
            self.shuffle = True
        #set shuffle to what it currently is in Spotipy.
        self.client.shuffle(self.shuffle, self.spotify_device_id)
        return

    def repeat(self, repeat_state):
        """ Set repeat mode for playback.

            Parameters:
                - state - `track`, `context`, or `off`
                - device_id - device target for playback
        """
        self.client.repeat(repeat_state, self.spotify_device_id)        

    def play_item(self, song_url):
        """ Plays the item (song, album, playlist, etc.) that has been passed
        to this method as 'song_url'. It will also create all the spotify clients and
        chromecast clients if needed.
        """
        if not self.cast_item:
            self.cast_item = self.get_cast_item(self.cast_item_name)
        if not self.client or not self.spotify_device_id:
            self.connect_spotify()
        self.client.start_playback(device_id=self.spotify_device_id, uris=song_url)

    def read_username(self):
        """ Reads the username from the 'username.txt' file to be used later.
        """
        with open("username.txt", "r") as f:
            username = f.read()
            print (username)
            return username

    def read_password(self):
        """ Reads the password from the 'password.txt' file to be used later.
        """
        with open("password.txt", "r") as f:
            password = f.read()
            print (password)
            return password