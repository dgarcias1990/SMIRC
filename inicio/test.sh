#! / Bin / bash

# Lo verdadero Python ejecutable para utilizar
Pyver = 2,7
PATHTOPYTHON = / usr / local / bin /
PYTHON = $ {} PATHTOPYTHON pitón $ {} Pyver

# Encontrar la raíz del virtualenv, debe ser el padre de la dir este script se encuentra en
ENV = `$ python -c" import os; os.path.abspath de impresión (os.path.join (os.path.dirname (\ "$ 0 \"), '..')) "`

# Ahora ejecutar Python con el virtualenv establecido como el hogar de Python
PYTHONHOME exportación = $ ENV
exec $ Python "$ @"