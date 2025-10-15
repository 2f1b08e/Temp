#!/bin/bash

# A beautiful script to print "nya~" in a heart shape that fits your terminal.
# It automatically redraws when you resize the window.
#
# Coded with <3
#
# Usage:
#   1. Save this file as nya-heart.sh
#   2. Make it executable: chmod +x nya-heart.sh
#   3. Run it: ./nya-heart.sh
#   4. Resize your terminal to see the magic!
#   5. Press Ctrl+C to exit gracefully.

# --- Dependency Check ---
# The 'tput' command is essential for this script to control the terminal.
# Let's check if it exists before we proceed.
if ! command -v tput &> /dev/null; then
    echo "Error: 'tput' command not found. This script needs it to work." >&2
    echo "Please install the 'ncurses' package for your system." >&2
    echo "e.g., on Debian/Ubuntu: sudo apt-get install ncurses-bin" >&2
    echo "e.g., on Red Hat/CentOS/Fedora: sudo dnf install ncurses" >&2
    exit 1
fi
# --- End of Check ---

# Function to draw the heart. It's called on start and on window resize.
draw_heart() {
    # Get the current terminal dimensions.
    local cols=$(tput cols)
    local lines=$(tput lines)
    local text="nya~"

    # Hide the cursor for a cleaner look.
    tput civis

    # Move cursor to the top-left corner and clear the part of the screen we'll use.
    # This prevents the screen from "jumping" on redraw.
    tput cup 0 0
    tput ed

    # AWK does all the heavy lifting. It's great at math and string manipulation.
    # We pass our shell variables to awk using the -v option.
    awk -v cols="$cols" -v lines="$lines" -v text="$text" '
    BEGIN {
        # Define ANSI escape codes for a nice pink color and for resetting.
        # This uses 256-color mode, which is supported by most modern terminals.
        color = "\033[38;5;205m";
        reset = "\033[0m";

        text_len = length(text);
        char_idx = 0;

        # Iterate over every character cell in the terminal (y is row, x is column).
        for (y = 0; y < lines; y++) {
            line_buffer = ""; # Build each line in a buffer to print all at once.
            for (x = 0; x < cols; x++) {

                # This is the magic part: the heart equation.
                # First, we normalize the (x, y) terminal coordinates to a mathematical
                # grid where the heart equation works well.
                # Character cells are taller than they are wide, so we scale y differently (by about 2x)
                # to make the heart look proportional. Smaller divisors make the heart bigger.
                # A small vertical offset (-0.2) is added to center the heart better.
                nx = (x - cols / 2) / (cols / 3.5);
                ny = (y - lines / 2) / (lines / 7) - 0.2;

                # The heart equation itself: (x^2 + y^2 - 1)^3 - x^2*y^3 <= 0
                # If the result for a given (nx, ny) point is less than or equal to zero,
                # it is inside the heart.
                val = (nx*nx + ny*ny - 1)^3 - (nx*nx * ny*ny*ny);

                if (val <= 0) {
                    # We are inside the heart! Get the next character from "nya~".
                    # substr is 1-indexed in awk, hence the +1.
                    char = substr(text, (char_idx % text_len) + 1, 1);
                    line_buffer = line_buffer color char reset;
                    char_idx++;
                } else {
                    # We are outside the heart, so just add a space.
                    line_buffer = line_buffer " ";
                }
            }
            # Print the fully assembled line.
            print line_buffer;
        }
    }'
}

# This function runs when the script exits (e.g., via Ctrl+C).
cleanup() {
    # Restore the cursor to its normal state.
    tput cnorm
    # Reset any lingering text colors or attributes.
    tput sgr0
    # Clear the screen one last time.
    clear
    exit 0
}

# Set up "traps" to catch signals from the operating system.
# trap cleanup SIGINT: When Ctrl+C (SIGINT) is pressed, run the cleanup function.
# trap draw_heart SIGWINCH: When the window is resized (SIGWINCH), run the draw_heart function.
trap cleanup SIGINT
trap draw_heart SIGWINCH

# Clear the screen and perform the first draw.
clear
draw_heart

# Keep the script alive so it can listen for resize events.
# A simple "read" command is an efficient way to pause indefinitely
# without using a busy loop like "while true; do sleep 1; done".
read -r -d ''
