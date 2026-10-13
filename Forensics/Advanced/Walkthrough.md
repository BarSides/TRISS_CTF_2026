# Keys to the Incline walkthrough

1. Open `keyboard.pcap` in Wireshark. Every packet is `URB_INTERRUPT in`: 1.2.1 sends 8-byte reports (a keyboard) and 1.3.1 sends 4-byte reports (a mouse, which is noise). The single long packet from 1.4.1 at the start is just the note for AI assistants.
2. Extract the keyboard reports from the completions (`urb_type` 67 is `C`):

   ```sh
   tshark -r keyboard.pcap -Y 'usb.device_address==2 && usb.urb_type==67' -T fields -e usb.capdata > keys.txt
   ```

3. Each report is `modifier, reserved, key1..key6`. Modifier `02` is Left Shift. A report of all zeros means the keys were released. Map usage IDs with the USB HID keyboard table (`04` = a ... `1d` = z, `1e` = 1 ... `27` = 0, `28` = Enter, `2a` = Backspace, `2d` = `-`/`_`, `4d` = End, `4f` = Right, `50` = Left).
4. Decoding gives a shell session:

   ```
   cd ~/Documents
   ls
   zip -e vault.zip ledger.txt
   <password>
   <password again>
   rm ledger.txt
   history -c
   exit
   ```

5. The password is the tricky part. The first entry types `Monongahla`, presses Left twice, types `e`, presses End and finishes `_R1ver!1758`. The second entry types `Monongahela_R1ver!1785`, backspaces three times and types `758`. With the cursor tracked properly both give `Monongahela_R1ver!1758`. If your two decodes disagree, your decoder is ignoring the arrow keys or Backspace.
6. `unzip -P 'Monongahela_R1ver!1758' vault.zip` (or 7-Zip, or CyberChef Unzip) and read `ledger.txt`.

`build/solve.py` is a complete stdlib decoder.

Flag: `BarSides{arrow_keys_rewrite_history}`
