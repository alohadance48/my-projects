import os

def main():
    class SortOnUnix:
        def __init__(self):
            self.source_dir = input('Введите путь к директории для сортировки: ')
            self.target_dir = input('Введите путь к целевой директории: ')
            self.name_for_dir_sort = 'sort'

            # Проверяем, существует ли исходная директория
            if not os.path.exists(self.source_dir):
                print(f"Исходная директория '{self.source_dir}' не найдена.")
                return

            # Создаем целевую директорию, если она не существует
            os.makedirs(self.target_dir, exist_ok=True)

        def sort_files(self):
            # Проходим по всем файлам в исходной директории
            for filename in os.listdir(self.source_dir):
                file_path = os.path.join(self.source_dir, filename)

                # Проверяем, является ли это файлом
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    ext = ext[1:]  # Убираем точку из расширения

                    # Создаем директорию для данного расширения в целевой директории
                    extension_dir = os.path.join(self.target_dir, ext)
                    os.makedirs(extension_dir, exist_ok=True)

                    # Перемещаем файл в соответствующую директорию
                    new_file_path = os.path.join(extension_dir, filename)
                    os.rename(file_path, new_file_path)
                    print(f"Файл '{filename}' перемещен в '{extension_dir}'.")

    sorter = SortOnUnix()
    sorter.sort_files()

if __name__ == '__main__':
    main()
