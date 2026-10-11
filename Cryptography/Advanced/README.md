# Name

The Bridge Keeper's Last Note

## Author

@justinforbes

## Overview

The Bridge Keeper's final note has arrived, and they've stopped disguising single letters. Our analysts believe letters are now locked together two at a time and mixed with a small key matrix before being written down. Frequency analysis is useless, and so is brute-forcing a shift. Luckily the Bridge Keeper still signs off every claim code the same way...

## Setup

Attach `files/bridge_keeper_3.txt` as a CTFd download. No hosted service is needed. CyberChef has no Hill cipher operation, so players need a short Python script (any Python 3.8+, no extra packages) or pen-and-paper modular arithmetic.

Final part of the Bridge Keeper series after "Steel City Shift" (Beginner) and "Bridge Keeper's Revenge" (Intermediate). It isn't set as a CTFd requirement, so players can attempt it in any order.

How the cipher is applied: only letters are encrypted. They're read in order and taken in pairs, ignoring spaces and punctuation. Case and non-letters keep their positions, and the flag begins on a pair boundary.

## Flag

BarSides{two_by_two_matrix_mod_twenty_six}
