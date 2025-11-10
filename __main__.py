#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()

import sys
from os import rename, chdir, listdir, getcwd
from builtins import str

VIDEO_FORMAT = ('avi', 'flv', 'mkv', 'm4p', 'm4v', 'mp4', 'mpeg', 'mpg', 'webm', 'wmv')
SUBTITLE_FORMAT = ('ass', 'srt', 'ssa', 'sub','vtt')

def get_files(_format, files):
    return sorted([f for f in files if f.split('.')[-1] in _format])

def clean_name(name):
    """Normalize filename for fuzzy matching"""
    name = '.'.join(name.split('.')[:-1])  # Remove extension
    name = name.lower().replace('_', ' ').replace('-', ' ')
    # Keep only letters, numbers, and spaces
    name = ''.join(ch for ch in name if ch.isalnum() or ch.isspace())
    return name

def match_name(movies, subtitles):
    """
    Improved matching using fuzzy string comparison.
    Handles differences in file naming like:
    'lecture-1-lets-code-in-python.vtt' → '07 Let's Code.mp4'
    """
    try:
        from rapidfuzz import fuzz, process  # Fast and modern library
    except ImportError:
        from fuzzywuzzy import fuzz, process  # Fallback if rapidfuzz not installed

    # Preprocess video filenames for fuzzy matching
    movie_clean = {m: clean_name(m) for m in movies}

    for subtitle in subtitles:
        sub_clean = clean_name(subtitle)

        # Find best fuzzy match for each subtitle
        result = process.extractOne(
            sub_clean,
            movie_clean.values(),
            scorer=fuzz.token_sort_ratio
        )

        if result is None:
            print(f"⚠️ No match found for {subtitle}")
            continue

        # Handle both (match, score) and (match, score, index)
        if len(result) == 2:
            match, score = result
        else:
            match, score, _ = result

        # Find which original movie filename corresponds to the match
        best_movie = next(k for k, v in movie_clean.items() if v == match)

        # Accept only if confidence > 40%
        if score > 40:
            new_name = "%s.%s" % ('.'.join(best_movie.split('.')[:-1]), subtitle.split('.')[-1])
            try:
                rename(subtitle, new_name)
                print(f"✅ Matched ({score}%): {subtitle} → {new_name}")
            except OSError as e:
                print(f"❌ Could not rename {subtitle}: {e}")
        else:
            print(f"⚠️ No confident match for {subtitle} (best match score {score}%)")


def main():
    chdir(str(sys.argv[1]) if len(sys.argv) > 1 else getcwd())
    files_in_movie_dir = listdir(getcwd())
    if files_in_movie_dir:
        movies = get_files(VIDEO_FORMAT, files_in_movie_dir)
        subtitles = get_files(SUBTITLE_FORMAT, files_in_movie_dir)
        match_name(movies, subtitles)
        print(">>> Done!!! <<<")
    else:
        print("There's nothing here. I'm leaving...")

if __name__ == '__main__':
    main()