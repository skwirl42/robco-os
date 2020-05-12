import consolekeys

class Program:

    def __init__(self, provider, args):

        self.key_pressed = 0
        self.provider = provider
        self.provider.clear()
        self.provider.refresh()

    def draw(self, provider):

        while self.key_pressed is not ord('q') and self.key_pressed is not consolekeys.ESCAPE:

            self.provider.clear()
            self.provider.print_str(0, 0, 'THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG')
            self.provider.print_str(0, 1, 'the quick brown fox jumped over the lazy dog')
            self.provider.print_str(0, 2, '01234567890123456789')
            self.provider.print_str(0, 3, '!@#$%^&*()_+-=[]{}\\/|,.<>?;:"')
            self.provider.print_str(0, 4, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed')
            self.provider.print_str(0, 5, 'do eiusmod tempor incididunt ut labore et dolore magna')
            self.provider.print_str(0, 6, 'aliqua. Ut enim ad minim veniam, quis nostrud exercitation')
            self.provider.print_str(0, 7, 'ullamco laboris nisi ut aliquip ex ea commodo consequat.')
            self.provider.print_str(0, 8, 'Duis aute irure dolor in reprehenderit in voluptate velit')
            self.provider.print_str(0, 9, 'esse cillum dolore eu fugiat nulla pariatur. Excepteur sint')
            self.provider.print_str(0, 10, 'occaecat cupidatat non proident, sunt in culpa qui officia')
            self.provider.print_str(0, 11, 'deserunt mollit anim id est laborum.')
            self.provider.refresh()

            self.key_pressed = provider.getch()
            self.provider.set_input_blocking_mode(True)

