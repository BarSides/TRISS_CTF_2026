#!/usr/bin/env python3
"""Builds model.json from a small synthetic mail corpus. Deterministic (fixed seed).

Run `python3 train.py` after editing the corpus, then rebuild the image.
"""
import json
import random
from pathlib import Path

from filter import train

random.seed(1870)

SPAM_OPENERS = [
    "URGENT action required", "Congratulations you are a winner", "Final notice",
    "Your account has been suspended", "Act now before it is too late", "Dear valued customer",
    "Limited time offer", "Security alert", "You have been selected", "Immediate response needed",
]
SPAM_BODIES = [
    "click the link below to verify your account and password",
    "buy gift cards and send the codes to me right away",
    "claim your free prize and cash reward today",
    "wire the payment immediately to avoid penalties",
    "your bitcoin wallet needs verification now",
    "confirm your bank login to unlock your funds",
    "I need you to purchase gift cards for a client, scratch off the codes and email them",
    "you won a free vacation, just pay the processing fee",
    "update your billing information or your account will be closed",
    "this is the CEO, I am in a meeting, buy gift cards urgently and text me the codes",
    "exclusive deal, cheap pills, no prescription needed",
    "your package is on hold, pay the customs fee with a gift card",
    "send your social security number to claim the refund",
    "earn money fast working from home, guaranteed income",
    "your password expires today, reset it using this secure link",
]
SPAM_CLOSERS = [
    "Do not tell anyone.", "Reply immediately.", "Act fast!", "Offer expires tonight!!!",
    "Keep this confidential.", "Click here now.", "Kind regards, The Security Team",
    "Sent from my iPhone", "100% guaranteed!", "Respond within 24 hours or lose access.",
]

HAM_OPENERS = [
    "Hi team", "Morning all", "Hey Dave", "Quick update", "Reminder for everyone",
    "Hi folks", "Thanks for yesterday", "Heads up", "Hello operators", "Notes from the meeting",
]
HAM_BODIES = [
    "the cable inspection on car two is scheduled for Tuesday morning before opening",
    "please log the brake test results in the maintenance binder at the upper station",
    "we need one more operator to cover the Saturday evening shift",
    "the lower station on Carson Street will open late because of the parade",
    "attached is the weekly rider count, ridership was up after the fireworks",
    "the hoist motor bearings were greased and the wheels were checked",
    "Port Authority wants our timetable updated for the winter schedule",
    "lunch is on me Friday, there are pierogies in the break room",
    "the Grandview Avenue overlook railing was repainted this week",
    "remember to sweep the platform and wipe down the car windows at close",
    "the track crew will replace two ties on the lower incline next month",
    "training for new operators is Thursday at the upper station office",
    "the fare box at the bottom was jammed again, I called the technician",
    "Mount Washington neighbors asked about the noise from the evening runs",
    "the safety audit went well and the inspector signed off on the report",
    "please swap the light bulbs in the upper station stairwell",
    "the Steelers game Sunday means heavy traffic, plan for extra riders",
    "minutes from the staff meeting are on the shared drive",
]
HAM_CLOSERS = [
    "Thanks!", "See you on shift.", "Cheers, Marge", "Let me know if questions.",
    "Have a good weekend.", "Talk soon.", "Thanks, Station Supervisor", "Appreciate it.",
    "Go Pens.", "Take care, Bob from maintenance",
]


def corpus(openers, bodies, closers, n, extra):
    docs = []
    for _ in range(n):
        body = ". ".join(random.sample(bodies, extra))
        docs.append(f"{random.choice(openers)}, {body}. {random.choice(closers)}")
    return docs


if __name__ == "__main__":
    spam = corpus(SPAM_OPENERS, SPAM_BODIES, SPAM_CLOSERS, 120, 2)
    ham = corpus(HAM_OPENERS, HAM_BODIES, HAM_CLOSERS, 120, 2)
    model = train(spam, ham)
    out = Path(__file__).with_name("model.json")
    out.write_text(json.dumps(model, indent=0, sort_keys=True))
    print(f"wrote {out.name}: {len(model['weights'])} words")
