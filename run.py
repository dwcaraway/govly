# Run a test server.
from app import app

if __name__ == '__main__':
	# This does nothing unless you run this module with --liveandletdie flag.
	import liveandletdie
	liveandletdie.Flask.wrap(app)
	app.run()
