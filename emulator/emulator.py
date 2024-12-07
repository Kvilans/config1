import zipfile
import os

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.vfs_path = self.config["vfs_path"]
        self.vfs_dir = "virtual_fs"  # Виртуальная файловая система после распаковки
        self.history = []  # Добавляем атрибут для хранения истории команд
        self.load_virtual_fs()

    def load_config(self, config_path):
        """Загрузка конфигурационного файла (формат YAML)"""
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def load_virtual_fs(self):
        """Распаковка архива в виртуальную файловую систему"""
        # Распаковываем архив vfs.zip в виртуальную директорию
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            zip_ref.extractall(self.vfs_dir)

    def mkdir(self, dir_name):
        """Создание директории внутри виртуальной файловой системы в архиве"""
        # Путь к новой директории внутри виртуальной файловой системы
        new_dir_path = os.path.join(self.vfs_dir, dir_name)

        # Если директория уже существует, возвращаем сообщение об ошибке
        if os.path.exists(new_dir_path):
            return f"Directory '{dir_name}' already exists."

        # Создаем директорию в локальной файловой системе
        os.makedirs(new_dir_path)

        # Теперь нужно добавить эту директорию в архив, создав там пустой файл (для имитации директории)
        with zipfile.ZipFile(self.vfs_path, 'a') as zip_ref:
            # Мы добавляем пустой файл для имитации директории в архив
            empty_file_path = os.path.join(new_dir_path, ".empty")
            # Создаем пустой файл в реальной файловой системе
            open(empty_file_path, 'w').close()
            # Добавляем пустой файл в архив
            zip_ref.write(empty_file_path, os.path.relpath(empty_file_path, self.vfs_dir))

        return f"Directory '{dir_name}' created in VFS."

    def ls(self):
        """Выводит список файлов и директорий в текущем каталоге"""
        contents = os.listdir(self.vfs_dir)
        return "\n".join(contents)

    def cd(self, path):
        """Переход в указанный каталог"""
        full_path = os.path.join(self.vfs_dir, path)
        if os.path.isdir(full_path):
            self.vfs_dir = full_path
            return f"Changed directory to {self.vfs_dir}"
        else:
            return f"Error: Directory '{path}' not found."

    def show_history(self):
        """Выводит историю команд"""
        return "\n".join(self.history)

    def handle_command(self, command):
        """Обработка команд и выполнение действий"""
        command = command.strip()

        # Сохраняем команду в истории
        self.history.append(command)

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
            else:
                output = "Command not found."
        except Exception as e:
            output = f"Error: {str(e)}"
        
        return output

    def exit(self):
        """Завершается выполнение эмулятора"""
        return "Exiting shell emulator."
