from flask import Flask, request, abort, g
from googlevinylemulator.cast_player import CastPlayer

def read_speaker_location():
        """ Reads the speaker location from speaker_loc.txt.
        """
        with open("speaker_loc.txt", "r") as f:
            speaker_location = f.read()
            print (speaker_location)
            return speaker_location

app = Flask(__name__)
app.config["DEBUG"] = True
with app.app_context():
    global cast_player
    cast_player = CastPlayer(read_speaker_location()) #Basement Group or First Floor or Second Floor or Basement Desk Speaker

@app.route("/spotify/now/<spotify_string>", methods=["GET"])
def play_spotify_item(spotify_string=""):
    #TODO: Handle the spotify string here.
    global cast_player
    #string_array = [spotify_string]
    #result = cast_player.play_item(string_array)
    result = cast_player.play_item(spotify_string)
    return result 

@app.route("/", methods=["GET"])
def hello_world(spotify_string=""):
    return "Welcome to the Googlecast API wrapper for the Vinyl Emulator!" 


@app.route("/play", methods=["GET"])
def play():
    global cast_player
    return cast_player.play()

@app.route("/pause", methods=["GET"])
def pause():
    global cast_player
    return cast_player.pause()

@app.route("/previous", methods=["GET"])
def previous():
    global cast_player
    return cast_player.previous()

@app.route("/next", methods=["GET"])
def next():
    global cast_player
    return cast_player.next()

@app.route("/shuffle", methods=["GET"])
def shuffle():
    global cast_player
    return cast_player.shuffle()    

#Need to figure out the following end points:
    #   command:playpause
    #   command:mute
    #   command:next
    #   command:volume/50
    #   command:volume/+10
#      command:shuffle/on
#Can remove the command: from the command



#Use this if running the flask app without a service.
def main():
    app.run(host="localhost", port = 8000, debug=True)

if __name__ == '__main__':
    main()
