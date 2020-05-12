# -*- coding: utf-8 -*-
"""
This is an effort to run "programs" in a simulated RobCo Termlink session.
It works somewhat like an OS by providing services to the python modules that
it launches into a Termlink-like terminal.
"""

import argparse
import consolekeys
import console_providers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute the RobCo OS simulator")
    parser.add_argument("program", help="the RobCo OS program to launch")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="arguments passed to the program")
    mainargs = parser.parse_args()
    provider = console_providers.TcodOSProvider()
    provider.execute_program(mainargs.program, mainargs.args)
