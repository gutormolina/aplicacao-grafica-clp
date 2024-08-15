# Compilador e flags para C
CC = gcc
CFLAGS = -O4 -fPIC -shared

# Python
PYTHON = python3
PYTHON_SCRIPT = interface.py

# Targets
LIBRARY = libMandel.so
SOURCES = mandelbrot.c

# Default
all: $(LIBRARY)

# Compilar biblioteca
$(LIBRARY): $(SOURCES)
	$(CC) $(CFLAGS) -o $@ $<

# Rodar script Python
run: $(LIBRARY)
	$(PYTHON) $(PYTHON_SCRIPT)