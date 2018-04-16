import curses
import chases

# chases.init()

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

if __name__ == "__main__":
    try:
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                chases.forward(60)
            elif char == curses.KEY_DOWN:
                chases.backwards(60)
            elif char == curses.KEY_LEFT:
                chases.left(50)
            elif char == curses.KEY_RIGHT:
                chases.right(50)
    finally:
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()

        chases.cleanup()