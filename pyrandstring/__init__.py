from .pyrandstring import pyrandstring

# El paquete, el modulo y la clase comparten nombre. Este alias mantiene vivo el
# patron historico `from pyrandstring import pyrandstring; pyrandstring.pyrandstring()`
# ahora que el nombre importado es la clase y ya no el modulo.
pyrandstring.pyrandstring = pyrandstring

__all__ = ['pyrandstring']
