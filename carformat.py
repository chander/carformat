#!/usr/bin/env python
'''
Simple(ish) python script to convert and organized music files to the
MP3 format.

'''
'''
The MIT License (MIT)

Copyright (c) 2015 Chander Ganesan <chander@otg-nc.com> 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''



import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TALB
from mutagen.mp4 import MP4
from subprocess import Popen, PIPE
import os
import sys

def shellquote(s):
    return s.replace('/','_')

class id3Tag:
    def __init__(self,f):
        self.file=MP3(f)
        try:
            self.title=self.file['TIT2'].text[0].strip()
        except:
            self.title=None
        try:
            self.artist=self.file['TPE1'].text[0].strip()
        except:
            self.artist=None
        try:
            self.album=self.file['TALB'].text[0].strip()
        except:
            self.album=None
class mp4Tag:
    def __init__(self,f):
        self.file=MP4(f)
        try:
            self.title=self.file['\xa9nam'][0].strip()
        except:
            self.title=None
        try:
            self.artist=self.file['\xa9ART'][0].strip()
        except:
            self.artist=None
        try:
            self.album=self.file['\xa9alb'][0].strip()
        except:
            self.album=None
        
def convertToMp3(f):
   #print "Converting %s to mp3" % (f)
   m4tags=mp4Tag(f)
   #print "Converting %s - %s (%s) to mp3" % (m4tags.title, m4tags.artist, m4tags.album)
   cmd1=['faad','-o','-',f]
   f2="%s.mp3" % (f.rsplit('.',1)[0],)
   cmd2=['lame','-', f2]
   p1=Popen(cmd1, stdout=PIPE)
   p2=Popen(cmd2, stdin=p1.stdout)
   p2.wait()
   try:
     mp3File=MP3(f2)
     mp3File['TIT2']=TIT2(encoding=3, text=[m4tags.title])
     mp3File['TPE1']=TPE1(encoding=3, text=[m4tags.artist])
     mp3File['TALB']=TALB(encoding=3, text=[m4tags.album])
     mp3File.save()
     print "%s converted to %s" % (f,f2)
   except:
     print >>sys.stderr, "Convert of %s failed." % f2
   os.unlink(f)
   

for cdir, subdirs, files in os.walk('.'):
  for f in files:
    if f.lower().endswith('m4a'):
      convertToMp3(f)
for cdir, subdirs, files in os.walk('.'):
  for f in files:
    if f.lower().endswith('mp3'):
      tag = id3Tag(f)
      album=tag.album or ''
      artist=tag.artist or ''
      title=tag.title or ''
      if album:
         album=shellquote(album)
         if not os.path.isdir(album):
            os.mkdir(album)
         if title and artist:
            fname="%s - %s.mp3" % (title, artist,)
         elif len(title):
            fname="%s.mp3" % (title,)
         else:
            fname=f
         fname=shellquote(fname)
         album=shellquote(album)
         fname=os.path.join(album,fname)
      elif artist:
         if not os.path.isdir(artist):
            os.mkdir(artist)
         if title and artist:
            fname="%s - %s.mp3" % (artist, title,)
         elif title:
            fname="%s.mp3" % (titlem)
         else:
            fname=f
         fname=shellquote(fname)
         artist=shellquote(artist)
         fname=os.path.join(artist,fname)
      try:
         os.rename(os.path.join(cdir, f), os.path.join(cdir,fname))
      except Exception, e:
         print "Error for rename: %s to %s (%s)" % (os.path.join(cdir, f), os.path.join(cdir,fname), e)
      else:
         pass
  break # Only do the first directory

