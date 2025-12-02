# Enhanced CLI Hex Viewer

A Python-based command-line hex viewer with advanced features, including:

- Customizable color highlighting for different byte types.
- Detection and highlighting of repeated byte patterns.
- Highlighting of specific hex byte sequences or ASCII strings.
- Adjustable bytes per line, start offset, and display length.

---

## Features

- **Hex and ASCII display:** Shows both hex values and corresponding ASCII characters.
- **Color highlighting:** Default ANSI colors for:
  - Non-printable bytes
  - Null bytes (`0x00`)
  - Repeated bytes
  - Multi-byte repeating patterns
  - Search results
- **Custom color schemes:** Override default colors via command-line argument.
- **Pattern detection:** Highlights repeated bytes and multi-byte sequences automatically.
- **Search support:** Highlight specific byte sequences (hex) or ASCII strings.

---

## Requirements

- Python 3.x
- ANSI-compatible terminal (most modern terminals support ANSI colors)

No additional dependencies are required.

---

## Arguments

-f, --file
Path to the file to display. Required.

-b, --bytes-per-line
Number of bytes to display per line. Default: 16.

--start
Starting byte offset. Default: 0.

--length
Number of bytes to display. If omitted, displays until the end of the file.

--search
Hex byte pattern to highlight. Example: DEADBEEF.

--search-str
ASCII string to highlight. Example: "password".

--color-scheme
Custom colors in the format:
null=cyan,repeat=yellow,pattern=magenta,nonprint=red,search=green

---

## Usage

![Screenshot of the help interface](/assets/images/cli.png)

Run the script from the command line:

```bash
python hex_viewer.py -f <file> [options]
```

Default Colors:
```
python hexviewer.py -f example.bin
```

Custom color scheme:
```
python hexviewer.py -f example.bin --color-scheme "null=blue,repeat=green,pattern=yellow,nonprint=red,search=magenta"
```

With search and region limit:
```
python hexviewer.py -f example.bin --start 512 --length 256 --search DEADBEEF
```


![Screenshot of output](/assets/images/output.png)
