# Name

Nesting Dolls

## Author

@justinforbes

## Overview

A postcard from Pittsburgh turned up in the BarSides mailbox, signed by our old friend The Bridge Keeper. The front is a nice view of the Point, but the card is suspiciously heavy for a picture this simple. There's more to this postcard than its front.

## Setup

Attach `files/postcard.jpg` as a CTFd download. No hosted service is needed. Players can solve it entirely in the local CyberChef (**Extract EXIF**, then **Unzip** with the password), or with `exiftool`/`file` plus `unzip`/7-Zip.

`build/make_postcard.py` regenerates the file (Pillow, the DejaVu fonts and the `zip` command required). It is for organizers only; do not attach it. ZipCrypto salts each build, so rebuilt files differ byte for byte but solve the same way.

## Flag

BarSides{postcards_have_two_sides}
