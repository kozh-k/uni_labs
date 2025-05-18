import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, simpledialog
import math

class GraphicsEditor:
    def __init__(self, master):
        self.master = master
        master.title("Графический редактор")

        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)

        self.current_shape = "окружность"  # По умолчанию
        self.start_x = None
        self.start_y = None

        self.debug_mode = False  # Режим отладки
        self.grid_size = 20  # Размер ячейки сетки

        self.setup_toolbar()
        self.setup_menu()

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def setup_toolbar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопки для выбора фигур
        shapes = ["окружность", "эллипс", "гипербола", "парабола"]
        for shape in shapes:
            button = ttk.Button(self.toolbar, text=shape, command=lambda s=shape: self.set_shape(s))
            button.pack(side=tk.LEFT, padx=2, pady=2)

        # Кнопка для включения/выключения режима отладки
        self.debug_button = ttk.Button(self.toolbar, text="Режим отладки: Выкл", command=self.toggle_debug_mode)
        self.debug_button.pack(side=tk.LEFT, padx=2, pady=2)

    def setup_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Выход", command=self.master.quit)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        self.shape_menu = tk.Menu(self.menu_bar, tearoff=0)
        shapes = ["окружность", "эллипс", "гипербола", "парабола"]
        for shape in shapes:
            self.shape_menu.add_command(label=shape, command=lambda s=shape: self.set_shape(s))
        self.menu_bar.add_cascade(label="Линии второго порядка", menu=self.shape_menu)

        self.master.config(menu=self.menu_bar)

    def set_shape(self, shape):
        self.current_shape = shape
        print(f"Выбрана фигура: {shape}")

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.debug_button.config(text="Режим отладки: Вкл")
            print("Режим отладки включен")
            self.draw_grid()
        else:
            self.debug_button.config(text="Режим отладки: Выкл")
            print("Режим отладки выключен")
            self.canvas.delete("grid")
            self.canvas.config(bg="white")

    def draw_grid(self):
        self.canvas.config(bg="#f0f0f0")  # Светло-серый фон для сетки
        for i in range(0, self.canvas_width, self.grid_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill="gray", tags="grid")
        for j in range(0, self.canvas_height, self.grid_size):
            self.canvas.create_line(0, j, self.canvas_width, j, fill="gray", tags="grid")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.debug_mode:
            self.start_x = self.grid_size * round(self.start_x / self.grid_size)
            self.start_y = self.grid_size * round(self.start_y / self.grid_size)

    def on_mouse_up(self, event):
        end_x = event.x
        end_y = event.y

        if self.debug_mode:
            end_x = self.grid_size * round(end_x / self.grid_size)
            end_y = self.grid_size * round(end_y / self.grid_size)

        if self.current_shape == "окружность":
            radius = int(math.sqrt((end_x - self.start_x)**2 + (end_y - self.start_y)**2))
            self.draw_circle(self.start_x, self.start_y, radius)
        elif self.current_shape == "эллипс":
            self.get_ellipse_params(self.start_x, self.start_y, end_x, end_y)
        elif self.current_shape == "гипербола":
            self.get_hyperbola_params(self.start_x, self.start_y, end_x, end_y)
        elif self.current_shape == "парабола":
            self.get_parabola_params(self.start_x, self.start_y, end_x, end_y)

    def draw_pixel(self, x, y, color="black"):
        if self.debug_mode:
            x = self.grid_size * round(x / self.grid_size)
            y = self.grid_size * round(y / self.grid_size)
            x0 = x - self.grid_size // 2
            y0 = y - self.grid_size // 2
            x1 = x + self.grid_size // 2
            y1 = y + self.grid_size // 2
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
        else:
            self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)

    def draw_circle(self, center_x, center_y, radius):
        x = radius
        y = 0
        decision_over_2 = 1 - x   # Decision criterion divided by 2 evaluated at x=r, y=0

        while x >= y:
            self.draw_pixel(x + center_x, y + center_y)
            self.draw_pixel(y + center_x, x + center_y)
            self.draw_pixel(-x + center_x, y + center_y)
            self.draw_pixel(-y + center_x, x + center_y)
            self.draw_pixel(-x + center_x, -y + center_y)
            self.draw_pixel(-y + center_x, -x + center_y)
            self.draw_pixel(x + center_x, -y + center_y)
            self.draw_pixel(y + center_x, -x + center_y)
            y += 1
            if decision_over_2 <= 0:
                decision_over_2 += 2 * y + 1   # Change in decision criterion for y -> y+1
            else:
                x -= 1
                decision_over_2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1

    def get_ellipse_params(self, center_x, center_y, end_x, end_y):
        self.ellipse_window = tk.Toplevel(self.master)
        self.ellipse_window.title("Параметры эллипса")

        tk.Label(self.ellipse_window, text="Радиус по X:").grid(row=0, column=0, padx=5, pady=5)
        self.rx_entry = tk.Entry(self.ellipse_window)
        self.rx_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.ellipse_window, text="Радиус по Y:").grid(row=1, column=0, padx=5, pady=5)
        self.ry_entry = tk.Entry(self.ellipse_window)
        self.ry_entry.grid(row=1, column=1, padx=5, pady=5)

        ok_button = ttk.Button(self.ellipse_window, text="OK", command=lambda: self.draw_ellipse(
            center_x, center_y, int(self.rx_entry.get()), int(self.ry_entry.get())))
        ok_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def draw_ellipse(self, center_x, center_y, rx, ry):
        x = 0
        y = ry

        rx2 = rx * rx
        ry2 = ry * ry
        dx = 2 * ry2 * x
        dy = 2 * rx2 * y
        err = ry2 - rx2 * ry + rx2 / 4

        while dx < dy:
            self.draw_pixel(center_x + x, center_y + y)
            self.draw_pixel(center_x - x, center_y + y)
            self.draw_pixel(center_x + x, center_y - y)
            self.draw_pixel(center_x - x, center_y - y)

            if err < 0:
                x += 1
                dx = dx + 2 * ry2
                err = err + dx + ry2
            else:
                x += 1
                y -= 1
                dx = dx + 2 * ry2
                dy = dy - 2 * rx2
                err = err + dx - dy + ry2

        err = (x + 0.5) ** 2 * ry2 + (y - 1) ** 2 * rx2 - rx2 * ry2
        while y >= 0:
            self.draw_pixel(center_x + x, center_y + y)
            self.draw_pixel(center_x - x, center_y + y)
            self.draw_pixel(center_x + x, center_y - y)
            self.draw_pixel(center_x - x, center_y - y)

            if err > 0:
                y -= 1
                dy = dy - 2 * rx2
                err = err - dy + rx2
            else:
                x += 1
                y -= 1
                dx = dx + 2 * ry2
                dy = dy - 2 * rx2
                err = err + dx - dy + rx2

        if hasattr(self, 'ellipse_window') and self.ellipse_window.winfo_exists():
            self.ellipse_window.destroy()

    def get_hyperbola_params(self, center_x, center_y, end_x, end_y):
        self.hyperbola_window = tk.Toplevel(self.master)
        self.hyperbola_window.title("Параметры гиперболы")

        tk.Label(self.hyperbola_window, text="a:").grid(row=0, column=0, padx=5, pady=5)
        self.a_entry = tk.Entry(self.hyperbola_window)
        self.a_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.hyperbola_window, text="b:").grid(row=1, column=0, padx=5, pady=5)
        self.b_entry = tk.Entry(self.hyperbola_window)
        self.b_entry.grid(row=1, column=1, padx=5, pady=5)

        ok_button = ttk.Button(self.hyperbola_window, text="OK", command=lambda: self.draw_hyperbola(
            center_x, center_y, float(self.a_entry.get()), float(self.b_entry.get())))
        ok_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def draw_hyperbola(self, center_x, center_y, a, b):
        x = a
        y = 0
        while x < self.canvas_width and y < self.canvas_height:
            y = b * math.sqrt((x**2 / a**2) - 1)
            self.draw_pixel(int(center_x + x), int(center_y + y))
            self.draw_pixel(int(center_x - x), int(center_y + y))
            self.draw_pixel(int(center_x + x), int(center_y - y))
            self.draw_pixel(int(center_x - x), int(center_y - y))
            x += 0.1
        if hasattr(self, 'hyperbola_window') and self.hyperbola_window.winfo_exists():
            self.hyperbola_window.destroy()

    def get_parabola_params(self, center_x, center_y, end_x, end_y):
        self.parabola_window = tk.Toplevel(self.master)
        self.parabola_window.title("Параметры параболы")

        tk.Label(self.parabola_window, text="p:").grid(row=0, column=0, padx=5, pady=5)
        self.p_entry = tk.Entry(self.parabola_window)
        self.p_entry.grid(row=0, column=1, padx=5, pady=5)

        ok_button = ttk.Button(self.parabola_window, text="OK", command=lambda: self.draw_parabola(
            center_x, center_y, float(self.p_entry.get())))
        ok_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def draw_parabola(self, center_x, center_y, p):
        x = -self.canvas_width/2
        while x < self.canvas_width/2:
            y = x**2 / (2 * p)
            self.draw_pixel(int(center_x + x), int(center_y - y))
            x += 0.1
        if hasattr(self, 'parabola_window') and self.parabola_window.winfo_exists():
            self.parabola_window.destroy()

root = tk.Tk()
editor = GraphicsEditor(root)
root.mainloop()