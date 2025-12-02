import argparse
import os

# Default ANSI color codes
ANSI_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m"
}

def highlight_repeats(chunk, min_repeat=2):
    """
    Detect multi-byte repeating patterns within the chunk.
    Returns a list of colors for each byte position.
    """
    colors = [None] * len(chunk)
    i = 0
    while i < len(chunk) - 1:
        repeat_len = 1
        # Look ahead for repeating bytes
        while i + repeat_len < len(chunk) and chunk[i] == chunk[i + repeat_len]:
            repeat_len += 1
        if repeat_len >= min_repeat:
            for j in range(repeat_len):
                colors[i + j] = "pattern"
            i += repeat_len
        else:
            i += 1
    return colors

def hex_view(file_path, bytes_per_line=16, start=0, length=None,
             search=None, search_str=None, color_scheme=None):
    """CLI hex viewer with customizable color scheme."""
    if color_scheme is None:
        # default colors
        color_scheme = {
            "nonprint": "red",
            "repeat": "yellow",
            "null": "cyan",
            "pattern": "magenta",
            "search": "green"
        }

    try:
        with open(file_path, "rb") as f:
            f.seek(start)
            line_number = start // bytes_per_line
            bytes_read = 0
            prev_chunk = None

            # Convert search hex string to bytes if needed
            if search:
                search_bytes = bytes.fromhex(search)
            elif search_str:
                search_bytes = search_str.encode('latin-1')
            else:
                search_bytes = None

            while True:
                if length is not None:
                    to_read = min(bytes_per_line, length - bytes_read)
                    if to_read <= 0:
                        break
                    chunk = f.read(to_read)
                else:
                    chunk = f.read(bytes_per_line)

                if not chunk:
                    break

                # Detect multi-byte repeats
                repeat_colors = highlight_repeats(chunk)

                # Hex representation
                hex_parts = []
                for i, b in enumerate(chunk):
                    hex_str = f"{b:02X}"

                    # Determine color
                    color = None
                    if b == 0x00:
                        color = ANSI_COLORS[color_scheme["null"]]
                    elif prev_chunk and i < len(prev_chunk) and b == prev_chunk[i]:
                        color = ANSI_COLORS[color_scheme["repeat"]]
                    elif repeat_colors[i] == "pattern":
                        color = ANSI_COLORS[color_scheme["pattern"]]

                    if color:
                        hex_str = f"{color}{hex_str}{ANSI_COLORS['reset']}"

                    hex_parts.append(hex_str)
                hex_line = ' '.join(hex_parts)

                # ASCII representation
                ascii_parts = []
                for i, b in enumerate(chunk):
                    if 32 <= b <= 126:
                        char = chr(b)
                    else:
                        char = f"{ANSI_COLORS[color_scheme['nonprint']]}.{ANSI_COLORS['reset']}"

                    # Search highlight
                    if search_bytes:
                        for j in range(len(search_bytes)):
                            if i + j < len(chunk) and chunk[i:i+len(search_bytes)] == search_bytes:
                                char = f"{ANSI_COLORS[color_scheme['search']]}{char}{ANSI_COLORS['reset']}"

                    # Multi-byte repeat
                    if repeat_colors[i] == "pattern":
                        char = f"{ANSI_COLORS[color_scheme['pattern']]}{char}{ANSI_COLORS['reset']}"

                    ascii_parts.append(char)
                ascii_line = ''.join(ascii_parts)

                # Print line offset, hex, and ASCII
                print(f"{line_number*bytes_per_line:08X}  {hex_line:<{bytes_per_line*3}}  {ascii_line}")

                prev_chunk = chunk
                line_number += 1
                bytes_read += len(chunk)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")

def parse_color_scheme(scheme_str):
    """
    Parse color scheme from a string like:
    null=cyan,repeat=yellow,pattern=magenta,nonprint=red,search=green
    Returns a dictionary.
    """
    scheme = {}
    for pair in scheme_str.split(','):
        if '=' in pair:
            key, val = pair.split('=', 1)
            key = key.strip().lower()
            val = val.strip().lower()
            if key in ["null", "repeat", "pattern", "nonprint", "search"] and val in ANSI_COLORS:
                scheme[key] = val
    return scheme

def main():
    parser = argparse.ArgumentParser(description="Enhanced CLI Hex Viewer with customizable colors")
    parser.add_argument("-f", "--file", required=True, help="Path to the file to display")
    parser.add_argument("-b", "--bytes-per-line", type=int, default=16, help="Number of bytes per line")
    parser.add_argument("--start", type=int, default=0, help="Start byte offset")
    parser.add_argument("--length", type=int, help="Number of bytes to display")
    parser.add_argument("--search", help="Hex byte pattern to highlight, e.g., 'DEADBEEF'")
    parser.add_argument("--search-str", help="ASCII string to highlight")
    parser.add_argument("--color-scheme", help="Comma-separated colors: null=cyan,repeat=yellow,pattern=magenta,nonprint=red,search=green")

    args = parser.parse_args()
    file_path = args.file

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    color_scheme = parse_color_scheme(args.color_scheme) if args.color_scheme else None

    hex_view(
        file_path,
        bytes_per_line=args.bytes_per_line,
        start=args.start,
        length=args.length,
        search=args.search,
        search_str=args.search_str,
        color_scheme=color_scheme
    )

if __name__ == "__main__":
    main()
