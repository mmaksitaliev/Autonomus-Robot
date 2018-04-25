# Chases testing

import curses
import chassis, lights

lights.setup()
# chases.init()

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

if __name__ == "__main__":
    try:
        lights.blink(3)
        lights.on()
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                chassis.forward(40)
            elif char == curses.KEY_DOWN:
                chassis.backwards(35)
            elif char == curses.KEY_LEFT:
                chassis.left(60)
            elif char == curses.KEY_RIGHT:
                chassis.right(60)
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

        lights.cleanup()
