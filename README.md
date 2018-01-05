# Machiavel

(WIP)

Machiavel generates music collages/sample mixes (plunderphonic song sketches) by analyzing a directory of audio files (mp3, wav, aif) and randomly select a song to build a mix around. It will then pick out other appropriate songs from that directory - tempo-stretching and pitch-shifting them as needed - to slice into samples, which it then assembles into a multi-track mix.

The quality of the output depends a lot on your own taste in curating the library Machiavel samples from. If you have a directory of songs that seem like they'll fit together, Machiavel will do pretty well. If you have a bunch of random tracks, you might get something nice too.

These mix sketches are meant for high-scale automated ideation and not a substitute for human editing ;)

## Setup

Machiavel uses some audio libraries to do the heavy-lifting.

- `brew install sox ffmpeg`
- Install [Essentia](http://essentia.upf.edu/documentation/installing.html)

Install pip requirements.

`$ pip install requirements.txt`

## Usage

You can have Machiavel analyze your library in one go, so that mix generation runs quicker. Machiavel will persist song analyses based on file hashes so no redundant processing is necessary.

- Store input songs in `.flac` format in the directory `input/`

- Run `$ python main.py` to generate mixes

- Output mixes are generated in `output/`

## Notes

- The quality of Machiavel's output depends a lot on what songs are in the library ("crate") you specify.

- Machiavel will try to avoid overlaying a song with itself, but sometimes it is unavoidable. 

- Songs with less clear beats are much harder to calculate tempos for, but they can lead to interesting results nonetheless

- Machiavel doesn't recognize vocals, so if you have a lot of vocal-heavy songs in your library, you may get kind of cacophonous results - but sometimes it works out well too

- You can pre-cut some samples, dump them into a folder, and point Machiavel to that to generate a mix from as well

## To do

- Add arguments as parameters

- Package code

- Add some EQing heuristics and probably use the Spotify API to maybe match songs better