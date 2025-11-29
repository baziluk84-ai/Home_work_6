import os
import shutil
from multiprocessing import Process, cpu_count
import tkinter as tk
from tkinter import filedialog, messagebox


def archive_folder(folder_path: str, output_dir: str):
    """Функція архівування — виконується в окремому процесі."""
    folder_name = os.path.basename(folder_path)
    archive_path = os.path.join(output_dir, folder_name)

    # створює ZIP-архів
    shutil.make_archive(archive_path, 'zip', folder_path)


def start_archiving(base_folder: str):
    """Створює процеси та запускає архівування всіх вкладених папок першого рівня."""

    if not os.path.isdir(base_folder):
        messagebox.showerror("Помилка", "Вибрана папка недійсна.")
        return

    subfolders = [
        os.path.join(base_folder, f)
        for f in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, f))
    ]

    if not subfolders:
        messagebox.showinfo("Інформація", "У вибраній папці немає вкладених директорій.")
        return

    processes = []
    limit = cpu_count()  # обмеження на кількість одночасних процесів

    output_dir = base_folder  # архіви зберігаються тут же

    for folder in subfolders:

        p = Process(target=archive_folder, args=(folder, output_dir))
        processes.append(p)
        p.start()

        # якщо процесів забагато — чекаємо
        while len([pr for pr in processes if pr.is_alive()]) >= limit:
            pass

    # чекаємо завершення всіх процесів
    for p in processes:
        p.join()

    messagebox.showinfo("Готово", "Архівування завершено.")


def create_gui():
    """Створення інтерфейсу Tkinter."""
    root = tk.Tk()
    root.title("Архіватор папок")

    # Поле введення шляху
    path_var = tk.StringVar()

    entry = tk.Entry(root, textvariable=path_var, width=60)
    entry.pack(pady=10)

    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            path_var.set(folder)

    tk.Button(root, text="Вибрати папку", command=select_folder).pack(pady=5)



    def on_start():
        folder = path_var.get().strip()
        if folder:
            start_archiving(folder)
        else:
            messagebox.showwarning("Увага", "Спочатку виберіть папку.")

    tk.Button(root, text="Запустити архівування", command=on_start).pack(pady=10)

    root.mainloop()


# ------------------ ГОЛОВНИЙ ВХІД --------------------
if __name__ == "__main__":
    create_gui()