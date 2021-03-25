# pylint: disable=invalid-name
#from googlevinylemulator import app
import time
import json

import spotify_token as st  # pylint: disable=import-error
import spotipy  # pylint: disable=import-error

import pychromecast
from pychromecast.controllers.spotify import SpotifyController

class CastPlayer:

    def __init__(self, cast_item_name = "Basement Desk Speaker") -> None:
        self.cast_item_name = cast_item_name
        self.cast_item = None
        #self.mc = self.cast_item.media_controller 
        self.mc = None
        self.client = None
        self.spotify_device_id = None
        self.shuffle = False
        self.sp = None
        self.spotify_device_id = None
        #Look at spotify_example to see how to set up the spotify controller.

    #Look at Spotipy to see what controls I have.
    #Need to use spotipy to get the client.

    def get_cast_item(self):
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[self.cast_item_name])
        if len(chromecasts) > 0:
            self.cast_item = chromecasts[0]
            # Wait for connection to the chromecast
            self.cast_item.wait()
            print("Chromecast '" + self.cast_item_name  +"' found.")
        else:
            print(self.cast_item)
            print("Chromecast could not be found. Please try again later.")
        return

    def connect_spotify(self):
        """Connects everything needed in order to get spotify to work.
        """
        # Launch the spotify app on the cast we want to cast to
        #Depends on spotipy.spotipy client for access token and expires
        
        #create a spotify token
        data = st.start_session(self.read_sp_dc(), self.read_sp_key())
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
        # for device in devices_available["devices"]:
        #     if device["id"] == self.sp.device:
        #         self.spotify_device_id = device["id"]
        #         print("Spotify found the device.")
        #         break

        #Currently brute forcing it due to google home's not appearing on spotify devices. Still seem to work for now.
        self.spotify_device_id = self.sp.device
        print (self.sp.device)

        #Error if device could not be found.
        if not self.spotify_device_id:
            print('No device with id "{}" known by Spotify'.format(self.sp.device))
            print("Known devices: {}".format(devices_available["devices"]))

        return
    #def connect_cast_and_spotify(self):


    def play(self):
        """Will start the music if it is paused.
        """
        
        _status = "OK"
        _statusMessage = ""
        self.client.start_playback(self.spotify_device_id)
        _statusMessage = "Playback has started."
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

    #Not seeing a way to mute.
    #def mute(self):
    #    mc = self.cast_item.media_controller

    #This looks exactly the same as getting the cast item. Not sure if anything else needs to happen.
    def change_speaker(self, cast_item_name):
        """Will move to the next song in a playlist or album. Not complete yet.
        """
        #TODO: Do this.
        _status = "OK"
        _statusMessage = ""
        self.cast_item = self.getCastItem(cast_item_name)
        
        #TODO: Handle this using some of the code in Connect_spotify.

        self.client.transfer_playback(self.new_device_id)
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

        return

    def next(self):
        """Will move to the next song in a playlist or album.
        """
        _status = "OK"
        _statusMessage = ""
        self.client.next_track(self.spotify_device_id)
        _statusMessage = "Moving to the next track."
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 
        return

    def previous(self):
        """Will move to a previous song in a playlist or album.
        """
        _status = "OK"
        _statusMessage = ""
        self.client.previous_track(self.spotify_device_id)
        _statusMessage = "Moving to the previous track."
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 
        return

    def pause(self):
        """Will pause the playback in Spotify if a song is playing.
        """
        #Could look at client.currentlyPlaying to see if that could be used.
        _status = "OK"
        _statusMessage = ""
        self.client.pause_playback(self.spotify_device_id)
        _statusMessage = "Playback has paused."
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

    def volume(self, volume_percent):
        """Will set volume on Spotify to the amount in 'volume_percent'. Not complete yet
        """
        #TODO: Do this. Need to get volume amount from the website.
        _status = "OK"
        _statusMessage = ""
        self.client.volume(volume_percent, self.spotify_device_id)
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

    def shuffle(self):
        """Will set shuffle on and off, based on the current state. Then passes
        that setting over to Spotify.
        """
        _status = "OK"
        _statusMessage = ""
        if self.shuffle == True:
            self.shuffle = False
            _statusMessage = "Shuffle has been turned off."
        else:
            self.shuffle = True
            _statusMessage = "Shuffle has been turned on."
        #set shuffle to what it currently is in Spotipy.
        self.client.shuffle(self.shuffle, self.spotify_device_id)
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

    def repeat(self, repeat_state):
        """ Set repeat mode for playback.

            Parameters:
                - state - `track`, `context`, or `off`
                - device_id - device target for playback
        """
        #TODO: Do this. Need to get volume type from the website.
        _status = "OK"
        _statusMessage = ""
        self.client.repeat(repeat_state, self.spotify_device_id)
        _statusMessage = "Repeat has been set to  " + repeat_state
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results) 

    def play_item(self, song_url):
        """ Plays the item (song, album, playlist, etc.) that has been passed
        to this method as 'song_url'. It will also create all the spotify clients and
        chromecast clients if needed.
        """
        _status = "OK"
        _statusMessage = ""
        print("Song is " + song_url)
        if self.cast_item is None:
            _statusMessage = "Looking for " + self.cast_item_name + ".\n"
            self.get_cast_item()
        if self.cast_item is not None: #If the cast worked, then put music on.
            if self.client is None or self.spotify_device_id is None:
                _statusMessage = _statusMessage + "Connecting to Spotify.\n"
                self.connect_spotify()
            if self.spotify_device_id is not None:
                print ("Spotify Device = " + self.spotify_device_id)
                if ":track:" in song_url:
                    #Song is a track, play it through the track process
                    string_array = [song_url]
                    print ("Playing Track = " + song_url)
                    self.client.start_playback(device_id=str(self.spotify_device_id), uris=string_array)
                else:    
                    print ("Playing Album or Playlist = " + song_url)
                    self.client.start_playback(device_id=str(self.spotify_device_id), context_uri=song_url)
                _statusMessage = _statusMessage + "Playback of " + song_url + " on " + self.cast_item_name + " will be starting shortly.\n"
            else:
                _statusMessage = _statusMessage + "Could not find the spotify device, cannot play music."
        else:
            _statusMessage = _statusMessage + "Could not find the chromecast, cannot play music."
            print (_statusMessage)
        results = {
            "Status":_status,
            "StatusMessage":_statusMessage
        }
        print (_statusMessage)
        return json.dumps(results)

    def read_sp_dc(self):
        """ Reads the username from the 'sp_dc.txt' file to be used later.
        """
        with open("sp_dc.txt", "r") as f:
            username = f.read()
            print (username)
            return username

    def read_sp_key(self):
        """ Reads the password from the 'sp_key.txt' file to be used later.
        """
        with open("sp_key.txt", "r") as f:
            password = f.read()
            print (password)
            return password