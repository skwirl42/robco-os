import tcod
import tcod.event
import tcod.console
import consolekeys
import simpleaudio
import os
import random
from abc import ABC, abstractmethod
import PiTerm

"""
Program modules must define:
- a class named Program, with the following methods:
  - a constructor taking a provider as an argument
  - a draw method, which takes a BaseOSProvider as an argument
  - a holotape_inserted method, which takes a path to a local file
	- this will be implemented in the future, depending on the host OS
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
	def execute_program_import(self, program_name, args):
		module = __import__("programs." + program_name, globals(), locals(), [program_name])
		return module.Program(self, args)

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
	def invert_at(self, x, y):
		pass

	@abstractmethod
	def clear(self):
		pass

	@abstractmethod
	def refresh(self):
		pass

	@abstractmethod
	def execute_program(self, program, args):
		pass

	@abstractmethod
	def set_input_blocking_mode(self, is_blocking):
		pass

class TcodOSProvider(BaseOSProvider):
	def __init__(self):
		self.common_setup()
		tcod.console_set_custom_font('font/robco-termfont.png', tcod.FONT_LAYOUT_ASCII_INROW, 16, 8)
		self.console = tcod.console_init_root(w=60, h=24, order='F', fullscreen=True)
		self.console.default_fg = (0, 255, 0)
		self.console.default_bg = (0, 0, 0)

	def execute_program(self, program_name, args):
		# TODO: Start a rendering loop to run this continuously
		program = self.execute_program_import(program_name, args)
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
				tcod.KEY_DELETE: consolekeys.DELETE,
				tcod.KEY_ENTER: consolekeys.ENTER,
				tcod.KEY_ESCAPE: consolekeys.ESCAPE,

				tcod.KEY_LEFT: consolekeys.LEFT_ARROW,
				tcod.KEY_RIGHT: consolekeys.RIGHT_ARROW,
				tcod.KEY_UP: consolekeys.UP_ARROW,
				tcod.KEY_DOWN: consolekeys.DOWN_ARROW,

				tcod.KEY_HOME: consolekeys.HOME,
				tcod.KEY_END: consolekeys.END,
				tcod.KEY_PAGEUP: consolekeys.PAGE_UP,
				tcod.KEY_PAGEDOWN: consolekeys.PAGE_DOWN,

				tcod.KEY_TAB: consolekeys.TAB,
			}
			char = mappings.get(key.vk, consolekeys.UNKNOWN_KEY)
		self.play_sound_for_char(char)
		return char

	def clear(self):
		self.console.clear()

	def refresh(self):
		tcod.console_flush()

	def set_character(self, x, y, ch):
		self.console.put_char(x, y, ord(ch))

	def print_str(self, x, y, str):
		self.console.print_(x, y, str)

	def set_input_blocking_mode(self, is_blocking):
		self.is_blocking = is_blocking

	def invert_at(self, x, y):
		for channel in range(3):
			temp = self.console.fg[x, y, channel]
			self.console.fg[x, y, channel] = self.console.bg[x, y, channel]
			self.console.bg[x, y, channel] = temp

class PiTermProvider(BaseOSProvider):
	def __init__(self):
		self.common_setup()
		PiTerm.alloc('font/robco-termfont.png')
		self.tcodContext = tcod.context.new_window(1920, 1080, sdl_window_flags=tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP)

	def execute_program(self, program_name, args):
		# TODO: Start a rendering loop to run this continuously
		program = self.execute_program_import(program_name, args)
		program.draw(self)

	def clear(self):
		PiTerm.clear()

	def refresh(self):
		PiTerm.refresh()

	def set_character(self, x, y, ch):
		PiTerm.set_character(x, y, ord(ch))

	def print_str(self, x, y, string):
		PiTerm.print_str(x, y, string)

	def invert_at(self, x, y):
		PiTerm.invert_at(x, y)

	def set_input_blocking_mode(self, is_blocking):
		self.is_blocking = is_blocking

	def getch(self):
		if self.is_blocking:
			self.events = tcod.event.wait()
		else:
			self.events = tcod.event.get()
		for event in self.events:
			if event.type == "KEYDOWN":
				key = event.sym
				char = consolekeys.NO_KEY
				if key == tcod.event.K_UNKNOWN:
					return consolekeys.NO_KEY
				elif key >= tcod.event.K_a and key <= tcod.event.K_z:
					char = ord('a') + (key - tcod.event.K_a)
				elif key >= tcod.event.K_0 and key <= tcod.event.K_9:
					char = ord('0') + (key - tcod.event.K_0)
				elif key >= tcod.event.K_F1 and key <= tcod.event.K_F12:
					char = consolekeys.FUNC_1 + (key - tcod.event.K_F1)

				if char == consolekeys.NO_KEY:
					mappings = {
						tcod.event.K_BACKSPACE: consolekeys.BACKSPACE,
						tcod.event.K_DELETE: consolekeys.DELETE,
						tcod.event.K_RETURN: consolekeys.ENTER,
						tcod.event.K_ESCAPE: consolekeys.ESCAPE,

						tcod.event.K_LEFT: consolekeys.LEFT_ARROW,
						tcod.event.K_RIGHT: consolekeys.RIGHT_ARROW,
						tcod.event.K_UP: consolekeys.UP_ARROW,
						tcod.event.K_DOWN: consolekeys.DOWN_ARROW,

						tcod.event.K_HOME: consolekeys.HOME,
						tcod.event.K_END: consolekeys.END,
						tcod.event.K_PAGEUP: consolekeys.PAGE_UP,
						tcod.event.K_PAGEDOWN: consolekeys.PAGE_DOWN,

						tcod.event.K_TAB: consolekeys.TAB,
					}
					char = mappings.get(key, consolekeys.UNKNOWN_KEY)
					self.play_sound_for_char(char)
					return char
			elif event.type == "QUIT":
				return consolekeys.ESCAPE

