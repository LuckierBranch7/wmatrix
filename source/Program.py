import random
import time
import os
import sys
import argparse
import curses
from collections import deque

def parse_args():
    parser = argparse.ArgumentParser(description='WMatrix - A Matrix-like screen for Windows')
    parser.add_argument('-c', '--color', type=str, default='green', 
                        choices=['green', 'red', 'blue', 'white', 'yellow', 'cyan', 'magenta'],
                        help='Set the color of the matrix (default: green)')
    parser.add_argument('-s', '--speed', type=float, default=0.05,
                        help='Set the speed of the matrix (default: 0.05, lower is faster)')
    parser.add_argument('-d', '--density', type=int, default=5,  # Increased default density
                        choices=range(1, 11),
                        help='Set the density of the matrix (1-10, default: 5)')
    parser.add_argument('-l', '--max-length', type=int, default=15,
                        help='Maximum length of matrix trails (default: 15)')
    parser.add_argument('-m', '--max-trails', type=int, default=None,
                        help='Maximum number of active trails (default: calculated based on terminal width)')
    parser.add_argument('-g', '--gap', type=int, default=2,
                        help='Minimum gap between trails (default: 2)')
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

class MatrixDrop:
    def __init__(self, x, height, max_length):
        self.x = x  # column position
        self.y = 0  # current position
        self.speed = random.randint(1, 3)  # Randomize speed for visual variety
        self.active = True
        self.max_length = max_length
        self.screen_height = height
        self.tail = deque(maxlen=max_length)  # Use deque with max length for efficient tail management
        self.head_char = chr(random.randint(33, 126))
    
    def update(self):
        # Add current position to tail with a random character
        if len(self.tail) >= self.max_length:
            self.tail.popleft()  # Remove oldest position if we exceed max length
        self.tail.append((self.y, chr(random.randint(33, 126))))
        
        # Move drop down based on its speed
        self.y += self.speed
        
        # Check if drop is off screen
        if self.y > self.screen_height + self.max_length:
            self.active = False
    
    def draw(self, stdscr, head_color, tail_color):
        # Draw the head (white)
        if 0 <= self.y < self.screen_height:
            safe_addstr(stdscr, self.y, self.x, self.head_char, head_color)
        
        # Draw the tail (color)
        for i, (pos_y, char) in enumerate(reversed(self.tail)):
            if 0 <= pos_y < self.screen_height:
                brightness = curses.A_BOLD if i < 3 else curses.A_NORMAL
                safe_addstr(stdscr, pos_y, self.x, char, tail_color | brightness)
    
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
    
    # Calculate max trails if not specified
    if args.max_trails is None:
        max_trails = max(width // 2, 1)  # Increased from 25% to 50% of screen width
    else:
        max_trails = args.max_trails
    
    # Initialize matrix drops
    active_drops = []
    
    # Track columns with active drops
    active_columns = set()
    
    # Track frame timing for consistent animation speed
    last_frame_time = time.time()
    frame_count = 0
    last_report_time = last_frame_time
    
    # Fill the screen initially with some drops for immediate visual effect
    for _ in range(min(width // 3, max_trails // 2)):
        x = random.randint(0, width - 1)
        if x not in active_columns:
            active_columns.add(x)
            # Start some drops partway down the screen for initial variety
            drop = MatrixDrop(x, height, args.max_length)
            if random.random() < 0.5:  # 50% chance to start partway down
                drop.y = random.randint(0, height // 2)
                # Pre-fill the tail for mid-screen drops
                for _ in range(min(drop.y, drop.max_length)):
                    drop.tail.append((drop.y - len(drop.tail) - 1, 
                                     chr(random.randint(33, 126))))
            active_drops.append(drop)
    
    # Main loop
    while True:
        try:
            current_time = time.time()
            elapsed = current_time - last_frame_time
            
            # Limit to target framerate (based on speed setting)
            if elapsed < args.speed:
                time.sleep(args.speed - elapsed)
                current_time = time.time()
            
            # Performance monitoring (every 5 seconds)
            if current_time - last_report_time > 5:
                fps = frame_count / (current_time - last_report_time)
                frame_count = 0
                last_report_time = current_time
            
            # Update frame timing
            last_frame_time = current_time
            frame_count += 1
            
            # Check if terminal was resized
            new_height, new_width = stdscr.getmaxyx()
            if new_height != height or new_width != width:
                height, width = new_height, new_width
                # Recalculate max trails if auto
                if args.max_trails is None:
                    max_trails = max(width // 2, 1)
                
                # Update active columns tracking
                active_columns = set(drop.x for drop in active_drops if drop.x < width)
                
                # Filter out drops that are now off-screen
                active_drops = [drop for drop in active_drops if drop.x < width]
                
                # Clear screen on resize
                stdscr.clear()
            
            # Clear the screen more efficiently
            stdscr.erase()
            
            # Remove inactive drops and update active columns
            new_active_drops = []
            active_columns.clear()
            for drop in active_drops:
                if drop.active:
                    new_active_drops.append(drop)
                    active_columns.add(drop.x)
            active_drops = new_active_drops
            
            # Randomly add new drops if we're under the maximum
            # Higher chance based on density parameter
            drop_chance = 0.15 * args.density
            
            # Try to add multiple drops per frame based on density
            for _ in range(min(3, args.density)):
                if len(active_drops) < max_trails and random.random() < drop_chance:
                    # Try to find an available column
                    available_columns = []
                    for x in range(width):
                        # Check for minimum gap between columns
                        is_available = True
                        for occupied_x in active_columns:
                            if abs(x - occupied_x) < args.gap:
                                is_available = False
                                break
                        if is_available:
                            available_columns.append(x)
                    
                    # If we found available columns, pick one randomly
                    if available_columns:
                        x = random.choice(available_columns)
                        active_columns.add(x)
                        active_drops.append(MatrixDrop(x, height, args.max_length))
            
            # Update and draw all active drops
            for drop in active_drops:
                drop.update()
                drop.draw(stdscr, curses.color_pair(2) | curses.A_BOLD, curses.color_pair(1))
            
            # Refresh the screen
            stdscr.refresh()
            
            # Check for keyboard input
            stdscr.nodelay(True)
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('+') or key == ord('='):  # Increase density
                args.density = min(10, args.density + 1)
            elif key == ord('-'):  # Decrease density
                args.density = max(1, args.density - 1)
            elif key == ord('p'):  # Add pause functionality
                stdscr.nodelay(False)
                stdscr.getch()  # Wait for any key
                stdscr.nodelay(True)
                last_frame_time = time.time()  # Reset frame timing
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