import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Файл для хранения данных
        self.data_file = "movies.json"

        # Загрузка существующих фильмов
        self.movies = self.load_movies()

        # Создание интерфейса
        self.create_widgets()

        # Обновление списка фильмов
        self.refresh_movie_list()

    def load_movies(self):
        """Загрузка фильмов из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_movies(self):
        """Сохранение фильмов в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.movies, file, ensure_ascii=False, indent=2)
            return True
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить фильмы")
            return False

    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        # Основной фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление нового фильма", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.bind('<Return>', lambda e: self.add_movie())

        ttk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w", padx=5)
        self.genre_entry = ttk.Entry(input_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)
        self.genre_entry.bind('<Return>', lambda e: self.add_movie())

        ttk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w", padx=5)
        self.year_entry = ttk.Entry(input_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)
        self.year_entry.bind('<Return>', lambda e: self.add_movie())

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="w", padx=5)
        self.rating_entry = ttk.Entry(input_frame, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)
        self.rating_entry.bind('<Return>', lambda e: self.add_movie())

        # Кнопки действий
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Добавить фильм", command=self.add_movie).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить поля", command=self.clear_entries).pack(side="left", padx=5)

        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация фильмов", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5)
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_entry = ttk.Entry(filter_frame, textvariable=self.filter_genre_var, width=25)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)
        self.filter_genre_var.trace('w', lambda *args: self.refresh_movie_list())

        # Фильтр по году
        ttk.Label(filter_frame, text="Фильтр по году:").grid(row=1, column=0, sticky="w", padx=5)
        self.filter_year_var = tk.StringVar()
        self.filter_year_entry = ttk.Entry(filter_frame, textvariable=self.filter_year_var, width=25)
        self.filter_year_entry.grid(row=1, column=1, padx=5, pady=5)
        self.filter_year_var.trace('w', lambda *args: self.refresh_movie_list())

        # Кнопка сброса фильтров
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=2, rowspan=2,
                                                                                           padx=20)

        # Фрейм для списка фильмов
        list_frame = ttk.LabelFrame(self.root, text="Список фильмов", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание Treeview для отображения фильмов
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Настройка колонок
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")

        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=100)
        self.tree.column("Рейтинг", width=100)

        # Скроллбар для списка
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Фрейм для кнопок управления списком
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Удалить выбранный", command=self.delete_movie).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Редактировать", command=self.edit_movie).pack(side="left", padx=5)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готов")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=10, pady=5)

        # Привязка обработчика двойного клика для редактирования
        self.tree.bind("<Double-Button-1>", lambda e: self.edit_movie())

    def validate_year(self, year):
        """Валидация года выпуска"""
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if 1888 <= year_int <= current_year + 1:
                return True, year_int
            else:
                return False, f"Год должен быть от 1888 до {current_year + 1}"
        except ValueError:
            return False, "Год должен быть целым числом"

    def validate_rating(self, rating):
        """Валидация рейтинга"""
        try:
            rating_float = float(rating)
            if 0 <= rating_float <= 10:
                return True, rating_float
            else:
                return False, "Рейтинг должен быть от 0 до 10"
        except ValueError:
            return False, "Рейтинг должен быть числом"

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        # Проверка обязательных полей
        if not title:
            messagebox.showwarning("Предупреждение", "Название фильма обязательно!")
            return

        if not genre:
            messagebox.showwarning("Предупреждение", "Жанр фильма обязателен!")
            return

        # Валидация года
        is_valid_year, year_result = self.validate_year(year)
        if not is_valid_year:
            messagebox.showwarning("Ошибка валидации", year_result)
            return

        # Валидация рейтинга
        is_valid_rating, rating_result = self.validate_rating(rating if rating else "0")
        if not is_valid_rating:
            messagebox.showwarning("Ошибка валидации", rating_result)
            return

        # Проверка на дубликаты
        for movie in self.movies:
            if movie["title"].lower() == title.lower() and movie["year"] == year_result:
                if messagebox.askyesno("Дубликат", f"Фильм '{title}' ({year_result}) уже существует.\nЗаменить его?"):
                    movie["genre"] = genre
                    movie["rating"] = rating_result
                    self.save_movies()
                    self.refresh_movie_list()
                    self.status_var.set(f"Фильм '{title}' обновлен")
                    self.clear_entries()
                return

        # Добавление нового фильма
        new_movie = {
            "title": title,
            "genre": genre,
            "year": year_result,
            "rating": rating_result,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.movies.append(new_movie)

        if self.save_movies():
            self.refresh_movie_list()
            self.status_var.set(f"Фильм '{title}' добавлен")
            self.clear_entries()
        else:
            self.movies.pop()  # Удаляем из памяти, если не сохранилось

    def delete_movie(self):
        """Удаление выбранного фильма"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return

        # Получение данных выбранного фильма
        item = self.tree.item(selection[0])
        movie_title = item['values'][0]
        movie_year = item['values'][2]

        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{movie_title}' ({movie_year})?"):
            # Поиск и удаление фильма
            for i, movie in enumerate(self.movies):
                if movie["title"] == movie_title and movie["year"] == int(movie_year):
                    del self.movies[i]
                    break

            if self.save_movies():
                self.refresh_movie_list()
                self.status_var.set(f"Фильм '{movie_title}' удален")

    def edit_movie(self):
        """Редактирование выбранного фильма"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите фильм для редактирования!")
            return

        # Получение данных выбранного фильма
        item = self.tree.item(selection[0])
        movie_title = item['values'][0]
        movie_genre = item['values'][1]
        movie_year = item['values'][2]
        movie_rating = item['values'][3]

        # Заполнение полей для редактирования
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, movie_title)
        self.genre_entry.delete(0, tk.END)
        self.genre_entry.insert(0, movie_genre)
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, movie_year)
        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, movie_rating)

        # Удаление старого фильма
        for i, movie in enumerate(self.movies):
            if movie["title"] == movie_title and movie["year"] == int(movie_year):
                del self.movies[i]
                break

        self.status_var.set(f"Редактирование фильма '{movie_title}'")
        self.title_entry.focus()

    def clear_entries(self):
        """Очистка полей ввода"""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.title_entry.focus()

    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_genre_var.set("")
        self.filter_year_var.set("")
        self.refresh_movie_list()
        self.status_var.set("Фильтры сброшены")

    def refresh_movie_list(self):
        """Обновление списка фильмов в интерфейсе"""
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Фильтрация фильмов
        filter_genre = self.filter_genre_var.get().lower()
        filter_year = self.filter_year_var.get().strip()

        filtered_movies = self.movies

        if filter_genre:
            filtered_movies = [
                movie for movie in self.movies
                if filter_genre in movie["genre"].lower()
            ]

        if filter_year:
            try:
                year_int = int(filter_year)
                filtered_movies = [
                    movie for movie in filtered_movies
                    if movie["year"] == year_int
                ]
            except ValueError:
                pass

        # Добавление отфильтрованных фильмов в список
        for movie in filtered_movies:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}" if isinstance(movie['rating'], float) else str(movie['rating'])
            ))

        # Обновление статусной строки
        total = len(self.movies)
        shown = len(filtered_movies)
        if filter_genre or filter_year:
            self.status_var.set(f"Найдено {shown} из {total} фильмов")
        else:
            self.status_var.set(f"Всего фильмов: {total}")


def main():
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()


if __name__ == "__main__":
    main()
