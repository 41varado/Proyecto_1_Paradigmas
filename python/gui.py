import tkinter as tk
import sys
from tkinter import scrolledtext
from evaluator import Evaluator
from main import read_file
from parser import *
from tokenizer import *
from tkinter import filedialog
from tkinter import messagebox

using_file_path = ""

def open_file():
    global using_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        using_file_path = file_path
        with open(file_path, "r") as file:
            content = file.read()
            scrolled_text.delete('1.0', tk.END)
            output_area.config(text="Resultados")
            scrolled_text.insert(tk.END, content)
    else:
        return ""


def save_file():
    global using_file_path
    if using_file_path != "":
        with open(using_file_path, "w") as file:
            file.write(scrolled_text.get("1.0", tk.END))
            messagebox.showinfo("Info", "Guardado exitosamente")
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".lox")
        with open(file_path, "w") as file:
            file.write(scrolled_text.get("1.0", tk.END))
            using_file_path = file_path


def compile_file():
    output_area.config(text="Resultados")
    global using_file_path
    if using_file_path == "":
        messagebox.showerror("Error", "Debe abrir o guardar el archivo")
    else:
        iterator = iter(sys.argv)
        next(iterator)
        command = next(iterator, "evaluate")
        file_path = using_file_path
        file_contents = read_file(using_file_path)
        tokenizer = Tokenizer(file_contents)
        tokens = tokenizer.process()
        tokens = map(lambda t: t.value, tokens)

        parser = Parser(tokens)
        expression_results = parser.process()
        expressions = map(lambda e: e.value, expression_results)
        result = ""
        try:
            evaluator = Evaluator(expressions, output_area)
            evaluator.process()
            if evaluator.error_flag is True:
                result = "El codigo presenta errores"
            else:
                result = "Codigo compilado exitosamente"
        except Exception as e:
            result = str(e)
        output_area.config(text=result)

def run_file():
    output_area.config(text="Resultados")
    global using_file_path
    if using_file_path == "":
        messagebox.showerror("Error", "Debe abrir o guardar el archivo")
    else:
        iterator = iter(sys.argv)
        next(iterator)
        command = next(iterator, "evaluate")
        file_path = using_file_path
        file_contents = read_file(using_file_path)
        tokenizer = Tokenizer(file_contents)
        tokens = tokenizer.process()
        tokens = map(lambda t: t.value, tokens)

        parser = Parser(tokens)
        expression_results = parser.process()
        expressions = map(lambda e: e.value, expression_results)

        try:
            evaluator = Evaluator(expressions, output_area)
            output_area.config(text=evaluator.process())
        except Exception as e:
            text = output_area["text"] + "\n"
            output_area.config(text=text + str(e))

def tokenize_file():
    output_area.config(text="Resultados")
    global using_file_path
    if using_file_path == "":
        messagebox.showerror("Error", "Debe abrir o guardar el archivo")
    else:
        iterator = iter(sys.argv)
        next(iterator)
        command = next(iterator, "evaluate")
        file_path = using_file_path
        file_contents = read_file(using_file_path)
        tokenizer = Tokenizer(file_contents)
        tokens = tokenizer.process()
        print_tokens(tokens, output_area)

def parse_file():
    output_area.config(text="Resultados")
    global using_file_path
    if using_file_path == "":
        messagebox.showerror("Error", "Debe abrir o guardar el archivo")
    else:
        iterator = iter(sys.argv)
        next(iterator)
        command = next(iterator, "evaluate")
        file_path = using_file_path
        file_contents = read_file(using_file_path)
        tokenizer = Tokenizer(file_contents)
        tokens = tokenizer.process()
        tokens = map(lambda t: t.value, tokens)

        parser = Parser(tokens)
        expression_results = parser.process()

        for result in expression_results:
            if result.is_ok:
                print_expression(result.value, output_area)
            else:
                output_area.config(text=result.error.message)



root = tk.Tk()
root.title("IDE UwU")
root.geometry("800x600")
open_button = tk.Button(root, text="Open", command=open_file)
save_button = tk.Button(root, text="Save", command=save_file)
compile_button = tk.Button(root, text="Compile", command=compile_file)
run_button = tk.Button(root, text="Run", command=run_file)
tokenize_button = tk.Button(root, text="Tokenize", command=tokenize_file)
parse_button = tk.Button(root, text="Parse", command=parse_file)

scrolled_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_area = tk.Label(root, text="Resultados", anchor=tk.NW)

open_button.grid(row=0, column=0, padx=1, sticky="w")
save_button.grid(row=0, column=1, padx=1)
compile_button.grid(row=0, column=2, padx=1)
run_button.grid(row=0, column=3, padx=1, sticky="e")
tokenize_button.grid(row=1, column=1, pady=2)
parse_button.grid(row=1, column=2, pady=2)

scrolled_text.grid(row=2, column=0, pady=1, rowspan=4, columnspan=4, sticky="nsew")
output_area.grid(row=5, column=0, pady=1, rowspan=3, columnspan=4, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.rowconfigure(2, weight=3)
root.rowconfigure(5, weight=1)
root.mainloop()