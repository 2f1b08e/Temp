#!/usr/bin/env python3

import shutil
import time
import sys
import os

# A beautiful and responsive Python script to print "nya~" in a heart shape.
# This script is designed to be more portable than its bash counterpart.
#
# Coded with <3
#
# Usage:
#   1. Save this file as nya_heart.py
#   2. Run it from your terminal: python3 nya_heart.py
#   3. Resize your terminal to see the magic!
#   4. Press Ctrl+C to exit gracefully.

def draw_heart():
    """
    Gets terminal dimensions and prints a heart to fit.
    This function contains the core logic for drawing the shape.
    """
    # Get the current terminal dimensions.
    # shutil.get_terminal_size() is the modern, reliable way to do this.
    cols, lines = shutil.get_terminal_size(fallback=(80, 24))

    # The text to fill the heart with.
    text = "nya~"
    text_len = len(text)
    text_char_idx = 0

    # ANSI escape codes for a nice pink color and to reset formatting.
    # This uses 256-color mode, which is supported by most modern terminals.
    pink_color = "\033[38;5;205m"
    reset_color = "\033[0m"

    # We will build the entire screen's content in this list of strings
    # and then print it all at once to prevent flickering.
    output_buffer = []

    # Iterate over every character cell in the terminal (y is row, x is column).
    for y in range(lines):
        line = ""
        for x in range(cols):
            # This is the magic part: the heart equation.
            # First, we normalize the (x, y) terminal coordinates to a mathematical
            # grid where the heart equation works well.
            # Character cells are taller than they are wide, so we scale y differently
            # to make the heart look proportional. Smaller divisors make the heart bigger.
            # A small vertical offset (-0.2) is added to center the heart better.
            nx = (x - cols / 2) / (cols / 3.5)
            ny = (y - lines / 2) / (lines / 7) - 0.2

            # The heart equation itself: (x^2 + y^2 - 1)^3 - x^2*y^3 <= 0
            # If the result for a given (nx, ny) point is less than or equal to zero,
            # it is inside the heart.
            val = (nx**2 + ny**2 - 1)**3 - (nx**2 * ny**3)

            if val <= 0:
                # We are inside the heart! Get the next character from "nya~".
                char = text[text_char_idx % text_len]
                line += f"{pink_color}{char}{reset_color}"
                text_char_idx += 1
            else:
                # We are outside the heart, so just add a space.
                line += " "
        
        output_buffer.append(line)

    # Move cursor to the top-left corner without clearing, to reduce flicker.
    sys.stdout.write("\033[H")
    # Join all the lines and print in a single operation.
    sys.stdout.write("\n".join(output_buffer))
    sys.stdout.flush()


def main():
    """
    The main loop that handles drawing, resizing, and graceful exit.
    """
    # Hide the cursor for a cleaner look when the script starts.
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    try:
        while True:
            # Continuously draw the heart. The draw_heart function always
            # gets the latest terminal size, making the script responsive.
            draw_heart()
            # A short sleep prevents the script from using 100% CPU.
            # This determines the "refresh rate" on resize.
            time.sleep(0.05)
    except KeyboardInterrupt:
        # User pressed Ctrl+C. Time to clean up!
        print("\nNyaa~ bye bye!")
    finally:
        # This block ensures cleanup happens even if an error occurs.
        # Restore the cursor to its normal state.
        sys.stdout.write("\033[?25h")
        # Reset any lingering text colors or attributes.
        sys.stdout.write("\033[0m")
        # It's good practice to clear the screen on exit.
        # Use 'cls' on Windows and 'clear' on other systems.
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.flush()


if __name__ == "__main__":
    main()
