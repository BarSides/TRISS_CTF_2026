# Name

Scatter Shot

## Author

@justinforbes

## Overview

We finally caught a break on The Bridge Keeper. A voicemail they left us is just a little chime tune, but their seized laptop had a script called `scatter.py` sitting next to it. Looks like they hid something in the audio and locked it with a PIN. They never told us the PIN.

## Setup

Attach `files/voicemail.wav` and `files/scatter.py` as CTFd downloads. No hosted service is needed. Players need Python 3 (standard library only; no Pillow or other packages).

`build/make_voicemail.py` regenerates the WAV using the same `files/scatter.py`, and `build/solve.py` is the reference solver (brute-forces the PIN in well under a second). Both are for organizers only; do not attach them.

## Flag

BarSides{four_digits_is_not_a_key}
