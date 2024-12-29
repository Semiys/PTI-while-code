import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np

class CyclicCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Изучение циклических кодов")
        
        # Устанавливаем полноэкранный режим
        self.root.state('zoomed')  # для Windows
        # Альтернатива для Linux/Mac:
        # self.root.attributes('-zoomed', True)
        
        # Создание основных фреймов
        self.create_frames()
        # Создание элементов управления
        self.create_controls()
        
    def create_frames(self):
        # Левая панель для ввода данных
        self.input_frame = ttk.LabelFrame(self.root, text="Входные данные", padding=10)
        self.input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Центральная панель для отображения шагов
        self.steps_frame = ttk.LabelFrame(self.root, text="Пошаговое выполнение", padding=10)
        self.steps_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # Правая панель для результатов
        self.result_frame = ttk.LabelFrame(self.root, text="Результаты", padding=10)
        self.result_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        # Настройка весов колонок
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_controls(self):
        # Элементы ввода данных
        ttk.Label(self.input_frame, text="Введите сообщение (двоичный код):").pack(anchor="w")
        self.message_entry = ttk.Entry(self.input_frame)
        self.message_entry.pack(fill="x", pady=5)
        
        ttk.Label(self.input_frame, text="Выберите или введите порождающий полином:").pack(anchor="w")
        
        # Создаем frame для полиномов
        poly_frame = ttk.Frame(self.input_frame)
        poly_frame.pack(fill="x", pady=5)
        
        # Переменная для хранения способа ввода полинома
        self.poly_input_mode = tk.StringVar(value="preset")
        
        # Радиокнопки для выбора способа ввода полинома
        ttk.Radiobutton(poly_frame, text="Готовые полиномы", 
                       variable=self.poly_input_mode, value="preset",
                       command=self.switch_polynomial_input).pack(anchor="w")
        ttk.Radiobutton(poly_frame, text="Свой полином", 
                       variable=self.poly_input_mode, value="custom",
                       command=self.switch_polynomial_input).pack(anchor="w")
        
        # Комбобокс с готовыми полиномами
        self.polynomial_var = tk.StringVar()
        polynomials = [
            "x + 1",
            "x² + x + 1",
            "x³ + x + 1",
            "x³ + x² + 1",
            "x⁴ + x + 1",
            "x⁴ + x³ + 1",
            "x⁵ + x² + 1",
            "x⁵ + x³ + 1",
            "x⁶ + x + 1",
            "x⁷ + x³ + 1",
            "x⁸ + x⁴ + x³ + x² + 1",
            "x⁹ + x⁴ + 1",
            "x¹⁰ + x³ + 1"
        ]
        self.polynomial_combo = ttk.Combobox(poly_frame, textvariable=self.polynomial_var, 
                                           values=polynomials, state="readonly")
        self.polynomial_combo.pack(fill="x", pady=5)
        self.polynomial_combo.set(polynomials[2])  # По умолчанию x³ + x + 1
        
        # Поле для ввода своего полинома
        ttk.Label(poly_frame, text="Введите двоичное представление полинома:").pack(anchor="w")
        self.custom_poly_entry = ttk.Entry(poly_frame)
        self.custom_poly_entry.pack(fill="x", pady=5)
        self.custom_poly_entry.config(state="disabled")
        
        # Кнопки управления
        ttk.Button(self.input_frame, text="Начать кодирование", 
                  command=self.start_encoding).pack(fill="x", pady=5)
        ttk.Button(self.input_frame, text="Проверить на ошибки", 
                  command=self.check_errors).pack(fill="x", pady=5)
        ttk.Button(self.input_frame, text="Сохранить результаты", 
                  command=self.save_results).pack(fill="x", pady=5)
        
        # Кнопка для внесения ошибок
        ttk.Button(self.input_frame, text="Внести ошибку", 
                  command=self.introduce_error).pack(fill="x", pady=5)
        
        # Область для пошагового отображения
        self.steps_text = tk.Text(self.steps_frame, wrap=tk.WORD, width=50, height=30)
        self.steps_text.pack(fill="both", expand=True)
        
        # Область результатов
        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD, width=30, height=30)
        self.result_text.pack(fill="both", expand=True)
        
        # Добавим скроллбар для текстовых областей
        steps_scroll = ttk.Scrollbar(self.steps_frame)
        steps_scroll.pack(side="right", fill="y")
        self.steps_text.config(yscrollcommand=steps_scroll.set)
        steps_scroll.config(command=self.steps_text.yview)
        
        result_scroll = ttk.Scrollbar(self.result_frame)
        result_scroll.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=result_scroll.set)
        result_scroll.config(command=self.result_text.yview)
        
        # Добавляем фрейм для примеров
        example_frame = ttk.LabelFrame(self.input_frame, text="Примеры", padding=5)
        example_frame.pack(fill="x", pady=5)
        
        ttk.Button(example_frame, text="Пример 1: Простое кодирование", 
                  command=lambda: self.load_example(1)).pack(fill="x", pady=2)
        ttk.Button(example_frame, text="Пример 2: Обнаружение ошибки", 
                  command=lambda: self.load_example(2)).pack(fill="x", pady=2)
        ttk.Button(example_frame, text="Пример 3: Исправление ошибки", 
                  command=lambda: self.load_example(3)).pack(fill="x", pady=2)
        
        # Добавляем кнопку для пошагового выполнения
        self.step_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.input_frame, text="Пошаговое выполнение", 
                       variable=self.step_var).pack(anchor="w", pady=5)
        
        self.next_step_button = ttk.Button(self.input_frame, text="Следующий шаг →", 
                                         command=self.next_step, state="disabled")
        self.next_step_button.pack(fill="x", pady=5)
        
        ttk.Label(poly_frame, text="Примеры примитивных полиномов:\n" +
                  "11 (x + 1)\n" +
                  "111 (x² + x + 1)\n" +
                  "1011 (x³ + x + 1)\n" +
                  "1101 (x³ + x² + 1)\n" +
                  "10011 (x⁴ + x + 1)\n" +
                  "11001 (x⁴ + x³ + 1)\n" +
                  "100101 (x⁵ + x² + 1)\n" +
                  "101001 (x⁵ + x³ + 1)\n" +
                  "1000011 (x⁶ + x + 1)\n" +
                  "10001001 (x⁷ + x³ + 1)",
                  justify="left").pack(anchor="w", pady=5)
        
        # Добавляем кнопку выхода в нижней части input_frame
        exit_button = ttk.Button(
            self.input_frame,
            text="Выход",
            command=self.root.destroy
        )
        exit_button.pack(fill="x", pady=5)  # Такой же отступ, как у других кнопок
        
        # Создаем более заметный стиль для кнопки выхода
        style = ttk.Style()
        style.configure('Exit.TButton', 
                       font=('Arial', 12, 'bold'),
                       padding=10,
                       background='#FF4444',  # Яркий красный цвет
                       foreground='white',
                       borderwidth=3,
                       relief='raised')
        
        # Добавляем эффекты при наведении и нажатии
        style.map('Exit.TButton',
                  background=[('active', '#FF0000'),  # Более темный красный при наведении
                             ('pressed', '#CC0000')], # Еще более темный при нажатии
                  foreground=[('active', 'white'),
                             ('pressed', 'white')])

    def polynomial_to_binary(self, poly_str):
        """Преобразует строковое представление полинома в двоичный массив"""
        try:
            # Удаляем пробелы и приводим к нижнему регистру
            poly_str = poly_str.replace(" ", "").lower()
            
            # Если это уже двоичное число
            if all(c in '01' for c in poly_str):
                result = [int(bit) for bit in poly_str]
                # Удаляем ведущие нули
                while len(result) > 1 and result[0] == 0:
                    result.pop(0)
                return result
            
            # Словарь примитивных полиномов
            primitive_polynomials = {
                "x+1": [1, 1],                    # x + 1
                "x²+x+1": [1, 1, 1],             # x² + x + 1
                "x³+x+1": [1, 0, 1, 1],          # x³ + x + 1
                "x³+x²+1": [1, 1, 0, 1],         # x³ + x² + 1
                "x⁴+x+1": [1, 0, 0, 1, 1],       # x⁴ + x + 1
                "x⁴+x³+1": [1, 1, 0, 0, 1],      # x⁴ + x³ + 1
                "x⁵+x²+1": [1, 0, 0, 1, 0, 1],   # x⁵ + x² + 1
                "x⁵+x³+1": [1, 0, 1, 0, 0, 1],   # x⁵ + x³ + 1
                "x⁶+x+1": [1, 0, 0, 0, 0, 1, 1], # x⁶ + x + 1
                "x⁷+x³+1": [1, 0, 0, 0, 1, 0, 0, 1], # x⁷ + x³ + 1
                "x⁸+x⁴+x³+x²+1": [1, 0, 0, 0, 1, 1, 1, 0, 1], # x⁸ + x⁴ + x³ + x² + 1
                "x⁹+x⁴+1": [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],    # x⁹ + x⁴ + 1
                "x¹⁰+x³+1": [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]  # x¹⁰ + x³ + 1
            }
            
            # Нормализация строки для сравнения
            normalized_str = poly_str.replace("^", "").replace(" ", "")
            
            # Поиск полинома в словаре
            for key, value in primitive_polynomials.items():
                if key.replace("^", "").replace(" ", "") == normalized_str:
                    return value
            
            # Если полином не распознан, возвращаем полином по умолчанию
            print(f"Неизвестный формат полинома: {poly_str}")
            return [1, 0, 1, 1]  # x³ + x + 1 по умолчанию
            
        except Exception as e:
            print(f"Ошибка в polynomial_to_binary: {str(e)}")
            return [1, 0, 1, 1]  # возвращаем x³ + x + 1 по умолчанию

    def polynomial_division(self, dividend, divisor):
        """
        Выполняет деление полиномов в GF(2)
        dividend: список коэффициентов делимого полинома
        divisor: список коэффициентов делителя
        """
        try:
            # Создаем рабочую копию делимого
            working = list(dividend)
            n = len(working)
            m = len(divisor)
            steps = []
            steps.append(f"Начальное делимое: {working}")
            
            # Проходим по всем битам делимого до тех пор, пока не останется остаток нужной длины
            for i in range(n - m + 1):
                if working[i] == 1:  # Если текущий бит 1
                    steps.append(f"Деление на позиции {i}")
                    # Выполняем XOR с делителем на текущей позиции
                    for j in range(m):
                        working[i + j] ^= divisor[j]
                    steps.append(f"Промежуточный результат: {working}")
                    steps.append(f"XOR на позиции {i}: {divisor} с {working[i:i+m]}")
            
            # Получаем остаток (последние m-1 бит)
            remainder = working[-(m-1):]
            
            # Проверяем корректность деления
            quotient_part = working[:-(m-1)]
            if any(bit == 1 for bit in quotient_part):
                steps.append(f"Внимание: остались ненулевые биты перед остатком: {quotient_part}")
            
            steps.append(f"Финальный остаток: {remainder}")
            return remainder, steps
            
        except Exception as e:
            print(f"Ошибка в polynomial_division: {str(e)}")
            return [], [f"Ошибка при делении: {str(e)}"]

    def format_polynomial(self, coefficients):
        """Форматирует массив коэффициентов в читаемый вид полинома"""
        terms = []
        for i, coef in enumerate(coefficients):
            if coef == 1:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        return " + ".join(reversed(terms)) if terms else "0"

    def start_encoding(self):
        try:
            if not self.validate_input():
                return
            
            # Если включен пошаговый режим
            if self.step_var.get():
                self.current_step = 0
                self.next_step_button.config(state="normal")
                self.next_step()
                return
            
            # Обычный режим - выполняем все сразу
            message = self.message_entry.get()
            message_bits = [int(bit) for bit in message]
            generator_poly = self.get_generator_polynomial()
            
            # Добавляем нули к сообщению
            augmented_message = message_bits + [0] * (len(generator_poly) - 1)
            
            # Выполняем деление
            remainder, steps = self.polynomial_division(augmented_message, generator_poly)
            
            # Формируем закодированное сообщение
            encoded_message = message_bits + remainder
            
            # Выводим результаты
            self.display_results(message_bits, generator_poly, steps, encoded_message)
            
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def check_errors(self):
        try:
            # Получаем закодированное сообщение из области результатов
            encoded_message = self.result_text.get("2.0", "2.end").strip()
            if not encoded_message:
                messagebox.showerror("Ошибка", "Сначала закодируйте сообщение!")
                return
                
            if not self.validate_binary_input(encoded_message):
                messagebox.showerror("Ошибка", "Некорректное закодированное сообщение!")
                return
                
            generator_poly_str = self.polynomial_var.get()
            if not generator_poly_str:
                messagebox.showerror("Ошибка", "Выберите порождающий полином!")
                return
                
            generator_poly = self.polynomial_to_binary(generator_poly_str)
            message_bits = [int(bit) for bit in encoded_message]
            
            # Выполняем деление на порождающий полином
            remainder, division_steps = self.polynomial_division(message_bits, generator_poly)
            
            self.steps_text.delete(1.0, tk.END)
            self.steps_text.insert(tk.END, "Проверка на наличие ошибок:\n\n")
            self.steps_text.insert(tk.END, f"1. Проверяемое сообщение: {encoded_message}\n")
            self.steps_text.insert(tk.END, f"2. Порождающий полином: {generator_poly_str}\n\n")
            self.steps_text.insert(tk.END, "3. Процесс проверки:\n")
            
            for step in division_steps:
                self.steps_text.insert(tk.END, f"   {step}\n")
            
            # Проверяем остаток
            has_error = False
            if remainder and any(bit == 1 for bit in remainder):
                has_error = True
            
            self.steps_text.insert(tk.END, f"\n4. Остаток от деления: {remainder}\n")
            
            if has_error:
                self.steps_text.insert(tk.END, "\nОбнаружена ошибка в сообщении!")
                self.result_text.insert(tk.END, "\nРезультат проверки: Сообщение содержит ошибки\n")
            else:
                self.steps_text.insert(tk.END, "\nОшибок не обнаружено")
                self.result_text.insert(tk.END, "\nРезультат проверки: Сообщение корректно\n")
                
        except Exception as e:
            print(f"Ошибка в check_errors: {str(e)}")  # для отладки
            messagebox.showerror("Ошибка", f"Произошла ошибка при проверке: {str(e)}")

    def save_results(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.steps_text.get(1.0, tk.END))
                file.write("\n\nРезультаты:\n")
                file.write(self.result_text.get(1.0, tk.END))
                
    def validate_binary_input(self, input_str):
        """Проверяет, что входная строка содержит только 0 и 1"""
        if not input_str:  # Проверка на пустую строку
            return False
        return all(bit in '01' for bit in input_str)

    def show_theory(self):
        """Показывает теоретическую справку"""
        theory_window = tk.Toplevel(self.root)
        theory_window.title("Теоретическая справка")
        theory_window.geometry("600x400")
        
        text = tk.Text(theory_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill="both", expand=True)
        
        theory_text = """
Циклические коды - это подкласс линейных блочных кодов, обладающих следующими свойствами:

1. Циклический сдвиг кодового слова также является кодовым словом.
2. Кодирование выполняется с помощью порождающего полинома g(x).
3. Процесс кодирования:
   - Исходное сообщение умножается на x^(n-k)
   - Результат делится на порождающий полином
   - Остаток от деления добавляется к сдвинутому сообщению

Порождающий полином должен быть неприводимым и иметь степень, равную количеству проверочных символов.
"""
        text.insert(1.0, theory_text)
        text.config(state="disabled")

    def introduce_error(self):
        """Вносит случайную ошибку в закодированное сообщение"""
        current_message = self.result_text.get("2.0", "2.end").strip()
        if not current_message:
            messagebox.showerror("Ошибка", "Сначала закодируйте сообщение!")
            return
            
        message_list = list(current_message)
        import random
        error_pos = random.randint(0, len(message_list)-1)
        message_list[error_pos] = '1' if message_list[error_pos] == '0' else '0'
        
        # Очищаем область результатов и записываем сообщение с ошибкой
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Закодированное сообщение:\n")
        self.result_text.insert(tk.END, f"{''.join(message_list)}\n")
        
        # Добавляем информацию об ошибке
        self.steps_text.insert(tk.END, f"\nВнесена ошибка в позиции {error_pos + 1}\n")
        self.result_text.insert(tk.END, f"\nСообщение с ошибкой:\n{''.join(message_list)}\n")

    def load_example(self, example_num):
        """Загружает предстановленные примеры"""
        examples = {
            1: {
                'message': '1011',
                'polynomial': 'x³ + x + 1',
                'description': 'Простой пример кодирования сообщения 1011'
            },
            2: {
                'message': '1101',
                'polynomial': 'x⁴ + x + 1',
                'description': 'Пример с внесением и обнаружением одиночной ошибки'
            },
            3: {
                'message': '11010',
                'polynomial': 'x⁷ + x³ + 1',
                'description': 'Пример с исправлением ошибки'
            }
        }
        
        example = examples.get(example_num)
        if example:
            self.message_entry.delete(0, tk.END)
            self.message_entry.insert(0, example['message'])
            self.polynomial_var.set(example['polynomial'])
            
            self.steps_text.delete(1.0, tk.END)
            self.result_text.delete(1.0, tk.END)
            self.steps_text.insert(tk.END, f"Загружен пример {example_num}:\n{example['description']}\n\n")

    def next_step(self):
        """Выполняет следующий шаг в пошаговом режиме"""
        if not hasattr(self, 'current_step'):
            self.current_step = 0
        
        self.current_step += 1
        
        # Получаем данные для кодирования
        message = self.message_entry.get()
        message_bits = [int(bit) for bit in message]
        generator_poly = self.get_generator_polynomial()
        augmented_message = message_bits + [0] * (len(generator_poly) - 1)
        
        # Очищаем текстовые поля при первом шаге
        if self.current_step == 1:
            self.steps_text.delete(1.0, tk.END)
            self.result_text.delete(1.0, tk.END)
        
        if self.current_step == 1:
            # Шаг 1: Анализ входных данных
            self.steps_text.insert(tk.END, "Шаг 1: Анализ входных данных\n\n")
            self.steps_text.insert(tk.END, f"• Исходное сообщение: {message}\n")
            self.steps_text.insert(tk.END, f"• Длина сообщения: {len(message)} бит\n")
            poly_str = self.format_polynomial(message_bits)
            self.steps_text.insert(tk.END, f"• Полиномиальное представление: {poly_str}\n")
            
        elif self.current_step == 2:
            # Шаг 2: Анализ порождающего полинома
            self.steps_text.insert(tk.END, "\nШаг 2: Анализ порождающего полинома\n\n")
            self.steps_text.insert(tk.END, f"• Порождающий полином: {self.polynomial_var.get()}\n")
            self.steps_text.insert(tk.END, f"• Двоичное представление: {generator_poly}\n")
            
        elif self.current_step == 3:
            # Шаг 3: Подготовка к делению
            self.steps_text.insert(tk.END, "\nШаг 3: Подготовка к делению\n\n")
            self.steps_text.insert(tk.END, f"• Добавление {len(generator_poly)-1} нулей к сообщению\n")
            self.steps_text.insert(tk.END, f"• Расширенное сообщение: {augmented_message}\n")
            
        elif self.current_step == 4:
            # Шаг 4: Выполнение деления
            remainder, steps = self.polynomial_division(augmented_message, generator_poly)
            self.steps_text.insert(tk.END, "\nШаг 4: Процесс деления\n\n")
            for step in steps:
                self.steps_text.insert(tk.END, f"• {step}\n")
            
        elif self.current_step == 5:
            # Шаг 5: Финальный результат
            remainder, _ = self.polynomial_division(augmented_message, generator_poly)
            encoded_message = message_bits + remainder
            self.steps_text.insert(tk.END, "\nШаг 5: Финальный результат\n\n")
            self.steps_text.insert(tk.END, f"• Контрольные биты: {remainder}\n")
            self.steps_text.insert(tk.END, f"• Закодированное сообщение: {encoded_message}\n")
            
            # Обновляем область результатов
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Закодированное сообщение:\n")
            self.result_text.insert(tk.END, f"{''.join(map(str, encoded_message))}\n")
            
            # Отключаем кнопку следующего шага
            self.next_step_button.config(state="disabled")
            self.current_step = 0
            return
        
        # Активируем кнопку следующего шага
        self.next_step_button.config(state="normal")

    def switch_polynomial_input(self):
        """Переключает между готовыми полиномами и пользовательским вводом"""
        if self.poly_input_mode.get() == "preset":
            self.polynomial_combo.config(state="normal")
            self.custom_poly_entry.config(state="disabled")
        else:
            self.polynomial_combo.config(state="disabled")
            self.custom_poly_entry.config(state="normal")

    def validate_polynomial(self, polynomial):
        """
        Проверяет корректность полинома
        polynomial: список коэффициентов полинома или строка
        Возвращает: (bool, str) - (валиден ли полином, сообщение об ошибке)
        """
        try:
            # Если передана строка, преобразуем её в список
            if isinstance(polynomial, str):
                polynomial = [int(bit) for bit in polynomial]
            
            if polynomial is None:
                return False, "Полином не может быть None"
            
            if not polynomial:
                return False, "Полином не может быть пустым"
            
            if len(polynomial) < 2:
                return False, "Полином должен иметь степень не менее 1"
            
            # Проверяем, что все элементы - биты
            if not all(bit in (0, 1) for bit in polynomial):
                return False, "Полином должен содержать только биты (0 или 1)"
            
            # Проверяем первый бит сразу
            if polynomial[0] != 1:
                return False, "Старший коэффициент должен быть равен 1"
            
            return True, ""
            
        except Exception as e:
            return False, f"Ошибка при валидации полинома: {str(e)}"

    def get_generator_polynomial(self):
        """Получает порождающий полином в зависимости от выбранного режима"""
        if self.poly_input_mode.get() == "preset":
            return self.polynomial_to_binary(self.polynomial_var.get())
        else:
            poly_str = self.custom_poly_entry.get().strip()
            is_valid, error_msg = self.validate_polynomial(poly_str)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Преобразуем в список битов и удаляем ведущие нули
            poly = [int(bit) for bit in poly_str]
            while len(poly) > 1 and poly[0] == 0:
                poly.pop(0)
            
            return poly

    def is_primitive_polynomial(self, poly):
        """
        Проверяет, является ли полином примитивным
        """
        # Словарь известных примитивных полиномов
        primitive_polynomials = {
            2: [[1, 1]],                    # x + 1
            3: [[1, 1, 1]],                # x² + x + 1
            4: [[1, 0, 1, 1], [1, 1, 0, 1]], # x³ + x + 1, x³ + x² + 1
            5: [[1, 0, 0, 1, 1], [1, 1, 0, 0, 1]], # x⁴ + x + 1, x⁴ + x³ + 1
            6: [[1, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 1]], # x⁵ + x² + 1, x⁵ + x³ + 1
            7: [[1, 0, 0, 0, 0, 1, 1]], # x⁶ + x + 1
            8: [[1, 0, 0, 0, 1, 0, 0, 1]], # x⁷ + x³ + 1
            9: [[1, 0, 0, 0, 1, 1, 1, 0, 1]], # x⁸ + x⁴ + x³ + x² + 1
            10: [[1, 0, 0, 0, 0, 1, 0, 0, 0, 1]], # x⁹ + x⁴ + 1
            11: [[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]] # x¹⁰ + x³ + 1
        }
        
        # Получаем длину полинома
        n = len(poly)
        
        # Проверяем, есть ли полином такой длины в словаре
        if n in primitive_polynomials:
            # Проверяем, совпадает ли полином с одним из известных примитивных полиномов
            return poly in primitive_polynomials[n]
        
        return False

    def validate_input(self):
        """Проверяет корректность входных данных"""
        message = self.message_entry.get()
        
        # Проверка на пустое сообщение
        if not message:
            messagebox.showerror("Ошибка", "Введите сообщение!")
            return False
        
        # Проверка на двоичный формат
        if not self.validate_binary_input(message):
            messagebox.showerror("Ошибка", "Сообщение должно содержать только 0 и 1!")
            return False
        
        # Получаем порождающий полином
        try:
            generator_poly = self.get_generator_polynomial()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return False
        
        # Проверка длины сообщения
        if len(message) < len(generator_poly) - 1:
            messagebox.showerror("Ошибка", 
                               "Длина сообщения должна быть не меньше степени полинома!")
            return False
        
        # Проверка примитивности полинома
        if not self.is_primitive_polynomial(generator_poly):
            messagebox.showwarning("Предупреждение", 
                                 "Выбранный полином не является примитивным!")
        
        return True

    def display_results(self, message_bits, generator_poly, steps, encoded_message):
        """Отображает результаты кодирования"""
        try:
            # Очищаем текстовые поля
            self.steps_text.delete(1.0, tk.END)
            self.result_text.delete(1.0, tk.END)
            
            # Отображаем пошаговое выполнение
            self.steps_text.insert(tk.END, "Процесс кодирования:\n\n")
            self.steps_text.insert(tk.END, f"1. Исходное сообщение: {message_bits}\n")
            self.steps_text.insert(tk.END, f"2. Порождающий полином: {generator_poly}\n")
            
            # Отображаем шаги деления
            self.steps_text.insert(tk.END, "\n3. Процесс деления:\n")
            for step in steps:
                self.steps_text.insert(tk.END, f"   {step}\n")
            
            # Отображаем результат
            self.result_text.insert(tk.END, "Закодированное сообщение:\n")
            self.result_text.insert(tk.END, f"{''.join(map(str, encoded_message))}\n")
            
            # Если полином не примитивный, показываем предупреждение
            if not self.is_primitive_polynomial(generator_poly):
                self.steps_text.insert(tk.END, "\nПредупреждение: Используемый полином не является примитивным!\n")
            
        except Exception as e:
            print(f"Ошибка в display_results: {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка при отображении результатов: {str(e)}")

    def convert_to_bits(self, input_data):
        """
        Преобразует входные данные в список битов
        input_data: строка или список
        """
        if isinstance(input_data, list):
            return input_data
        
        if isinstance(input_data, str):
            # Убираем префикс 0b если есть
            if input_data.startswith('0b'):
                input_data = input_data[2:]
            return [int(bit) for bit in input_data]
        
        raise ValueError(f"Неподдерживаемый формат входных данных: {type(input_data)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyclicCodeApp(root)
    root.mainloop()
