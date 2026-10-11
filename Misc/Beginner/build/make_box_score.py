#!/usr/bin/env python3
"""Build files/box_score.xlsx for Misc Beginner "Box Score".

Organizers only; do not attach. Needs openpyxl (pip install openpyxl).
"""
import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

FLAG = "BarSides{hidden_sheets_still_get_emailed}"
OUT = Path(__file__).resolve().parent.parent / "files" / "box_score.xlsx"

HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="27251F")
GOLD_FILL = PatternFill("solid", fgColor="FDB827")

ROSTER = [
    ("#", "Player", "Pos", "B/T", "Hometown"),
    (3, "Dez Halloran", "SS", "R/R", "Bloomfield, PA"),
    (7, "Marco Tolentino", "C", "R/R", "Santo Domingo, DR"),
    (12, "Jake Wyszynski", "1B", "L/L", "Polish Hill, PA"),
    (18, "Reggie Okafor", "CF", "L/R", "Wilkinsburg, PA"),
    (22, "Tommy Brucato", "3B", "R/R", "Bethel Park, PA"),
    (27, "Luis Arceneaux", "RF", "S/R", "Baton Rouge, LA"),
    (31, "Kenji Moriyama", "SP", "R/R", "Sendai, JP"),
    (36, "Pete Szabo", "LF", "L/L", "Munhall, PA"),
    (44, "Andre Pettaway", "RP", "L/L", "McKeesport, PA"),
    (52, "Cal Dombrowski", "2B", "R/R", "Lawrenceville, PA"),
]

STATS = [
    ("Player", "G", "AB", "H", "HR", "RBI", "AVG"),
    ("Dez Halloran", 141, 532, 149, 11, 58),
    ("Marco Tolentino", 118, 401, 102, 17, 66),
    ("Jake Wyszynski", 150, 561, 163, 29, 97),
    ("Reggie Okafor", 155, 604, 175, 8, 49),
    ("Tommy Brucato", 133, 488, 127, 21, 74),
    ("Luis Arceneaux", 147, 553, 149, 24, 81),
    ("Pete Szabo", 101, 344, 88, 6, 31),
    ("Cal Dombrowski", 139, 517, 145, 9, 52),
]


def header(ws, row):
    for cell in ws[row]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL


def main():
    wb = Workbook()

    roster = wb.active
    roster.title = "Roster"
    for row in ROSTER:
        roster.append(row)
    header(roster, 1)
    for col, width in zip("ABCDE", (5, 20, 6, 6, 22)):
        roster.column_dimensions[col].width = width

    stats = wb.create_sheet("2026 Stats")
    stats.append(STATS[0])
    for name, g, ab, h, hr, rbi in STATS[1:]:
        r = stats.max_row + 1
        stats.append((name, g, ab, h, hr, rbi, f"=ROUND(D{r}/C{r},3)"))
        stats.cell(r, 7).number_format = "0.000"
    header(stats, 1)
    stats.column_dimensions["A"].width = 20

    notes = wb.create_sheet("Trade Deadline")
    notes.sheet_state = "hidden"
    notes["A1"] = "FRONT OFFICE ONLY - DO NOT SEND OUTSIDE THE BUILDING"
    notes["A1"].font = Font(bold=True, color="C00000", size=14)
    notes["A3"] = "Wyszynski to Cleveland for two arms. Announce after the deadline."
    notes["A4"] = "Okafor extension: 5 years. Agent has not signed yet."
    notes["A5"] = "Tolentino on waivers if Dombrowski's knee holds up."
    notes["A7"] = "Code word for the deal call is below. Made it white so nobody sees it over my shoulder."
    notes["A8"] = FLAG
    notes["A8"].font = Font(color="FFFFFF")
    notes.column_dimensions["A"].width = 90
    for r in (3, 4, 5, 7):
        notes[f"A{r}"].alignment = Alignment(wrap_text=False)

    readme = wb.create_sheet("Notes", 0)
    readme["A1"] = "Pittsburgh Pierogies Baseball Club - Media Packet"
    readme["A1"].font = Font(bold=True, size=14)
    readme["A1"].fill = GOLD_FILL
    readme["A3"] = "Roster and season stats for the press box. Approved for release."
    readme["A4"] = "Questions: media@pierogies.example"
    readme.column_dimensions["A"].width = 70

    fixed = datetime.datetime(2026, 9, 30, 14, 5, 0)
    wb.properties.creator = "J. Kowalczyk"
    wb.properties.lastModifiedBy = "J. Kowalczyk"
    wb.properties.title = "Media Packet"
    wb.properties.created = fixed
    wb.properties.modified = fixed

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
