import random
import time
import os
import sys
import argparse
import curses

def parse_args():
    parser = argparse.ArgumentParser(description='WMatrix - A Matrix-like screen for Windows')
    parser.add_argument('-c', '--color', type=str, default='green', 
                        choices=['green', 'red', 'blue', 'white', 'yellow', 'cyan', 'magenta'],
                        help='Set the color of the matrix (default: green)')
    parser.add_argument('-s', '--speed', type=float, default=0.05,
                        help='Set the speed of the matrix (default: 0.05, lower is faster)')
    parser.add_argument('-d', '--density', type=int, default=2,
                        choices=range(1, 11),
                        help='Set the density of the matrix (1-10, default: 2)')
    return parser.parse_args()

def get_color(color_name):
    colors = {
        'green': curses.COLOR_GREEN,
        'red': curses.COLOR_RED,
        'blue': curses.COLOR_BLUE,
        'white': curses.COLOR_WHITE,
        'yellow': curses.COLOR_YELLOW,
        'cyan': curses.COLOR_CYAN,
        'magenta': curses.COLOR_MAGENTA
    }
    return colors.get(color_name, curses.COLOR_GREEN)

def safe_addstr(stdscr, y, x, string, attr=curses.A_NORMAL):
    """Safely add a string to the screen, avoiding buffer overflow errors"""
    height, width = stdscr.getmaxyx()
    # Check if the position is within bounds
    if 0 <= y < height and 0 <= x < width:
        try:
            stdscr.addstr(y, x, string, attr)
        except curses.error:
            # Still can fail if we're at the bottom-right corner
            pass
    
def main(stdscr, args):
    # Setup
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.use_default_colors()
    color = get_color(args.color)
    curses.init_pair(1, color, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    
    # Initialize screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Initialize rain drops
    drops = [0] * width
    chars = [' '] * width
    
    # Main loop
    while True:
        try:
            # Check if terminal was resized
            new_height, new_width = stdscr.getmaxyx()
            if new_height != height or new_width != width:
                height, width = new_height, new_width
                # Adjust drops array if width changed
                if len(drops) < width:
                    drops.extend([0] * (width - len(drops)))
                    chars.extend([' '] * (width - len(chars)))
                elif len(drops) > width:
                    drops = drops[:width]
                    chars = chars[:width]
                
                # Clear screen on resize
                stdscr.clear()
            
            stdscr.erase()
            
            for i in range(min(width, len(drops))):
                # Random chance to start a new drop
                if drops[i] == 0 and random.random() < 0.02 * args.density:
                    drops[i] = 1
                    chars[i] = chr(random.randint(33, 126))  # ASCII printable characters
                
                # Draw current position of drop
                if drops[i] > 0:
                    # Head of the drop (white)
                    if drops[i] <= height:
                        safe_addstr(stdscr, drops[i]-1, i, chars[i], 
                                    curses.color_pair(2) | curses.A_BOLD)
                    
                    # Tail of the drop (color)
                    for j in range(1, min(drops[i], height)):
                        if drops[i] - j < height:
                            char = chr(random.randint(33, 126))
                            brightness = curses.A_NORMAL if j > 5 else curses.A_BOLD
                            safe_addstr(stdscr, drops[i]-j-1, i, char, 
                                        curses.color_pair(1) | brightness)
                    
                    # Move drop down
                    drops[i] += 1
                    
                    # If drop is off screen, reset it
                    if drops[i] > height + 10:
                        drops[i] = 0
            
            stdscr.refresh()
            time.sleep(args.speed)
            
            # Check for keyboard input
            stdscr.nodelay(True)
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_RESIZE:
                # Let the resize be handled in the next iteration
                continue
                
        except Exception as e:
            # Handle any unexpected errors
            curses.endwin()
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    args = parse_args()
    try:
        curses.wrapper(main, args)
    except KeyboardInterrupt:
        print("WMatrix terminated.")