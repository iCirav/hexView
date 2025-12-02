usage: hexView.py [-h] -f FILE [-b BYTES_PER_LINE] [--start START] [--length LENGTH] [--search SEARCH]
                  [--search-str SEARCH_STR] [--color-scheme COLOR_SCHEME]

Enhanced CLI Hex Viewer with customizable colors

options:
  -h, --help            show this help message and exit
  -f, --file FILE       Path to the file to display
  -b, --bytes-per-line BYTES_PER_LINE
                        Number of bytes per line
  --start START         Start byte offset
  --length LENGTH       Number of bytes to display
  --search SEARCH       Hex byte pattern to highlight, e.g., 'DEADBEEF'
  --search-str SEARCH_STR
                        ASCII string to highlight
  --color-scheme COLOR_SCHEME
                        Comma-separated colors: null=cyan,repeat=yellow,pattern=magenta,nonprint=red,search=green

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
