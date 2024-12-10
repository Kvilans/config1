import zipfile
import os
from datetime import datetime


class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.vfs_path = self.config["vfs_path"]
        self.current_dir = ""  # Текущая директория внутри архива
        self.history = []  # История команд

        # Проверка существования zip-файла
        if not zipfile.is_zipfile(self.vfs_path):
            raise FileNotFoundError(f"VFS file '{self.vfs_path}' not found or is not a valid ZIP archive.")

    def load_config(self, config_path):
        """Загрузка конфигурационного файла (формат YAML)"""
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def normalize_path(self, path):
        """Приведение пути к нормализованному формату внутри архива"""
        normalized = os.path.normpath(f"{self.current_dir}/{path}").lstrip("/")
        return normalized if normalized != "." else ""

    def list_dir(self, dir_path):
        """Список файлов и папок в указанной директории архива"""
        dir_path = dir_path.rstrip("/") + "/"
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            items = [name[len(dir_path):].split('/')[0] for name in zip_ref.namelist()
                     if name.startswith(dir_path) and name != dir_path]
            return sorted(set(items))

    def mkdir(self, dir_name):
        """Создание директории внутри архива"""
        if not dir_name:
            return "Error: Directory name is required."

        full_path = self.normalize_path(dir_name) + "/"
        with zipfile.ZipFile(self.vfs_path, 'a') as zip_ref:
            if any(name.startswith(full_path) for name in zip_ref.namelist()):
                return f"Error: Directory '{dir_name}' already exists."
            zip_ref.writestr(full_path, "")  # Создаем запись для папки в архиве
        return f"Directory '{dir_name}' created."

    def ls(self):
        """Выводит список файлов и директорий в текущем каталоге"""
        contents = self.list_dir(self.current_dir)
        return "\n".join(contents) if contents else "Directory is empty."

    def cd(self, path):
        """Переход в указанный каталог"""
        # Обработка относительного или абсолютного пути
        if path == "/":
            target_dir = ""  # Переход в корень
        else:
            target_dir = os.path.normpath(f"{self.current_dir}/{path}").lstrip("/")

        # Проверка существования директории
        target_dir_with_slash = target_dir.rstrip("/") + "/"  # Убедиться, что это папка
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            if target_dir_with_slash not in zip_ref.namelist():
                return f"Error: Directory '{path}' not found."

        # Обновление текущей директории
        self.current_dir = target_dir
        return f"Changed directory to {self.current_dir or '/'}"

    def show_history(self):
        """Выводит историю команд"""
        return "\n".join(self.history)

    def date(self):
        """Вывод текущей даты и времени"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def handle_command(self, command):
        """Обработка команд и выполнение действий"""
        command = command.strip()
        self.history.append(command)  # Сохраняем команду в историю

        try:
            if command == "ls":
                output = self.ls()
            elif command.startswith("cd"):
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    output = self.cd(parts[1])
                else:
                    output = "No directory specified for 'cd' command."
            elif command == "exit":
                output = self.exit()
            elif command == "history":
                output = self.show_history()
            elif command.startswith("mkdir"):
                parts = command.split(" ", 1)
                if len(parts) > 1:
                    output = self.mkdir(parts[1])
                else:
                    output = "Directory name is required."
            elif command == "date":
                output = self.date()
            else:
                output = "Command not found."
        except Exception as e:
            output = f"Error: {str(e)}"

        return output

    def exit(self):
        """Завершение работы эмулятора"""
        return "Exiting shell emulator."
