# Lost Badge walkthrough

1. Open `http://EVENT_HOST:8012`. The home feed has BarSides' post about the badge left at Stinky's, with a photo.
2. Look at the badge: TRISS 2026, SPEAKER, "Rosie K.", talk "Rust Belt Red Teaming", and `Yinzr: @pierogi_` with a thumb over the end of the handle.
3. Search people for `pierogi`. Five accounts come back: `@pierogi_packets`, `@pierogi_payloads`, `@pierogi_pat`, `@pierogi_pals`, `@pierogi_parade`.
4. Rule out the obvious ones: a pierogi race fan, a food blog and a marching band. Two accounts are TRISS speakers named Rosie.
5. Corroborate with the meetup date (October 15, the night before BarSides' post):
   - `@pierogi_payloads` (Rosie Kaminski, Columbus) posted "Stuck in Columbus all week... missing the BarSides meetup tonight" on October 15, and says their badge is still in their bag.
   - `@pierogi_packets` (Rosie K., Lawrenceville) posted "Dry-running my TRISS talk at the BarSides meetup at Stinky's" at 7:12pm on October 15, and "Woke up with no speaker badge" the next morning. Their slides post also names the talk on the badge, Rust Belt Red Teaming.
6. `@pierogi_packets` pinned a note to self with the claim code: `BarSides{pivot_on_the_handle}`.

Lesson: a partial username is enough to pivot on, but always confirm the match with something independent (here, where the person was that night) before trusting it. And don't post your secrets, even as a note to self.
