from flask import Flask, request, abort, g
from googlevinylemulator.cast_player import CastPlayer

app = Flask(__name__)
app.config["DEBUG"] = True
with app.app_context():
    global cast_player
    cast_player = CastPlayer("Basement Group") #Basement Group or First Floor

@app.route("/spotify/now/<spotify_string>", methods=["GET"])
def play_spotify_item(spotify_string=""):
    #TODO: Handle the spotify string here.
    global cast_player
    string_array = [spotify_string]
    cast_player.play_item(string_array)
    return "You should be playing " + spotify_string + " on " + cast_player.cast_item_name + " soon."

@app.route("/", methods=["GET"])
def hello_world(spotify_string=""):
    return "Welcome to the Googlecast API wrapper for the Vinyl Emulator!" 

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
