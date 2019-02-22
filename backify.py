import os
import csv
import json
import argparse
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

class Backify:
	def __init__(self, token):
		self.sp = spotipy.Spotify(auth=token)
		print('Authenticated!')
		print(json.dumps(self.sp.current_user(), sort_keys=True, indent=4))

	def importing(self, f):
			with open(f, 'r') as csvfile:
					reader = csv.reader(csvfile)
					for row in reader:
							print('Importing {} by {}'.format(row[0], row[1]))
							self.sp.current_user_saved_tracks_add(tracks=[row[2]])
	def exporting(self, f):
			with open(f, 'w') as f:
				writer = csv.writer(f)
				saved_songs = self.sp.current_user_saved_tracks()
				songs = saved_songs['items']
				while saved_songs['next']:
						saved_songs = self.sp.next(saved_songs)
						songs.extend(saved_songs['items'])
				for song in songs:
						print('Exporting {} by {}'.format(song['track']['name'], song['track']['artists'][0]['name']))
						writer.writerow(str(song['track']['name'] + '\t' + song['track']['artists'][0]['name'] + '\t' + song['track']['uri']).split('\t'))

def main():
	parser = argparse.ArgumentParser(description='Import/Export your Spotify playlists. By default, opens a browser window to authorize the Spotify Web API')
	group = parser.add_mutually_exclusive_group(required=True)
	parser.add_argument('-userid', help='userID for the spotify account', required=True)
	group.add_argument('-importing', help='Import saved songs from file')
	group.add_argument('-exporting', help='Import saved songs from file')
	args = parser.parse_args()
	#username = 'iwc2bkgvcprn4w0h6srwdm36s'
	try:
		token = spotipy.util.prompt_for_user_token(args.userid, 'user-library-modify playlist-read-private')
	except (AttributeError, JSONDecodeError):
		os.remove('.cache-{}'.format(args.userid))
		token = spotipy.util.prompt_for_user_token(args.userid, 'user-library-modify playlist-read-private')
	backify = Backify(token)
	if args.importing:
		backify.importing(args.importing)
	elif args.exporting:
		backify.exporting(args.exporting)
		
if __name__ == '__main__':
	main()

