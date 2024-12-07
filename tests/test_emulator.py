import unittest
import os
from emulator.emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator("./resources/config.yaml")

    def test_ls(self):
        output = self.emulator.ls()
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)

    def test_cd(self):
        test_dir = os.path.join(self.emulator.vfs, "test_dir")
        os.makedirs(test_dir, exist_ok=True)
        output = self.emulator.cd("test_dir")
        self.assertEqual(self.emulator.current_dir, test_dir)
        self.assertIn("test_dir", output)

    def test_mkdir(self):
        output = self.emulator.mkdir("new_dir")
        self.assertTrue(os.path.exists(os.path.join(self.emulator.current_dir, "new_dir")))
        self.assertIn("Directory 'new_dir' created", output)

    def test_date(self):
        output = self.emulator.date()
        self.assertRegex(output, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_history(self):
        self.emulator.handle_command("ls")
        self.emulator.handle_command("mkdir test_dir")
        output = self.emulator.history_command()
        self.assertIn("ls", output)
        self.assertIn("mkdir test_dir", output)

    def test_exit(self):
        output = self.emulator.exit()
        self.assertEqual(output, "Exiting shell emulator")

if __name__ == "__main__":
    unittest.main()
