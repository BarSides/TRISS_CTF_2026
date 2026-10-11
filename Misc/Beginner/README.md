# Name

Box Score

## Author

@justinforbes

## Overview

The Pittsburgh Pierogies' media office sent this spreadsheet to every reporter in the press box. The front office swears it only held the roster and season stats.

A sports writer thinks there was more in it than that. Take a look.

## Setup

Attach `files/box_score.xlsx` as a CTFd download. No hosted service is needed.

The workbook has three visible sheets and a fourth, `Trade Deadline`, that is hidden. The flag sits in that sheet in white text on a white background. Players solve it in Excel (right click a sheet tab > Unhide) or LibreOffice Calc (Sheet > Show Sheet). Google Sheets needs the Internet, so it is not an option at the venue. Without a spreadsheet app, an `.xlsx` is a ZIP: unzipping it and reading the sheet XML under `xl/worksheets/` also shows the flag.

The file is compressed, so `strings` on the `.xlsx` itself does not show the flag.

`build/make_box_score.py` regenerates the workbook (needs `openpyxl`). It is for organizers only; do not attach it.

## Flag

BarSides{hidden_sheets_still_get_emailed}
