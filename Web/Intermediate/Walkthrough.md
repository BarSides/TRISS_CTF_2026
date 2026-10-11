# 446 Bridges: walkthrough

1. Searching `Clemente` returns one bridge. Searching a single quote `'` returns a database error:

   ```
   Database error: unrecognized token: "' ORDER BY name"
   ```

   The search text is pasted into the SQL query, so this is SQL injection. The query is something like `SELECT ... FROM bridges WHERE name LIKE '%<search>%' ORDER BY name`.

2. Searching `' OR 1=1--` lists every bridge, which confirms we control the query. `--` comments out the rest of it.

3. The results table has three columns, so a `UNION SELECT` must return three columns. Every SQLite database lists its tables in `sqlite_master`:

   ```
   ' UNION SELECT name, sql, type FROM sqlite_master--
   ```

   Among the bridges are two extra rows: `bridges` and `maintenance_crew_notes`, with the `CREATE TABLE` statements showing the columns `id` and `note`.

4. Read the notes:

   ```
   ' UNION SELECT id, note, 1 FROM maintenance_crew_notes--
   ```

   Note 3 reads: `Gate code for the Liberty Bridge maintenance catwalk: BarSides{union_select_the_city_of_bridges}`

Lesson: never build SQL by pasting user input into a string. Parameterized queries (`WHERE name LIKE ?`) keep data from being read as SQL. Showing raw database errors to users also helps attackers.

Flag: `BarSides{union_select_the_city_of_bridges}`
