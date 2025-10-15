from turtle import *
import time

# A graphical version of the "nya~" heart script using Python's turtle module.
# This script will open a new window and draw the heart.
#
# Coded with <3
#
# Usage:
#   1. Save this file as nya_heart_turtle.py
#   2. Run it from your terminal: python3 nya_heart_turtle.py
#   3. Watch the heart get drawn!
#   4. Close the window to exit.

def draw_filled_heart():
    """
    Sets up the turtle environment and draws a heart filled with text.
    """
    # --- Setup the Screen ---
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.bgcolor("black")
    screen.title("Drawing a heart for you... nya~")
    # Turn off tracer for instant drawing. If you want to see it animate,
    # comment out the next line and the screen.update() at the end.
    screen.tracer(0)

    # --- Setup the Turtle (our "pen") ---
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("#FF69B4")  # A lovely hot pink color

    # --- Drawing Configuration ---
    text = "nya~"
    char_index = 0
    font_size = 12
    font_style = ("Courier", font_size, "bold")
    
    # Adjust these to change heart size and text density
    y_range = range(15, -18, -1) # Vertical range to scan
    x_range = range(-30, 31)   # Horizontal range to scan
    x_spacing = 10             # Horizontal space between characters
    y_spacing = 18             # Vertical space between lines

    # --- The Drawing Loop ---
    # We will scan a grid of points. If a point is inside the heart equation,
    # we'll write a character there. This is like creating a pixelated text image.
    
    for y in y_range:
        for x in x_range:
            # This is the same heart equation used in the terminal scripts.
            # We normalize the coordinates to make the equation work.
            nx = x * 0.05
            ny = y * 0.1

            val = (nx**2 + ny**2 - 1)**3 - (nx**2 * ny**3)

            if val <= 0:
                # This point is inside the heart!
                # Go to the calculated screen position.
                writer.goto(x * x_spacing, y * y_spacing)
                
                # Get the next character from "nya~".
                char_to_write = text[char_index % len(text)]
                
                # Write the character to the screen.
                writer.write(char_to_write, align="center", font=font_style)
                
                char_index += 1

    # --- Finalize ---
    # Update the screen to show the completed drawing all at once.
    screen.update()
    
    # Keep the window open until it's closed by the user.
    screen.mainloop()


if __name__ == "__main__":
    draw_filled_heart()
