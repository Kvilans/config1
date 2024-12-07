from emulator.emulator import ShellEmulator
from emulator.gui import EmulatorGUI

if __name__ == "__main__":
    emulator = ShellEmulator("./resources/config.yaml")
    gui = EmulatorGUI(emulator)
    gui.start()
