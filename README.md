SoundBooth
==========

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/uucastine/soundbooth?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build
Status](https://travis-ci.org/uucastine/soundbooth.svg?branch=master)](https://travis-ci.org/uucastine/soundbooth)

SoundBooth is a simple Django project with a mission to make it easy to record
line-in audio on a computer running by itself in the back of a building.

The use case it was designed for was a church where the line-in is patched
from the audio rack, and the server is up 24/7 and configured to auto-record
at a set time once a week (3 guesses what day, and your first two don't count).

Once setup, you can configure where the audio is saved to. By default we
give it some S3 credentials and it tosses a lossless audio file into a bucket
with a timestamp for a file name.

From there, someone goes in and does postprocessing manually before the file
is ready to be archived on our website.

For task running, we use Celery. Audio is captured using the awesome PyAudio
library, which runs on top of PortAudio. This means you need to have a mic
or line-in on the machine you set this up on, and you also need to run both
a web applicaiton process, and a celery process (or two, depending on whether
you split celery-beat into it's own process).


Easy bootstrapping!
-------------------

Powered by the ubiquitous Makefile ... this should be pretty easy:

1. make install
2. make run
3. open your browser to: http://127.0.0.1:45000

If you've never used Django on your machine before, you may need to:

`make deps`

or 

`make mac_deps`
