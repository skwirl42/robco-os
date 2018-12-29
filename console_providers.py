import tcod
import curses
import simpleaudio
import os
import random

"""
The console is assumed to be 55x22 based on an (un)educated guess
"""
class BaseOSProvider:
    def __init__(self):
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

    # getch will return an ASCII code or a constant from consolekeys
    def getch(self):
        # Subclasses: Implement the proper library's implementation of getch
        # in __platform_getch
        char = self.__platform_getch()
        self.play_sound_for_char(char)

    def play_sound_for_char(self, char):
        # Subclasses: Override this method for the appropriate sounds per char
        random.choice(sfx_char).play()

    # Loads and runs the module identified by module_name and runs it
    # replacing the currently running module
    def execute_module(self, module_name):
        # TODO: Execute the requested module, passing this provider on to the
        # new module
        print("Intending to run the {0} module".format(module_name))

    def play_sound(self, sound_name):
        if sound_name == "ack":
            self.sfx_ack.play()
        elif sound_name == "nack":
            self.sfx_nack.play()
        elif sound_name == "reset":
            self.sfx_reset.play()
        elif sound_name == "clear":
            self.sfx_clear.play()

class TcodOSProvider(BaseOSProvider):
    def __init__(self):
        BaseOSProvider.__init__(self)
        self.console = tcod.console_init_root(w=55, h=22)

class CursesProvider(BaseOSProvider):
    def __init__(self):
        BaseOSProvider.__init__(self)
        self.console = curses.initscr()

    def __platform_getch(self):
        getch = self.console.getch()
        if getch >= ord(' ') and getch <= ord('~'):
            return getch
        if getch >= curses.KEY_F0 and getch <= curses.KEY_F14:
            return consolekeys.FUNC_0 + (getch - curses.KEY_F0)
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
        return mappings.get(getch, consolekeys.UNKNOWN_KEY)
