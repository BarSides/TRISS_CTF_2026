# Link Preview: walkthrough

PghChat fetches a URL on its server and shows the result. That means the fetch runs from the server's point of view, so it can reach things the player cannot, such as a service bound to the server's own loopback address. This is server side request forgery (SSRF).

1. A normal link works: `http://news.example.com/` shows a preview.
2. The footer and the admin hint point at an internal admin console. Try the obvious internal addresses:
   - `http://localhost/` -> "Previews of localhost are blocked for security reasons."
   - `http://127.0.0.1/` -> blocked the same way.
3. The blocklist is an exact text match on two strings. The same loopback address can be written many other ways, none of which are on the list:
   - `http://127.1/`
   - `http://2130706433/` (127.0.0.1 as a single decimal number)
   - `http://[::1]/` (IPv6 loopback)
   - `http://127.0.0.1./` (trailing dot)
   - `http://0.0.0.0/`
   - `http://0177.0.0.1/` (127.0.0.1 in octal)

   Any of these reaches the admin console:

   ```
   PghChat Admin Console
   Deploy key: BarSides{server_side_requests_cross_the_bridge}
   ```

Lesson: blocking SSRF by matching hostnames is a losing game, because one address has countless spellings. Safe designs resolve the address first and block by the resolved IP range (loopback, link-local, private), or only allow an explicit set of hosts.

Flag: `BarSides{server_side_requests_cross_the_bridge}`
