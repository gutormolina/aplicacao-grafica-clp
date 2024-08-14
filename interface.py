import ctypes
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

mylib = ctypes.CDLL('./libMandel.so')

class Application:
    def __init__(self, root) -> None:
        self.root = root
        self.generateScreen()

    # Função a ser chamada quando o botão for clicado
    def processFractal(self):
        xmin, xmax, ymin, ymax, maxiter, xres = self.getValues()
        try:
            mylib.main.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_char_p)
            ]
            mylib.main.restype = ctypes.c_int

            maxiter_bytes = str(maxiter).encode('utf-8')
            arguments = [
                b"./mandelbrot",
                xmin.encode('utf-8'), xmax.encode('utf-8'),
                ymin.encode('utf-8'), ymax.encode('utf-8'),
                maxiter_bytes,
                xres.encode('utf-8'),
                b"pic.ppm"
            ]
            argc = len(arguments)
            argv = (ctypes.c_char_p * argc)(*arguments)

            ret = mylib.main(argc, argv)
            print(f"Function returned: {ret}")

            self.loadImage()
        except ValueError:
            messagebox.showerror("Error", "Por favor insira um número válido.")

    # Função para validar a entrada, permitindo apenas números
    def validateEntry(self, value_if_allowed):
        if value_if_allowed.isdigit() or value_if_allowed == "":
            return True
        else:
            return False

    def getValues(self):
        xmin = self.xminEnt.get()
        xmax = self.xmaxEnt.get()
        ymin = self.yminEnt.get()
        ymax = self.ymaxEnt.get()
        maxiter = self.maxiterEnt.get()
        xres = self.xresEnt.get()

        return xmin, xmax, ymin, ymax, maxiter, xres   

    def generateScreen(self):
        # atribuições da janela
        self.root.title("Fractal de Mandelbrot")
        self.root.geometry("370x200")
        self.root.resizable(width='false', height='false')

        # xmin
        self.xminLab = tk.Label(self.root, text="xmin:")
        self.xminLab.grid(column=0, row=0)
        self.xminEnt = tk.Entry(self.root)
        self.xminEnt.insert(0, "-0.74877")
        self.xminEnt.grid(column=0, row=1)

        # xmax
        self.xmaxLab = tk.Label(self.root, text="xmax:")
        self.xmaxLab.grid(column=1, row=0)
        self.xmaxEnt = tk.Entry(self.root)
        self.xmaxEnt.insert(0, "-0.74872")
        self.xmaxEnt.grid(column=1, row=1)

        #ymin
        self.yminLab = tk.Label(self.root, text="ymin:")
        self.yminLab.grid(column=0, row=2)
        self.yminEnt = tk.Entry(self.root)
        self.yminEnt.insert(0, "0.06505")
        self.yminEnt.grid(column=0, row=3)

        #ymax
        self.ymaxLab = tk.Label(self.root, text="ymax:")
        self.ymaxLab.grid(column=1, row=2)
        self.ymaxEnt = tk.Entry(self.root)
        self.ymaxEnt.insert(0, "0.06510")
        self.ymaxEnt.grid(column=1, row=3)

        #maxiter
        self.maxiterLab = tk.Label(self.root, text="maxiter:")
        self.maxiterLab.grid(column=0, row=4)
        self.maxiterEnt = tk.Entry(self.root)
        self.maxiterEnt.insert(0, "1000")
        self.maxiterEnt.grid(column=0, row=5)

        #xres
        self.xresLab = tk.Label(self.root, text="xres:")
        self.xresLab.grid(column=1, row=4)
        self.xresEnt = tk.Entry(self.root)
        self.xresEnt.insert(0, "1024")
        self.xresEnt.grid(column=1, row=5)

        # Cria uma validação para a entrada
        vcmd = (self.root.register(self.validateEntry), "%P")

        # Cria um campo de entrada (entry) que aceita apenas números
        self.entry = tk.Entry(self.root, validate="key", validatecommand=vcmd)

        # Cria um botão que chama a função process_number ao ser clicado
        self.button = tk.Button(self.root, text="Processar", command=self.processFractal)
        self.button.grid(column=0 , row=6, columnspan=2)

        # Cria um botão que apresenta valores recomendados
        self.recommend = tk.Button(self.root, text="Parâmetros recomendados", command=self.recommendParameters)
        self.recommend.grid(column=0, row=7, columnspan=2)

    def recommendParameters(self):
        rec_window = tk.Toplevel(self.root)
        rec_window.title("Recomendações")
        
        heart = tk.Label(rec_window, text="Heart:")
        heart.grid(column=0, row=0, columnspan=2)
        heart_xmin_text = tk.StringVar(value="-0.74877")
        heart_xmin = tk.Entry(rec_window, state='readonly', textvariable=heart_xmin_text)
        heart_xmin.grid(column=0, row=1)
        heart_xmax_text = tk.StringVar(value="-0.74872")
        heart_xmax = tk.Entry(rec_window, state='readonly', textvariable=heart_xmax_text)
        heart_xmax.grid(column=1, row=1)
        heart_ymin_text = tk.StringVar(value="0.06505")
        heart_ymin = tk.Entry(rec_window, state='readonly', textvariable=heart_ymin_text)
        heart_ymin.grid(column=0, row=2)
        heart_ymax_text = tk.StringVar(value="0.06510")
        heart_ymax = tk.Entry(rec_window, state='readonly', textvariable=heart_ymax_text)
        heart_ymax.grid(column=1, row=2)
        heart_maxiter_text = tk.StringVar(value="1000")
        heart_maxiter = tk.Entry(rec_window, state='readonly', textvariable=heart_maxiter_text)
        heart_maxiter.grid(column=0, row=3)
        heart_xres_text = tk.StringVar(value="1024")
        heart_xres = tk.Entry(rec_window, state='readonly', textvariable=heart_xres_text)
        heart_xres.grid(column=1, row=3)
        
        wide_view = tk.Label(rec_window, text="Wide view:")
        wide_view.grid(column=2, row=0, columnspan=2)
        wv_xmin_text = tk.StringVar(value="-2.0")
        wv_xmin = tk.Entry(rec_window, state='readonly', textvariable=wv_xmin_text)
        wv_xmin.grid(column=2, row=1)
        wv_xmax_text = tk.StringVar(value="1.0")
        wv_xmax = tk.Entry(rec_window, state='readonly', textvariable=wv_xmax_text)
        wv_xmax.grid(column=3, row=1)
        wv_ymin_text = tk.StringVar(value="-1.5")
        wv_ymin = tk.Entry(rec_window, state='readonly', textvariable=wv_ymin_text)
        wv_ymin.grid(column=2, row=2)
        wv_ymax_text = tk.StringVar(value="1.5")
        wv_ymax = tk.Entry(rec_window, state='readonly', textvariable=wv_ymax_text)
        wv_ymax.grid(column=3, row=2)
        wv_maxiter_text = tk.StringVar(value="500")
        wv_maxiter = tk.Entry(rec_window, state='readonly', textvariable=wv_maxiter_text)
        wv_maxiter.grid(column=2, row=3)
        wv_xres_text = tk.StringVar(value="800")
        wv_xres = tk.Entry(rec_window, state='readonly', textvariable=wv_xres_text)
        wv_xres.grid(column=3, row=3)
        
        mini_mandelbrot = tk.Label(rec_window, text="Mini Mandelbrot:")
        mini_mandelbrot.grid(column=1, row=4, columnspan=2)
        mm_xmin_text = tk.StringVar(value="-1.25066")
        mm_xmin = tk.Entry(rec_window, state='readonly', textvariable=mm_xmin_text)
        mm_xmin.grid(column=1, row=5)
        mm_xmax_text = tk.StringVar(value="-1.25055")
        mm_xmax = tk.Entry(rec_window, state='readonly', textvariable=mm_xmax_text)
        mm_xmax.grid(column=2, row=5)
        mm_ymin_text = tk.StringVar(value="0.02012")
        mm_ymin = tk.Entry(rec_window, state='readonly', textvariable=mm_ymin_text)
        mm_ymin.grid(column=1, row=6)
        mm_ymax_text = tk.StringVar(value="0.02022")
        mm_ymax = tk.Entry(rec_window, state='readonly', textvariable=mm_ymax_text)
        mm_ymax.grid(column=2, row=6)
        mm_maxiter_text = tk.StringVar(value="3000")
        mm_maxiter = tk.Entry(rec_window, state='readonly', textvariable=mm_maxiter_text)
        mm_maxiter.grid(column=1, row=7)
        mm_xres_text = tk.StringVar(value="1920")
        mm_xres = tk.Entry(rec_window, state='readonly', textvariable=mm_xres_text)
        mm_xres.grid(column=2, row=7)
        
    def loadImage(self):
        try:
            img_window = tk.Toplevel(self.root)
            img_window.title("Imagem gerada")

            img = Image.open("pic.ppm")
            img = img.resize((800, 800), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(img_window, image=img_tk)
            img_label.image = img_tk
            img_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Error", "File pic.ppm not found.")

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()