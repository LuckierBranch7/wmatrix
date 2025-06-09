# WMatrix

A Windows version of the classic Linux CMatrix program that displays the "Matrix" digital rain effect in your terminal.

## Installation

1. You may need to run terminal as admin to install
2. Make sure you have Python installed on your Windows system
3. Run the install script:
   ```
   python install.py
   ```
4. The script will:
   - Install WMatrix to your local AppData folder
   - Add it to your PATH environment variable
   - Install any required dependencies
5. You may need to restart your terminal or system for PATH changes to take effect

## Usage

```
wmatrix [options]
```

### Options:

- `-c, --color COLOR`: Set the color (green, red, blue, white, yellow, cyan, magenta)
- `-s, --speed SPEED`: Set the speed (lower is faster, default: 0.05)
- `-d, --density DENSITY`: Set the density (1-10, default: 5)
- `-l, --max-length LENGTH`: Maximum length of matrix trails (default: 15)
- `-m, --max-trails TRAILS`: Maximum number of active trails (default: 50% of terminal width)
- `-g, --gap GAP`: Minimum gap between trails (default: 2)

### Interactive Controls:

While running, you can use these keyboard controls:
- `q`: Quit the program
- `p`: Pause/resume the animation
- `+` or `=`: Increase density
- `-`: Decrease density

### Examples:

```
wmatrix
wmatrix --color red --speed 0.03
wmatrix --density 10 --max-length 20
wmatrix --gap 1 --max-trails 100
```

## Visual Customization

Adjust the parameters to get different visual effects:

- For a dense, fast Matrix look: `wmatrix --density 10 --gap 1 --speed 0.03`
- For a sparse, slow effect: `wmatrix --density 2 --speed 0.1`
- For longer trails: `wmatrix --max-length 30`
- For shorter trails: `wmatrix --max-length 8`

## Performance Tips

If you experience lag:
1. Reduce the density (`--density 3`)
2. Reduce the maximum number of trails (`--max-trails 30`)
3. Reduce the maximum trail length (`--max-length 10`)
4. Increase the minimum gap (`--gap 3`)
5. Slow down the animation (`--speed 0.1`)

## Requirements

- Python 3.6+
- windows-curses package (installed automatically)

## Troubleshooting

- If you see an error related to `addwstr()`, try running in a different terminal or resizing your window
- If the animation is slow or laggy, try reducing the density or maximum trail length
- If colors don't display correctly, ensure your terminal supports ANSI colors