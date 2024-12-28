import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np

class CyclicCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Изучение циклических кодов")
        self.root.geometry("1200x800")
        
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
        
        ttk.Label(self.input_frame, text="Выберите порождающий полином:").pack(anchor="w")
        self.polynomial_var = tk.StringVar()
        polynomials = ["x³ + x + 1", "x⁴ + x + 1", "x⁷ + x³ + 1"]
        self.polynomial_combo = ttk.Combobox(self.input_frame, textvariable=self.polynomial_var, values=polynomials)
        self.polynomial_combo.pack(fill="x", pady=5)
        
        # Переключатель режима
        self.mode_var = tk.StringVar(value="study")
        ttk.Label(self.input_frame, text="\nРежим работы:").pack(anchor="w")
        ttk.Radiobutton(self.input_frame, text="Учебный режим", 
                       variable=self.mode_var, value="study").pack(anchor="w")
        ttk.Radiobutton(self.input_frame, text="Тестовый режим", 
                       variable=self.mode_var, value="test").pack(anchor="w")
        
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
        
        # Область рез��льтатов
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

    def polynomial_to_binary(self, polynomial_str):
        """Преобразует строковое представление полинома в бинарный массив коэффициентов"""
        try:
            # Для x³ + x + 1 должно получиться [1, 1, 0, 1]
            # Для x⁴ + x + 1 должно получиться [1, 1, 0, 0, 1]
            degrees = {'³': 3, '⁴': 4, '⁷': 7}
            max_degree = 0
            
            # Находим максимальную степень
            for c in polynomial_str:
                if c in degrees:
                    max_degree = max(max_degree, degrees[c])
            
            # Создаем массив нужной длины
            result = [0] * (max_degree + 1)
            result[max_degree] = 1  # Старший коэффициент
            
            # Разбираем остальные члены
            if '+ x + 1' in polynomial_str:
                result[1] = 1  # коэффициент при x
                result[0] = 1  # свободный член
                
            return result
        except Exception as e:
            print(f"Ошибка в polynomial_to_binary: {str(e)}")
            return [1, 1, 0, 1]  # возвращаем x³ + x + 1 по умолчанию

    def polynomial_division(self, dividend, divisor):
        """Выполняет деление полиномов в GF(2)"""
        try:
            # Преобразуем входные данные в списки
            dividend = list(dividend)  # Создаем копию делимого
            steps = []
            
            # Записываем начальное состояние
            steps.append(f"Делимое: {dividend}")
            
            # Пока длина делимого больше или равна длине делителя
            while len(dividend) >= len(divisor):
                # Если старший разряд равен 1
                if dividend[0] == 1:
                    # Выполняем XOR с делителем
                    for i in range(len(divisor)):
                        if i < len(dividend):
                            dividend[i] ^= divisor[i]
                
                steps.append(f"После вычитания: {dividend}")
                
                # Убираем ведущий ноль
                if dividend and dividend[0] == 0:
                    dividend.pop(0)
            
            # Дополняем остаток нулями слева до нужной длины
            while len(dividend) < len(divisor) - 1:
                dividend.insert(0, 0)
            
            return dividend, steps
            
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
            # Получаем входные данные
            message = self.message_entry.get()
            if not self.validate_binary_input(message):
                messagebox.showerror("Ошибка", "Введите корректное двоичное число!")
                return
            
            # Получаем порождающий полином
            generator_poly = self.polynomial_to_binary(self.polynomial_var.get())
            
            # Преобразуем сообщение в список битов
            message_bits = [int(bit) for bit in message]
            
            # Добавляем нули к сообщению
            augmented_message = message_bits + [0] * (len(generator_poly) - 1)
            
            # Выполняем деление
            remainder, steps = self.polynomial_division(augmented_message, generator_poly)
            
            # Формируем закодированное сообщение
            encoded_message = message_bits + remainder
            
            # Выводим результаты
            self.steps_text.delete(1.0, tk.END)
            self.result_text.delete(1.0, tk.END)
            
            self.steps_text.insert(tk.END, "Процесс кодирования:\n\n")
            self.steps_text.insert(tk.END, f"1. Исходное сообщение: {message}\n")
            self.steps_text.insert(tk.END, f"2. Порождающий полином: {self.polynomial_var.get()}\n")
            self.steps_text.insert(tk.END, f"3. Двоичное представление полинома: {generator_poly}\n\n")
            self.steps_text.insert(tk.END, "4. Процесс деления:\n")
            
            for step in steps:
                self.steps_text.insert(tk.END, f"   {step}\n")
            
            result = ''.join(map(str, encoded_message))
            self.steps_text.insert(tk.END, f"\n5. Результат кодирования: {result}\n")
            
            self.result_text.insert(tk.END, "Закодированное сообщение:\n")
            self.result_text.insert(tk.END, f"{result}\n")
            
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
        return all(bit in '01' for bit in input_str)

    def show_theory(self):
        """Показывает теоретическую справку"""
        theory_window = tk.Toplevel(self.root)
        theory_window.title("Теоретическая справ��а")
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
        """Выполняет следующий шаг  пошаговом режиме"""
        if not hasattr(self, 'current_step'):
            self.current_step = 0
            
        self.current_step += 1
        if self.current_step == 1:
            self.show_encoding_step_1()
        elif self.current_step == 2:
            self.show_encoding_step_2()
        elif self.current_step == 3:
            self.show_encoding_step_3()
        elif self.current_step == 4:
            self.show_encoding_step_4()
        else:
            self.next_step_button.config(state="disabled")
            self.current_step = 0

    def show_encoding_step_1(self):
        """Показывает первый шаг кодирования"""
        message = self.message_entry.get()
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "Шаг 1: Анализ входных данных\n\n")
        self.steps_text.insert(tk.END, f"• Исходное сообщение: {message}\n")
        self.steps_text.insert(tk.END, f"• Длина сообщения: {len(message)} бит\n")
        self.steps_text.insert(tk.END, "• Представление в виде полинома:\n")
        
        # Показываем полиномиальное представление сообщения
        poly_terms = []
        for i, bit in enumerate(reversed(message)):
            if bit == '1':
                if i == 0:
                    poly_terms.append("1")
                elif i == 1:
                    poly_terms.append("x")
                else:
                    poly_terms.append(f"x^{i}")
        poly_str = " + ".join(reversed(poly_terms)) if poly_terms else "0"
        self.steps_text.insert(tk.END, f"  {poly_str}\n")

    def show_encoding_step_2(self):
        """Показывает второй шаг кодирования"""
        generator_poly_str = self.polynomial_var.get()
        generator_poly = self.polynomial_to_binary(generator_poly_str)
        
        self.steps_text.insert(tk.END, "\nШаг 2: Анализ порождающего полинома\n\n")
        self.steps_text.insert(tk.END, f"• Выбранный полином: {generator_poly_str}\n")
        self.steps_text.insert(tk.END, f"• Степень полинома: {len(generator_poly)-1}\n")
        self.steps_text.insert(tk.END, f"• Двоичное представление: {generator_poly}\n")

    def show_encoding_step_3(self):
        """Показывает третий шаг кодирования"""
        message = self.message_entry.get()
        generator_poly = self.polynomial_to_binary(self.polynomial_var.get())
        
        message_bits = [int(bit) for bit in message]
        zeros = [0] * (len(generator_poly) - 1)
        augmented_message = message_bits + zeros
        
        self.steps_text.insert(tk.END, "\nШаг 3: Подготовка сообщения\n\n")
        self.steps_text.insert(tk.END, f"• Исходное сообщение: {message_bits}\n")
        self.steps_text.insert(tk.END, f"• Добавляем {len(zeros)} нулей: {augmented_message}\n")

    def show_encoding_step_4(self):
        """Показывает четвертый шаг кодирования и финальный результат"""
        message = self.message_entry.get()
        generator_poly = self.polynomial_to_binary(self.polynomial_var.get())
        
        message_bits = [int(bit) for bit in message]
        zeros = [0] * (len(generator_poly) - 1)
        augmented_message = message_bits + zeros
        
        remainder, division_steps = self.polynomial_division(augmented_message, generator_poly)
        encoded_message = message_bits + remainder
        
        self.steps_text.insert(tk.END, "\nШаг 4: Получение контрольных битов\n\n")
        for step in division_steps:
            self.steps_text.insert(tk.END, f"• {step}\n")
            
        self.steps_text.insert(tk.END, "\nФинальный результат:\n")
        self.steps_text.insert(tk.END, f"• Закодированное сообщение: {''.join(map(str, encoded_message))}\n")
        
        # Обновляем область результатов
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Закодированное сообщение:\n")
        self.result_text.insert(tk.END, f"{''.join(map(str, encoded_message))}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyclicCodeApp(root)
    root.mainloop()
