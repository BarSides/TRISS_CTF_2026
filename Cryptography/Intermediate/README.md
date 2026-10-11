# Name

Bridge Keeper's Revenge

## Author

@justinforbes

## Overview

The Bridge Keeper is back, and this time they say a simple shift won't save you. Our analysts think every letter was multiplied by a secret number and then shifted by another before being written down. Brute-forcing the shift won't work this time, but you already know how the flag starts...

## Setup

Attach `files/bridge_keeper_2.txt` as a CTFd download. No hosted service is needed. Players can solve it with the local CyberChef (Affine Cipher Decode) after recovering the key from the known `BarSides` prefix, or with a few lines of Python.

Sequel to Cryptography Beginner "Steel City Shift". It isn't set as a CTFd requirement so players can attempt it in any order.

## Flag

BarSides{multiply_then_shift}
