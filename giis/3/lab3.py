import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np

HERMITE_MATRIX = np.array([
    [ 2, -2,  1,  1],
    [-3,  3, -2, -1],
    [ 0,  0,  1,  0],
    [ 1,  0,  0,  0]
])

BEZIER_MATRIX = np.array([
    [-1,  3, -3,  1],
    [ 3, -6,  3,  0],
    [-3,  3,  0,  0],
    [ 1,  0,  0,  0]
])

BSPLINE_MATRIX = (1/6) * np.array([
    [-1,  3, -3,  1],
    [ 3, -6,  3,  0],
    [-3,  0,  3,  0],
    [ 1,  4,  1,  0]
])

HERMITE = "Эрмит"
BEZIER = "Безье"
BSPLINE = "B-Сплайн"

class CurveEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор Кривых")
        self.geometry("800x600")
        self.current_curve_type = tk.StringVar(value=BEZIER)
        self.is_editing = tk.BooleanVar(value=False)
        self.control_points = []
        self.drawn_curves = []
        self.selected_point_info = None
        self.drag_start_pos = None
        self._create_menu()
        self._create_toolbar()
        self._create_canvas()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.status_bar = tk.Label(self, text="Режим: Рисование | Тип: Безье | Кликните для добавления точек.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status_bar()

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Очистить всё", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        curve_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Тип кривой", menu=curve_menu)
        curve_menu.add_radiobutton(label="Эрмит", variable=self.current_curve_type, value=HERMITE, command=self.on_curve_type_change)
        curve_menu.add_radiobutton(label="Безье", variable=self.current_curve_type, value=BEZIER, command=self.on_curve_type_change)
        curve_menu.add_radiobutton(label="B-Сплайн", variable=self.current_curve_type, value=BSPLINE, command=self.on_curve_type_change)
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_checkbutton(label="Режим Редактирования", variable=self.is_editing, command=self.toggle_edit_mode)

    def _create_toolbar(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        hermite_btn = tk.Radiobutton(toolbar, text="Эрмит", variable=self.current_curve_type, value=HERMITE, indicatoron=0, command=self.on_curve_type_change, width=10)
        bezier_btn = tk.Radiobutton(toolbar, text="Безье", variable=self.current_curve_type, value=BEZIER, indicatoron=0, command=self.on_curve_type_change, width=10)
        bspline_btn = tk.Radiobutton(toolbar, text="B-Сплайн", variable=self.current_curve_type, value=BSPLINE, indicatoron=0, command=self.on_curve_type_change, width=10)
        edit_btn = tk.Checkbutton(toolbar, text="Редакт.", variable=self.is_editing, indicatoron=0, command=self.toggle_edit_mode, width=10)
        clear_btn = tk.Button(toolbar, text="Очистить", command=self.clear_canvas, width=10)
        hermite_btn.pack(side=tk.LEFT, padx=2, pady=2)
        bezier_btn.pack(side=tk.LEFT, padx=2, pady=2)
        bspline_btn.pack(side=tk.LEFT, padx=2, pady=2)
        edit_btn.pack(side=tk.LEFT, padx=5, pady=2)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white", relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def update_status_bar(self):
        mode_text = "Редактирование" if self.is_editing.get() else "Рисование"
        curve_type = self.current_curve_type.get()
        points_needed = self.get_points_needed(curve_type)
        points_have = len(self.control_points)
        status = f"Режим: {mode_text} | Тип: {curve_type} | "
        if self.is_editing.get():
            status += "Кликните рядом с контрольной точкой для выбора и перетаскивания."
        else:
            status += f"Кликните для добавления точек ({points_have}/{points_needed} для текущего сегмента)."
        self.status_bar.config(text=status)

    def get_points_needed(self, curve_type):
        return 4

    def on_curve_type_change(self):
        if len(self.control_points) > 0 and not self.is_editing.get():
            self.clear_current_points()
            messagebox.showinfo("Тип кривой изменен", "Текущие точки для рисования очищены.")
        self.update_status_bar()

    def toggle_edit_mode(self):
        if len(self.control_points) > 0:
            self.clear_current_points()
        self.selected_point_info = None
        self.update_status_bar()
        self.redraw_canvas()

    def clear_canvas(self):
        if messagebox.askyesno("Подтверждение", "Очистить все рисунки и точки?"):
            self.canvas.delete("all")
            self.control_points = []
            self.drawn_curves = []
            self.selected_point_info = None
            self.update_status_bar()

    def clear_current_points(self):
        for point_info in self.control_points:
            if 'id' in point_info and point_info['id'] is not None:
                try:
                    self.canvas.delete(point_info['id'])
                except tk.TclError:
                    pass
        self.control_points = []
        self.update_status_bar()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        if self.is_editing.get():
            if self.selected_point_info:
                prev_point_id = self.selected_point_info['canvas_id']
                if self.canvas.winfo_exists() and prev_point_id in self.canvas.find_all():
                    try:
                        self.canvas.itemconfig(prev_point_id, fill="green", outline="black")
                    except tk.TclError:
                        pass
            self.selected_point_info = self.find_nearby_control_point(x, y)
            if self.selected_point_info:
                self.drag_start_pos = (x, y)
                point_id = self.selected_point_info['canvas_id']
                if self.canvas.winfo_exists() and point_id in self.canvas.find_all():
                    try:
                        self.canvas.itemconfig(point_id, fill="red", outline="red")
                    except tk.TclError:
                        pass
        else:
            points_needed = self.get_points_needed(self.current_curve_type.get())
            point_id = self.draw_control_point(x, y, "blue")
            self.control_points.append({'x': x, 'y': y, 'id': point_id})
            if len(self.control_points) == points_needed:
                self.finalize_curve_segment()
            self.update_status_bar()

    def on_canvas_drag(self, event):
        if self.is_editing.get() and self.selected_point_info and self.drag_start_pos:
            dx = event.x - self.drag_start_pos[0]
            dy = event.y - self.drag_start_pos[1]
            curve_idx = self.selected_point_info['curve_index']
            point_idx = self.selected_point_info['point_index']
            point_id = self.selected_point_info['canvas_id']
            if self.canvas.winfo_exists() and point_id in self.canvas.find_all():
                self.canvas.move(point_id, dx, dy)
            else:
                self.selected_point_info = None
                self.drag_start_pos = None
                return
            new_x, new_y = self.drawn_curves[curve_idx]['points'][point_idx][0] + dx, self.drawn_curves[curve_idx]['points'][point_idx][1] + dy
            self.drawn_curves[curve_idx]['points'][point_idx] = (new_x, new_y)
            self.drag_start_pos = (event.x, event.y)
            self.redraw_specific_curve(curve_idx)

    def on_canvas_release(self, event):
        if self.is_editing.get() and self.selected_point_info:
            point_id = self.selected_point_info['canvas_id']
            if self.canvas.winfo_exists() and point_id in self.canvas.find_all():
                try:
                    self.canvas.itemconfig(point_id, fill="green", outline="black")
                except tk.TclError:
                    pass
        self.drag_start_pos = None

    def find_nearby_control_point(self, x, y, tolerance=10):
        for curve_index in range(len(self.drawn_curves) - 1, -1, -1):
            curve = self.drawn_curves[curve_index]
            for point_index in range(len(curve['points']) - 1, -1, -1):
                px, py = curve['points'][point_index]
                point_id = curve['point_ids'][point_index]
                dist_sq = (x - px)**2 + (y - py)**2
                if dist_sq < tolerance**2:
                    if self.canvas.winfo_exists() and point_id in self.canvas.find_all():
                        return {
                            'curve_index': curve_index,
                            'point_index': point_index,
                            'canvas_id': point_id
                        }
        return None

    def redraw_specific_curve(self, curve_index):
        if curve_index < 0 or curve_index >= len(self.drawn_curves):
            return
        curve_data = self.drawn_curves[curve_index]
        control_points_coords = curve_data['points']
        curve_type = curve_data['type']
        curve_id = curve_data.get('id')
        point_ids = curve_data.get('point_ids', [])
        if len(control_points_coords) < self.get_points_needed(curve_type):
            if curve_id and self.canvas.winfo_exists() and curve_id in self.canvas.find_all():
                self.canvas.delete(curve_id)
                curve_data['id'] = None
            return
        try:
            curve_plot_points = self.calculate_curve_points(control_points_coords, curve_type)
        except Exception as e:
            if curve_id and self.canvas.winfo_exists() and curve_id in self.canvas.find_all():
                self.canvas.delete(curve_id)
                curve_data['id'] = None
            return
        if curve_plot_points and len(curve_plot_points) > 1:
            if curve_id and self.canvas.winfo_exists() and curve_id in self.canvas.find_all():
                flat_points = [coord for point in curve_plot_points for coord in point]
                try:
                    self.canvas.coords(curve_id, *flat_points)
                except tk.TclError:
                    curve_data['id'] = None
                    new_id = self.canvas.create_line(curve_plot_points, fill="black", width=2, tags=("curve", f"curve_{curve_index}"))
                    curve_data['id'] = new_id
            else:
                new_id = self.canvas.create_line(curve_plot_points, fill="black", width=2, tags=("curve", f"curve_{curve_index}"))
                curve_data['id'] = new_id
            for point_id in point_ids:
                if point_id and self.canvas.winfo_exists() and point_id in self.canvas.find_all():
                    self.canvas.tag_raise(point_id)
        elif curve_id and self.canvas.winfo_exists() and curve_id in self.canvas.find_all():
            self.canvas.delete(curve_id)
            curve_data['id'] = None

    def redraw_canvas(self):
        self.canvas.delete("curve")
        self.canvas.delete("control_point")
        point_color = "green" if self.is_editing.get() else "blue"
        point_outline = "black"
        for curve_index, curve in enumerate(self.drawn_curves):
            new_point_ids = []
            points_coords = curve.get('points', [])
            if len(points_coords) < self.get_points_needed(curve.get('type', BEZIER)):
                curve['point_ids'] = []
                curve['id'] = None
                continue
            for i, (px, py) in enumerate(points_coords):
                current_point_color = point_color
                current_point_outline = point_outline
                if self.is_editing.get() and self.selected_point_info and \
                   self.selected_point_info['curve_index'] == curve_index and \
                   self.selected_point_info['point_index'] == i:
                    current_point_color = "red"
                    current_point_outline = "red"
                pid = self.draw_control_point(px, py, current_point_color, current_point_outline, tags=("control_point", f"curve_{curve_index}", f"point_{curve_index}_{i}"))
                new_point_ids.append(pid)
            curve['point_ids'] = new_point_ids
            try:
                plot_points = self.calculate_curve_points(curve['points'], curve['type'])
                if plot_points and len(plot_points) > 1:
                    curve_id = self.canvas.create_line(plot_points, fill="black", width=2, tags=("curve", f"curve_{curve_index}"))
                    curve['id'] = curve_id
                else:
                    curve['id'] = None
            except Exception as e:
                curve['id'] = None

        if not self.is_editing.get():
            for i, p in enumerate(self.control_points):
                new_id = self.draw_control_point(p['x'], p['y'], "blue", "black", tags="control_point")
                self.control_points[i]['id'] = new_id

    def on_canvas_resize(self, event):
        pass

    def draw_control_point(self, x, y, color="blue", outline="black", radius=3, tags=()):
        x1, y1 = x - radius, y - radius
        x2, y2 = x + radius, y + radius
        point_id = self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, tags=tags)
        return point_id

    def finalize_curve_segment(self):
        if not self.control_points:
            return
        curve_type = self.current_curve_type.get()
        points_needed = self.get_points_needed(curve_type)
        if len(self.control_points) < points_needed:
            return
        current_segment_points_data = list(self.control_points)
        current_segment_points_coords = [(p['x'], p['y']) for p in current_segment_points_data]
        try:
            plot_points = self.calculate_curve_points(current_segment_points_coords, curve_type)
        except Exception as e:
            messagebox.showerror("Ошибка вычисления", f"Не удалось рассчитать точки кривой: {e}")
            self.clear_current_points()
            return
        if plot_points and len(plot_points) > 1:
            curve_id = self.canvas.create_line(plot_points, fill="black", width=2, tags="curve")
            point_ids = [p['id'] for p in current_segment_points_data]
            self.drawn_curves.append({
                'id': curve_id,
                'points': current_segment_points_coords,
                'type': curve_type,
                'point_ids': point_ids
            })
            if curve_type == BSPLINE:
                if len(current_segment_points_data) > 0 and current_segment_points_data[0]['id'] is not None:
                    try:
                        self.canvas.delete(current_segment_points_data[0]['id'])
                    except tk.TclError:
                        pass
                self.control_points = current_segment_points_data[1:]
                for i in range(len(self.control_points)):
                    self.control_points[i]['id'] = point_ids[i + 1]
            elif curve_type == BEZIER or curve_type == HERMITE:
                self.control_points = []
            self.update_status_bar()
        else:
            messagebox.showwarning("Предупреждение", "Сегмент кривой не содержит точек для рисования.")
            self.clear_current_points()


    def calculate_curve_points(self, control_points_coords, curve_type, num_steps=50):
        n_points = len(control_points_coords)
        points_needed = self.get_points_needed(curve_type)
        if n_points < points_needed:
            return []
        G_raw = np.array(control_points_coords[:points_needed])
        matrix = None
        G = G_raw
        if curve_type == HERMITE:
            matrix = HERMITE_MATRIX
            P0 = G_raw[0]
            P1 = G_raw[1]
            P2 = G_raw[2]
            P3 = G_raw[3]
            tangent_scale = 1.0
            T0 = tangent_scale * (P1 - P0)
            T1 = tangent_scale * (P3 - P2)
            G_hermite = np.array([P0, P3, T0, T1])
            G = G_hermite
        elif curve_type == BEZIER:
            matrix = BEZIER_MATRIX
        elif curve_type == BSPLINE:
            matrix = BSPLINE_MATRIX
        else:
            raise ValueError(f"Неизвестный тип кривой: {curve_type}")
        if G.shape != (4, 2):
            raise ValueError(f"Вектор геометрии G имеет неожиданную форму: {G.shape}. Ожидалась (4, 2).")
        plot_points = []
        for i in range(num_steps + 1):
            t = i / num_steps
            T = np.array([t**3, t**2, t, 1])
            calculated_point = T @ matrix @ G
            plot_points.append(tuple(calculated_point))
        return plot_points

if __name__ == "__main__":
    app = CurveEditor()
    app.mainloop()
