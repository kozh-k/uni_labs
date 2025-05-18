import tkinter as tk
import time

class SimpleEditor:
    def __init__(self, master):
        self.master = master
        master.title("Простой графический редактор")

        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

        self.start_x = None
        self.start_y = None
        self.current_algorithm = "bresenham"  # По умолчанию - Брезенхем

        # Кнопки для выбора алгоритма
        self.bresenham_button = tk.Button(master, text="Брезенхем", command=lambda: self.set_algorithm("bresenham"))
        self.bresenham_button.pack()
        self.dda_button = tk.Button(master, text="ЦДА", command=lambda: self.set_algorithm("dda"))
        self.dda_button.pack()
        self.wu_button = tk.Button(master, text="Ву", command=lambda: self.set_algorithm("wu"))
        self.wu_button.pack()

        # Отладочный режим
        self.debug_mode = tk.BooleanVar()
        self.debug_checkbutton = tk.Checkbutton(master, text="Отладочный режим", variable=self.debug_mode)
        self.debug_checkbutton.pack()

        # Шаг сетки (для отладочного режима)
        self.grid_step = 10 # Уменьшаем шаг сетки в 2 раза

    def set_algorithm(self, algorithm):
        """Устанавливает текущий алгоритм рисования."""
        self.current_algorithm = algorithm

    def draw_grid(self):
        """Рисует дискретную сетку на канве."""
        grid_color = "lightgray"
        for i in range(0, self.canvas_width, self.grid_step):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill=grid_color)
        for i in range(0, self.canvas_height, self.grid_step):
            self.canvas.create_line(0, i, self.canvas_width, i, fill=grid_color)

    def putpixel(self, x, y, color="black", algorithm=""):
        """Рисует пиксель на канве."""
        if self.debug_mode.get():
            # Отладочный режим: рисуем с учетом сетки
            x0 = x * self.grid_step
            y0 = y * self.grid_step
            x1 = x0 + self.grid_step
            y1 = y0 + self.grid_step
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
            text_color = "red"
            self.canvas.create_text(x0 + self.grid_step/2, y0 + self.grid_step/2,
                                    text=f"({x}, {y})", fill=text_color)
            self.master.update()
            time.sleep(0.01)
        else:
            # Обычный режим: рисуем пиксель размером 1x1
            self.canvas.create_rectangle(x, y, x, y, fill=color, outline=color)

    def bresenham(self, x1, y1, x2, y2):
        """Алгоритм Брезенхема для рисования линии."""
        if self.debug_mode.get():
            # Отладочный режим: работаем с координатами сетки
            # Делим координаты на размер ячейки сетки
            x1 //= self.grid_step
            y1 //= self.grid_step
            x2 //= self.grid_step
            y2 //= self.grid_step

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            x = x1
            y = y1
            while True:
                self.putpixel(x, y, color="black", algorithm="Брезенхем")
                if x == x2 and y == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy
        else:
            # Обычный режим: используем оригинальный алгоритм Брезенхема
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            x = x1
            y = y1
            while True:
                self.putpixel(x, y, color="black", algorithm="Брезенхем")
                if x == x2 and y == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x += sx
                if e2 < dx:
                    err += dx
                    y += sy

    def dda(self, x1, y1, x2, y2):
        """Алгоритм ЦДА (DDA) для рисования линии."""
        if self.debug_mode.get():
            # Отладочный режим: работаем с координатами сетки
            # Делим координаты на размер ячейки сетки
            x1 //= self.grid_step
            y1 //= self.grid_step
            x2 //= self.grid_step
            y2 //= self.grid_step

            dx = x2 - x1
            dy = y2 - y1

            if abs(dx) > abs(dy):
                steps = abs(dx)
            else:
                steps = abs(dy)

            x_inc = dx / steps
            y_inc = dy / steps

            x = x1
            y = y1

            for i in range(steps):
                self.putpixel(round(x), round(y), color="black", algorithm="ЦДА")
                x += x_inc
                y += y_inc
        else:
            # Обычный режим: используем оригинальный алгоритм ЦДА
            dx = x2 - x1
            dy = y2 - y1

            if abs(dx) > abs(dy):
                steps = abs(dx)
            else:
                steps = abs(dy)

            x_inc = dx / steps
            y_inc = dy / steps

            x = x1
            y = y1

            for i in range(steps):
                self.putpixel(round(x), round(y), color="black", algorithm="ЦДА")
                x += x_inc
                y += y_inc

    def wu(self, x1, y1, x2, y2):
        """Алгоритм Ву для рисования линии с антиалиасингом."""
        def putpixel_wu(x, y, intensity):
            """Рисует пиксель с учетом интенсивности (антиалиасинг)"""
            color = self.intensity(intensity)
            self.putpixel(x, y, color=color, algorithm="Ву")

        if self.debug_mode.get():
            # Отладочный режим: работаем с координатами сетки
            # Делим координаты на размер ячейки сетки
            x1 //= self.grid_step
            y1 //= self.grid_step
            x2 //= self.grid_step
            y2 //= self.grid_step

            # Используем алгоритм из обычного режима, но с дискретными координатами
            steep = abs(y2 - y1) > abs(x2 - x1)

            # Изменяем порядок координат, если линия крутая
            if steep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2

            dx = x2 - x1
            dy = y2 - y1

            gradient = dy / dx

            x_end = round(x1)
            y_end = y1 + gradient * (x_end - x1)
            x_gap = 1 - (x1 - int(x1))
            xpxl1 = x_end
            ypxl1 = int(y_end)

            def plot(x, y, brightness):
                if steep:
                    putpixel_wu(y, x, brightness)
                else:
                    putpixel_wu(x, y, brightness)

            plot(xpxl1, ypxl1, 1 - (y_end - int(y_end)))
            plot(xpxl1, ypxl1 + 1, y_end - int(y_end))
            intery = y_end + gradient

            x_start = xpxl1 + 1
            x_end_loop = x2

            if x1 > x2:
                x_start = xpxl1 - 1
                x_end_loop = x2
                gradient = -gradient  # Инвертируем градиент

            x = x_start
            while (x <= x_end_loop) if (x1 <= x2) else (x >= x_end_loop):
                plot(x, int(intery), 1 - (intery - int(intery)))
                plot(x, int(intery) + 1, intery - int(intery))
                intery += gradient
                x += 1 if (x1 <= x2) else -1
        else:
            # Обычный режим: используем оригинальный алгоритм Ву
            steep = abs(y2 - y1) > abs(x2 - x1)

            # Изменяем порядок координат, если линия крутая
            if steep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2

            # Изменяем порядок координат, если x1 > x2
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            dx = x2 - x1
            dy = y2 - y1

            gradient = dy / dx

            x_end = round(x1)
            y_end = y1 + gradient * (x_end - x1)
            x_gap = 1 - (x1 - int(x1))
            xpxl1 = x_end
            ypxl1 = int(y_end)

            def plot(x, y, brightness):
                if steep:
                    putpixel_wu(y, x, brightness)
                else:
                    putpixel_wu(x, y, brightness)

            plot(xpxl1, ypxl1, 1 - (y_end - int(y_end)))
            plot(xpxl1, ypxl1 + 1, y_end - int(y_end))
            intery = y_end + gradient

            x = xpxl1 + 1
            while x <= x2:
                plot(x, int(intery), 1 - (intery - int(intery)))
                plot(x, int(intery) + 1, intery - int(intery))
                intery += gradient
                x += 1


    def intensity(self, value):
        """Вычисляет оттенок серого на основе значения."""
        gray = int(value * 255)
        return "#{:02x}{:02x}{:02x}".format(gray, gray, gray)

    def start_line(self, event):
        """Запоминает начальную точку линии."""
        self.start_x = event.x
        self.start_y = event.y

    def end_line(self, event):
        """Рисует линию, когда отпускается кнопка мыши."""
        self.canvas.delete("all")

        if self.start_x is not None and self.start_y is not None:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y

            if self.current_algorithm == "bresenham":
                self.bresenham(x1, y1, x2, y2)
            elif self.current_algorithm == "dda":
                self.dda(x1, y1, x2, y2)
            elif self.current_algorithm == "wu":
                self.wu(x1, y1, x2, y2)

            if self.debug_mode.get():
                self.draw_grid()

            self.start_x = None
            self.start_y = None

root = tk.Tk()
editor = SimpleEditor(root)
root.mainloop()
