import ctypes

mylib = ctypes.CDLL('./libMandel.so')

def main():
    mylib.main.argtypes =[
    ctypes.c_int,            # argc (número de argumentos)
    ctypes.POINTER(ctypes.c_char_p)  # argv (array de strings)
    ]

    mylib.main.restype = ctypes.c_int  # Tipo de retorno da função (int em C)

    # Preparando os argumentos
    arguments = [
        b"./mandel",         # Nome do programa, geralmente ignorado
        b"0.27085", b"0.27100",  # xmin, xmax
        b"0.004640", b"0.004810",  # ymin, ymax
        b"400",             # maxiter
        b"2048",             # xres
        b"pic3.ppm"           # filename
    ]
    argc = len(arguments)
    argv = (ctypes.c_char_p * argc)(*arguments)

    # Chamando a função main da biblioteca C
    ret = mylib.main(argc, argv)

    # Verificando o retorno da função
    print(f"Função retornou: {ret}")


if __name__ == "__main__":
    main()