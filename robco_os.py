# -*- coding: utf-8 -*-
"""
This is an effort to run "programs" in a simulated RobCo Termlink session.
It works somewhat like an OS by providing services to the python modules that
it launches into a Termlink-like terminal.
"""

import argparse
import consolekeys
import console_providers

class ProviderAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == "tcod":
            namespace.provider = console_providers.TcodOSProvider
        else:
            namespace.provider = console_providers.CursesProvider

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Excute the RobCo OS simulator")
    parser.add_argument("--provider", default=console_providers.CursesProvider, action=ProviderAction, nargs=1, choices=["curses", "tcod"], help="selects which console provider is used")
    parser.add_argument("program", help="the RobCo OS program to launch")
    args = parser.parse_args()
    providerClass = args.provider
    provider = providerClass()
    provider.execute_program(args.program)
