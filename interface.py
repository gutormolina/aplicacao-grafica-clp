import ctypes
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

mylib = ctypes.CDLL('./libMandel.so')

# Função a ser chamada quando o botão for clicado
def process_number(maxiter):
    print("botao")
    try:
        mylib.main.argtypes =[
        ctypes.c_int,            # argc (número de argumentos)
        ctypes.POINTER(ctypes.c_char_p)  # argv (array de strings)
        ]

        mylib.main.restype = ctypes.c_int  # Tipo de retorno da função (int em C)

        # Preparando os argumentos
        maxiter_bytes = str(maxiter).encode('utf-8')
        arguments = [
            b"./mandelbrot",         # Nome do programa, geralmente ignorado
            b"0.27085", b"0.27100",  # xmin, xmax
            b"0.004640", b"0.004810",  # ymin, ymax
            maxiter_bytes,             # maxiter
            b"1024",             # xres
            b"pic.ppm"           # filename
        ]
        argc = len(arguments)
        argv = (ctypes.c_char_p * argc)(*arguments)

        # Chamando a função main da biblioteca C
        ret = mylib.main(argc, argv)

        # Verificando o retorno da função
        print(f"Função retornou: {ret}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido.")

# Função para validar a entrada, permitindo apenas números
def validate_entry(value_if_allowed):
    if value_if_allowed.isdigit() or value_if_allowed == "":
        return True
    else:
        return False

def generateScreen():
    root = tk.Tk()
    root.title("Minha Primeira Janela")

    # Configurar o tamanho da janela
    root.geometry("1280x720")
    label = tk.Label(root, text="Digite um número:")
    label.pack(pady=10)

    # Cria uma validação para a entrada
    vcmd = (root.register(validate_entry), "%P")

    # Cria um campo de entrada (entry) que aceita apenas números
    entry = tk.Entry(root, validate="key", validatecommand=vcmd)
    entry.pack(pady=10)

    # Cria um botão que chama a função process_number ao ser clicado
    button = tk.Button(root, text="Processar", command=lambda: process_number(entry.get()))
    button.pack(pady=10)

    # Carregar e exibir a imagem
    img = Image.open("pic.ppm")
    img = img.resize((400, 400), Image.Resampling.LANCZOS)  
    img_tk = ImageTk.PhotoImage(img)
    
    # Cria um rótulo (label) para a imagem
    img_label = tk.Label(root, image=img_tk)
    img_label.image = img_tk  # Manter uma referência para evitar que a imagem seja coletada pelo garbage collector
    img_label.pack(pady=20)

    root.mainloop()    

if __name__ == "__main__":
    generateScreen()
