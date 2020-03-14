---
layout: dataset
dataset_id: densmore-teton-sioux
analyzed: true
title: Densmore's Teton Sioux Music
dataset_url: https://github.com/craigsapp/densmore-teton-sioux
urls:
    - https://github.com/craigsapp/densmore-teton-sioux
    - http://kern.ccarh.org/cgi-bin/ksbrowse?s=sioux
authors: 
    - name: Francis Densmore
      role: author
    - name: Craig Stuart Sapp
      url: https://github.com/craigsapp
      role: digitization    
tags: [symbolic]
formats: [kern]
files: 245
notes: 
duration: 
copyright: Copyright 2002 Craig Stuart Sapp
licence_abbr: CC BY-NC-SA 4.0
license_url: https://creativecommons.org/licenses/by-nc-sa/4.0
version: none
description: >
    A digital edition of 245 songs from the book Teton Sioux Music by Frances Densmore, originally published by the Bureau of American Ethnology, Bulletin 61, Smithsonian Institution (1918). The digital edition was prepared by Craig Stuart Sapp in 2002.
---


Corrections
================================

If you think that there is a mistake in the data, verify that there is a problem by viewing
the original edition at https://books.google.com/books?id=Adw_AAAAYAAJ to compare
with the digital edition.

If an error is found, there are two methods for fixing it.  A simple method is to report the problem
on the [issues](https://github.com/craigsapp/densmore-teton-sioux/issues) page for this repository.  You
should cite the song number and page in the source PDF (and/or the page number in the original publication) 
with a description of the error.  Also cite the measure number in the source edition (visible at the start of the systems
in VHV, as well as after `=` signs in the data).  Also preferably you should include a snapshot of the 
error in the VHV notation and in the source scan of the corresponding spot.  

Images can be added to the issue report by dragging-and-dropping them into the report form.


More advanced users can submit a [pull request](https://help.github.com/articles/about-pull-requests)
fixing the error, after first making a [fork](https://help.github.com/articles/fork-a-repo/) (i.e., a copy) into 
their Github account.

In both case, you will have to create a [free account](https://github.com/join) on Github.

Line/page breaks and staff spacings are dependent on verovio and not
taken from the source edition (may be added in the future).

Downloading
==================

The files can be downloaded by clicking on the green "Clone or download" 
button that should be near the top right corner of this page.  Then
choose "Download ZIP" in the drop-down menu that appears.

To download with `git`:

```bash
git clone https://github.com/craigsapp/densmore-teton-sioux
```

To update your copy with any new changes to the data, type this command
within the densmore-teton-sioux directory:

```bash
git pull
```

Alternate access to data
========================

This digital edition is also accessible in a variety of interfaces
described below.


KernScores website access
-------------------------

These digital scores are available on the kernScores library of Humdrum musical scores:
*    http://kernscores.stanford.edu/browse?l=folk/sioux

with mirrors at:
*    http://kern.humdrum.org/browse?l=folk/sioux
*    http://kern.ccarh.org/browse?l=folk/sioux


Command-line downloading with Humdrum Extras
--------------------------------------------

The [Humdrum Extras](http://extras.humdrum.org) command-line programs 
can download these files from kernScores.  A quick method of downloading:
```bash
    mkdir -p densmore-teton-sioux
    cd densmore-teton-sioux
    humsplit h://folk/sioux
```

To interface to the original Humdrum Toolkit commands, use the humcat command to download to standard input (the -s option is needed when downloading multiple files):
```bash
   humcat -s h://folk/sioux | census -k
```

There are 16091 notes in this data set, which is an average of 66 notes per song.  The lowest pitch is
D2 and the hightest is F5.  The shortest note, other than a few grace notes, is a triplet 32nd note, and the
longest note is a dotted half note.
