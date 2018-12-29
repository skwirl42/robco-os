import tcod
import curses
import consolekeys
import simpleaudio
import os
import random
from abc import ABC, abstractmethod

"""
Program modules must define:
- a class named Program, with the following methods:
  - a constructor taking a provider as an argument
  - a draw method, which takes a BaseOSProvider as an argument
  - a holotape_inserted method, which takes a path to a local file
    - this will be implemented in the future, depending on the host OS
"""

"""
The console is assumed to be 55x22 based on an (un)educated guess
"""
class BaseOSProvider(ABC):
    def common_setup(self):
        self.is_blocking = True

        sounds_path = "sounds"
        self.sfx_enter = []
        self.sfx_char = []

        enter_sounds_path = os.path.join(sounds_path, "enter")
        if os.path.isdir(enter_sounds_path):
            for file in os.listdir(enter_sounds_path):
                self.sfx_enter.append(simpleaudio.WaveObject.from_wave_file(os.path.join(enter_sounds_path, file)))

        char_sounds_path = os.path.join(sounds_path, "char")
        if os.path.isdir(char_sounds_path):
            for file in os.listdir(char_sounds_path):
                self.sfx_char.append(simpleaudio.WaveObject.from_wave_file(os.path.join(char_sounds_path, file)))

        self.sfx_ack = simpleaudio.WaveObject.from_wave_file(os.path.join(sounds_path, 'passgood.wav'))
        self.sfx_nack = simpleaudio.WaveObject.from_wave_file(os.path.join(sounds_path, 'passbad.wav'))
        self.sfx_reset = simpleaudio.WaveObject.from_wave_file(os.path.join(sounds_path, 'passreset.wav'))
        self.sfx_clear = simpleaudio.WaveObject.from_wave_file(os.path.join(sounds_path, 'passdud.wav'))

    def play_sound_for_char(self, char):
        # Subclasses: Override this method for the appropriate sounds per char
        random.choice(self.sfx_char).play()

    def play_sound(self, sound_name):
        if sound_name == "ack":
            self.sfx_ack.play()
        elif sound_name == "nack":
            self.sfx_nack.play()
        elif sound_name == "reset":
            self.sfx_reset.play()
        elif sound_name == "clear":
            self.sfx_clear.play()

    # Loads and runs the module identified by module_name and runs it
    # replacing the currently running module
    def execute_program_import(self, program_name):
        module = __import__("programs." + program_name, globals(), locals(), [program_name])
        return module.Program(self)

    # getch must return an int that is ether an ASCII code or a constant from consolekeys
    @abstractmethod
    def getch(self):
        pass

    # sets the character at x,y in the console to ch
    @abstractmethod
    def set_character(self, x, y, ch):
        pass

    @abstractmethod
    def print_str(self, x, y, string):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def execute_program(self, program):
        pass

    @abstractmethod
    def set_input_blocking_mode(self, is_blocking):
        pass

class TcodOSProvider(BaseOSProvider):
    def __init__(self):
        self.common_setup()
        self.console = tcod.console_init_root(w=55, h=22)
        self.console.default_fg = (0, 255, 0)
        self.console.default_bg = (0, 0, 0)

    def execute_program(self, program_name):
        # TODO: Start a rendering loop to run this continuously
        program = self.execute_program_import(program_name)
        program.draw(self)

    def getch(self):
        key = tcod.KEY_NONE
        char = consolekeys.NO_KEY
        if self.is_blocking:
            key = tcod.console_wait_for_keypress(False)
        else:
            key = tcod.console_check_for_keypress()

        if key == tcod.KEY_NONE or key.vk == tcod.KEY_NONE:
            return consolekeys.NO_KEY
        elif key.vk == tcod.KEY_CHAR:
            char = key.c
        elif key.vk >= tcod.KEY_0 and key.vk <= tcod.KEY_9:
            char = key.vk
        elif key.vk >= tcod.KEY_F1 and key.vk <= tcod.KEY_F12:
            char = consolekeys.FUNC_1 + (key.vk - tcod.KEY_F1)

        if char == consolekeys.NO_KEY:
            mappings = {
                tcod.KEY_BACKSPACE: consolekeys.BACKSPACE,
                tcod.KEY_ENTER: consolekeys.ENTER,

                tcod.KEY_LEFT: consolekeys.LEFT_ARROW,
                tcod.KEY_RIGHT: consolekeys.RIGHT_ARROW,
                tcod.KEY_UP: consolekeys.UP_ARROW,
                tcod.KEY_DOWN: consolekeys.DOWN_ARROW,

                tcod.KEY_HOME: consolekeys.HOME,
                tcod.KEY_END: consolekeys.END,
                tcod.KEY_PAGEUP: consolekeys.PAGE_UP,
                tcod.KEY_PAGEDOWN: consolekeys.PAGE_DOWN,
            }
            char = mappings.get(key.vk, consolekeys.UNKNOWN_KEY)
        self.play_sound_for_char(char)
        return char

    def clear(self):
        self.console.clear()

    def refresh(self):
        tcod.console_flush()

    def set_character(self, x, y, ch):
        self.console.putchar(x, y, ord(ch))

    def print_str(self, x, y, str):
        self.console.print_(x, y, str)

    def set_input_blocking_mode(self, is_blocking):
        self.is_blocking = is_blocking

class CursesProvider(BaseOSProvider):
    def __init__(self):
        self.common_setup()
        self.console = curses.initscr()

    def execute_program(self, program_name):
        self.program = self.execute_program_import(program_name)
        curses.wrapper(self.__curses_wrapper)

    def __curses_wrapper(self, console):
        self.program.draw(self)

    def getch(self):
        getch = self.console.getch()
        char = consolekeys.NO_KEY
        if getch >= ord(' ') and getch <= ord('~'):
            char = getch
        if getch >= curses.KEY_F0 and getch <= curses.KEY_F14:
            char = consolekeys.FUNC_0 + (getch - curses.KEY_F0)

        if char == consolekeys.NO_KEY:
            mappings = {
                curses.KEY_BACKSPACE: consolekeys.BACKSPACE,
                curses.KEY_ENTER: consolekeys.ENTER,

                curses.KEY_LEFT: consolekeys.LEFT_ARROW,
                curses.KEY_RIGHT: consolekeys.RIGHT_ARROW,
                curses.KEY_UP: consolekeys.UP_ARROW,
                curses.KEY_DOWN: consolekeys.DOWN_ARROW,

                curses.KEY_HOME: consolekeys.HOME,
                curses.KEY_END: consolekeys.END,
                curses.KEY_PPAGE: consolekeys.PAGE_UP,
                curses.KEY_NPAGE: consolekeys.PAGE_DOWN,
            }
            char = mappings.get(getch, consolekeys.UNKNOWN_KEY)
        self.play_sound_for_char(char)
        return char

    def set_character(self, x, y, ch):
        self.console.addch(y, x, ch)

    def print_str(self, x, y, str):
        self.console.addstr(y, x, str)

    def clear(self):
        self.console.clear()

    def refresh(self):
        self.console.refresh()

    def set_input_blocking_mode(self, is_blocking):
        self.console.nodelay(not is_blocking)