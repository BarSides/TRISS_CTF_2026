# Staff Only: walkthrough

1. The site footer says the backstage page isn't linked and "not even search engine robots are allowed in". That points at `robots.txt`, the file sites use to tell crawlers what to skip.
2. Visit `http://EVENT_HOST:8004/robots.txt`:

   ```
   User-agent: *
   Disallow: /backstage/
   ```

3. Visit `/backstage/`. It says "STAFF ONLY. Our records say you are not staff." and sets a cookie `staff=false`.
4. Open developer tools (F12). In Firefox go to Storage > Cookies, in Chrome or Edge go to Application > Cookies. Double click the value of `staff`, change it to `true`, and reload the page.

   Or with curl: `curl -b staff=true http://EVENT_HOST:8004/backstage/`

5. The backstage page welcomes you and shows the pass code.

Lessons: `robots.txt` is a public list of the places a site wants to hide, so it is a map for attackers, not a lock. And anything stored in the browser, such as a cookie, is under the user's control; the server must never trust it to decide who someone is.

Flag: `BarSides{robots_txt_is_a_map_not_a_lock}`
