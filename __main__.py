#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import
from future import standard_library
standard_library.install_aliases()

import os
import sys
import difflib

VIDEO_FORMAT = ('avi', 'flv', 'mkv', 'm4p', 'm4v', 'mp4', 'mpeg', 'mpg', 'webm', 'wmv', 'vtt')
SUBTITLE_FORMAT = ('ass', 'srt', 'ssa', 'sub')

def get_files(_format, files):
    return sorted([f for f in files if f.split('.')[-1].lower() in _format])

def match_name(movies, subtitles):
    for subtitle in subtitles:
        sub_name = os.path.splitext(subtitle)[0]
        movie_names = [os.path.splitext(m)[0] for m in movies]
        match = difflib.get_close_matches(sub_name, movie_names, n=1, cutoff=0.3)
        if match:
            movie = next(m for m in movies if m.startswith(match[0]))
            new_name = f"{os.path.splitext(movie)[0]}.{subtitle.split('.')[-1]}"
            if not os.path.exists(new_name):
                os.rename(subtitle, new_name)
                print(f"✅ Renamed: {subtitle} → {new_name}")
            else:
                print(f"⚠️ File already exists: {new_name}, skipping.")
        else:
            print(f"❌ No match found for: {subtitle}")

def main():
    target_dir = str(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
    os.chdir(target_dir)
    files = os.listdir(target_dir)
    if files:
        movies = get_files(VIDEO_FORMAT, files)
        subtitles = get_files(SUBTITLE_FORMAT, files)
        match_name(movies, subtitles)
        print("\n>>> Done! <<<")
    else:
        print("There's nothing here. I'm leaving...")

if __name__ == '__main__':
    main()
