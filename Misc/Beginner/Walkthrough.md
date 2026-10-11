# Box Score walkthrough

1. Open `box_score.xlsx` in Excel or LibreOffice Calc. The visible sheets are `Notes`, `Roster` and `2026 Stats`. Nothing in them looks secret.
2. Look for hidden sheets. Excel: right click any sheet tab > Unhide, pick `Trade Deadline`. LibreOffice: Sheet > Show Sheet.
3. The `Trade Deadline` sheet holds front office notes. Row 7 says the code word was made white so nobody could read it over a shoulder, and row 8 looks empty.
4. Click cell A8 (the formula bar shows its contents), or select the sheet and change the font colour to black.

No spreadsheet app:

```sh
unzip -o box_score.xlsx -d box_score
grep -o 'BarSides{[^}]*}' box_score/xl/sharedStrings.xml
```

CyberChef works too: Unzip, then open `xl/sharedStrings.xml`.

Flag: `BarSides{hidden_sheets_still_get_emailed}`
