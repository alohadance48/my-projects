import os
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


class SortForFile:
    """Класс для сортировки файлов по расширениям в указанной директории."""

    def __init__(self, directory):
        """Инициализация класса с заданной директорией."""
        self.directory = directory

    def sort_files(self, extensions):
        """
        Сортирует файлы по указанным расширениям.

        :param extensions: список расширений файлов для сортировки
        :return: общее количество файлов и количество перемещённых файлов
        """
        sorted_files_count = 0
        total_files_count = 0
        file_counts = {ext: 0 for ext in extensions}

        # Создаем папки для каждого расширения
        for ext in extensions:
            ext_folder = os.path.join(self.directory, ext)
            if not os.path.exists(ext_folder):
                os.makedirs(ext_folder)

        # Перемещаем файлы в соответствующие папки и считаем их
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                total_files_count += 1
                for ext in extensions:
                    if filename.lower().endswith(ext):
                        destination_path = os.path.join(self.directory, ext, filename)
                        os.rename(file_path, destination_path)
                        sorted_files_count += 1
                        file_counts[ext] += 1

        return total_files_count, sorted_files_count, file_counts


class SortForFileApp:
    """Графический интерфейс для сортировки файлов."""

    def __init__(self, master):
        """Инициализация главного окна приложения."""
        self.master = master
        master.title("Сортировка файлов")

        self.label = tk.Label(master, text="Введите путь к директории:")
        self.label.pack()

        self.directory_entry = tk.Entry(master)
        self.directory_entry.pack()

        self.extensions_label = tk.Label(master, text="Введите расширения (через запятую):")
        self.extensions_label.pack()

        self.extensions_entry = tk.Entry(master)
        self.extensions_entry.pack()

        self.sort_button = tk.Button(master, text="Сортировать", command=self.sort_files)
        self.sort_button.pack()

    def sort_files(self):
        """Обрабатывает ввод пользователя и запускает сортировку файлов."""
        directory = self.directory_entry.get()
        extensions_input = self.extensions_entry.get()

        # Обработка ввода расширений
        extensions = [ext.strip() for ext in extensions_input.split(',')]

        if not os.path.isdir(directory):
            messagebox.showerror("Ошибка", "Указанная директория не существует.")
            return

        sorter = SortForFile(directory)

        total_files_count, sorted_files_count, file_counts = sorter.sort_files(extensions)

        # Отображаем статистику
        messagebox.showinfo("Статистика", f"Всего файлов: {total_files_count}\nПеремещено файлов: {sorted_files_count}")

        # Визуализация статистики в виде диаграммы
        self.plot_statistics(file_counts)

    def plot_statistics(self, file_counts):
        """Создает столбчатую диаграмму для отображения статистики по файлам."""
        labels = list(file_counts.keys())
        counts = list(file_counts.values())

        plt.bar(labels, counts)
        plt.xlabel('Расширения')
        plt.ylabel('Количество файлов')
        plt.title('Статистика по количеству файлов различных форматов')

        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = SortForFileApp(root)
    root.mainloop()
