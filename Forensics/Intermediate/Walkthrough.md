# Forgot to Clear History walkthrough

1. Unzip `dkowalski_firefox_profile.zip`. The interesting files are `places.sqlite` (history, bookmarks, downloads) and `formhistory.sqlite` (text typed into web forms and the search bar).
2. List the history in time order. Firefox stores times as microseconds since 1970 (UTC):

   ```sql
   SELECT datetime(v.visit_date/1000000, 'unixepoch') AS utc, p.url
   FROM moz_historyvisits v JOIN moz_places p ON p.id = v.place_id
   ORDER BY v.visit_date;
   ```

3. On Monday Dana opens the confidential Gen4 bid pricing page and downloads `Gen4_Bid_Pricing_FINAL.xlsx` (see `moz_annos`), then reads an offer letter from Three Rivers Traffic Systems.
4. Tuesday morning: searches for "how to send a file without work email", "paste site that deletes after reading" and "hide text from dlp scanner", then CyberChef, then a burn-after-reading paste site, then "how to clear firefox history" (which Dana never actually did).
5. The CyberChef URLs hold the recipe. The last one is `XOR` with the UTF8 key `yinz`, then `To Base64`.
6. The paste itself is gone, but Firefox remembered the form:

   ```sql
   SELECT fieldname, value FROM moz_formhistory ORDER BY firstUsed;
   ```

   `paste_body` is `OwgcKRANCwkCHQYfJhsLGRAZCyUOCB0lEAcxDhEMMQ8LBRM=`.
7. Reverse the recipe in CyberChef: **From Base64**, then **XOR** with key `yinz` (UTF8). XOR is its own inverse.

Alternative for step 7: From Base64 then **XOR Brute Force** with crib `BarSides{` and key length 4 also finds the key.

Flag: `BarSides{the_recipe_was_in_the_url}`
