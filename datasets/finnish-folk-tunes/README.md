Background
----------

Please look here for [details about the collection](http://esavelmat.jyu.fi/collection.html). Citing from that page:

> "By the end of the 19th century, the Finnish Literary Society (SKS) had collected tens of thousands of folk tunes from all over the Finland (see maps for more details). Most of the fieldwork was done prior to the advent of recording technology and therefore the material consists mainly of transcriptions. The impetus for collecting tunes from all around the nation came from the rising nationalism that already had produced the Finnish national epic, Kalevala (1835) and Kanteletar (1840). By the end of the century, a Finnish music scholar, Ilmari Krohn, had started to edit and publish the collected folk songs in separate volumes, all falling under the name Finnish Folk Tunes (Suomen Kansan Sävelmiä). The volumes included about 9000 folk tunes and they were published between the years 1898-1933. This collection is musically comprehensive, nationally important and thoroughly documented."

Downloading
-----------

The collection can be downloaded from http://esavelmat.jyu.fi/collection_download.html.
Two files are provided:

- `finfolktunes_data_corrected.txt` a tab-separated file with some metadata
- `finfolktunes.mat` a MatLab matrix file containing a note matrix. This is the MIDI representation used by the MIDI Toolbox. 

Note matrices
-----------

A note matrix has as many rows as there are events (notes) and 7 columns containing the properties that define the event 
(see [MIDIToolbox manual](https://github.com/miditoolbox/1.1/blob/master/documentation/MIDItoolbox1.1_manual.pdf), page 10), namely:

1. Note onset (in beats)
2. Note duration (in beats)
3. MIDI channel
4. MIDI pitch
5. Velocity
6. Onset (seconds)
7. Duration (seconds)

Just for later reference, you can easily load this in Python using scipy:

```python
import scipy.io

def load_note_matrices(filename):
    """Load the Finnish Folk Tunes notematrix file.
    Returns an array with note matrices of all songs"""
    # If you read out a mat file, you get back a dictionary
    # The note matrix has key `nm`
    fft = scipy.io.loadmat(filename)
    assert fft['nm'].shape[0] == 1
    notematrices = fft['nm'][0]
    return notematrices

songs = load_note_matrices('finfolktunes.mat')
song0 = songs[0]
# Song 0 has 40 notes/events
assert song0.shape == (40, 7)
```


Catafolk notes
--------------

- We assume the filenames contain the numbers of the songs
in their respective publications.
- Note that the data file contains two `key` columns. We rename the first when importing.