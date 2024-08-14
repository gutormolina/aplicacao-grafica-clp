import ctypes
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

mylib = ctypes.CDLL('./libMandel.so')

# Função a ser chamada quando o botão for clicado
def processFractal():
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
def validateEntry(value_if_allowed):
    if value_if_allowed.isdigit() or value_if_allowed == "":
        return True
    else:
        return False
    
def getValues():
    xmin = xminEnt.get()
    xmax = xmaxEnt.get()
    ymin = yminEnt.get()
    ymax = ymaxEnt.get()
    maxiter = maxiterEnt.get()
    xres = xresEnt.get()

    return xmin, xmax, ymin, ymax, maxiter, xres   

def generateScreen():
    root = tk.Tk()
    root.title("Fractal de Mandelbrot")
    root.geometry("370x200")
    root.resizable(width = 'false', height = 'false')

    # xmin
    xminLab = tk.Label(root, text = "xmin:")
    xminLab.grid(column = 0, row = 0)
    xminEnt = tk.Entry(root)
    xminEnt.grid(column = 0, row = 1)

    # xmax
    xmaxLab = tk.Label(root, text = "xmax:")
    xmaxLab.grid(column = 1, row = 0)
    xmaxEnt = tk.Entry(root)
    xmaxEnt.grid(column = 1, row = 1)

    #ymin
    yminLab = tk.Label(root, text = "ymin:")
    yminLab.grid(column = 0, row = 2)
    yminEnt = tk.Entry(root)
    yminEnt.grid(column = 0, row = 3)

    #ymax
    ymaxLab = tk.Label(root, text = "ymax:")
    ymaxLab.grid(column = 1, row = 2)
    ymaxEnt = tk.Entry(root)
    ymaxEnt.grid(column = 1, row = 3)

    #maxiter
    maxiterLab = tk.Label(root, text = "maxiter:")
    maxiterLab.grid(column = 0, row = 4)
    maxiterEnt = tk.Entry(root)
    maxiterEnt.grid(column = 0, row = 5)

    #xres
    xresLab = tk.Label(root, text = "xres:")
    xresLab.grid(column = 1, row = 4)
    xresEnt = tk.Entry(root)
    xresEnt.grid(column = 1, row = 5)

    # Cria uma validação para a entrada
    vcmd = (root.register(validateEntry), "%P")

    # Cria um campo de entrada (entry) que aceita apenas números
    entry = tk.Entry(root, validate = "key", validatecommand = vcmd)

    # Cria um botão que chama a função process_number ao ser clicado
    button = tk.Button(root, text = "Processar", command = processFractal())
    button.grid(column = 0 , row = 6, columnspan = 2)

    # Carregar e exibir a imagem
    img = Image.open("pic.ppm")
    img = img.resize((400, 400), Image.Resampling.LANCZOS)  
    img_tk = ImageTk.PhotoImage(img)
    
    # Cria um rótulo (label) para a imagem
    img_label = tk.Label(root, image = img_tk)
    img_label.image = img_tk  # Manter uma referência para evitar que a imagem seja coletada pelo garbage collector
    
    root.mainloop() 


if __name__ == "__main__":
    generateScreen()
