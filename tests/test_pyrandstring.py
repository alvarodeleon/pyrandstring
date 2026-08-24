import unittest

from pyrandstring import pyrandstring

ALPHABETS = ['abc', 'num', 'anum', 'all', 'bash', 'zsh']

# Tamano esperado de cada alfabeto, para detectar caracteres perdidos o duplicados.
SIZES = {'abc': 52, 'num': 10, 'anum': 62, 'all': 81, 'bash': 78, 'zsh': 78}


def alphabet(name):
	'''Devuelve el alfabeto observado generando una muestra grande.'''
	p = pyrandstring()
	return set(''.join(p.getString(2000, name) for _ in range(10)))


class TestAlphabets(unittest.TestCase):

	def test_sizes(self):
		for name in ALPHABETS:
			self.assertEqual(len(alphabet(name)), SIZES[name], name)

	def test_abc_tiene_las_52_letras(self):
		esperado = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
		self.assertEqual(alphabet('abc'), esperado)

	def test_h_presente(self):
		# Regresion: las listas tenian '' donde iba 'h'.
		for name in ['abc', 'anum', 'all', 'bash']:
			self.assertIn('h', alphabet(name), name)

	def test_num_solo_digitos(self):
		self.assertEqual(alphabet('num'), set('0123456789'))

	def test_bash_excluye_comillas_y_parentesis(self):
		observado = alphabet('bash')
		for ch in ['"', '(', ')']:
			self.assertNotIn(ch, observado)

	def test_bash_es_subconjunto_de_all(self):
		self.assertTrue(alphabet('bash').issubset(alphabet('all')))

	def test_seed_desconocido(self):
		with self.assertRaises(KeyError):
			pyrandstring().getString(8, 'inexistente')


class TestLargo(unittest.TestCase):

	def test_largo_exacto(self):
		# Regresion: el '' en el alfabeto producia strings mas cortos que lo pedido.
		p = pyrandstring()
		for name in ALPHABETS:
			for _ in range(200):
				self.assertEqual(len(p.getString(20, name)), 20, name)

	def test_largo_por_defecto(self):
		self.assertEqual(len(pyrandstring().getString()), 18)

	def test_largo_cero(self):
		self.assertEqual(pyrandstring().getString(0), '')

	def test_largo_como_string(self):
		self.assertEqual(len(pyrandstring().getString('7', 'num')), 7)


class TestEstado(unittest.TestCase):

	def test_length_explicito_no_pisa_el_default(self):
		# Regresion: getString(5) dejaba self.length en 5 para siempre.
		p = pyrandstring()
		p.getString(5, 'num')
		self.assertEqual(p.length, 18)
		self.assertEqual(len(p.getString()), 18)

	def test_seed_explicito_no_pisa_el_default(self):
		p = pyrandstring()
		p.getString(8, 'num')
		self.assertEqual(p.seed, 'all')

	def test_get_string_unique_no_pisa_el_default(self):
		# Regresion: getStringUnique() dejaba self.length en 16.
		p = pyrandstring()
		p.getStringUnique()
		self.assertEqual(p.length, 18)
		self.assertEqual(len(p.getString()), 18)

	def test_defaults_de_instancia(self):
		p = pyrandstring()
		p.length = 30
		p.seed = 'num'
		s = p.getString()
		self.assertEqual(len(s), 30)
		self.assertTrue(s.isdigit())

	def test_instancias_independientes(self):
		a = pyrandstring()
		b = pyrandstring()
		a.length = 40
		self.assertEqual(len(b.getString()), 18)


class TestZsh(unittest.TestCase):
	'''zsh es el nombre que usa el script passgen para el mismo alfabeto que bash.'''

	def test_zsh_es_alias_de_bash(self):
		self.assertEqual(alphabet('zsh'), alphabet('bash'))

	def test_zsh_excluye_comillas_y_parentesis(self):
		observado = alphabet('zsh')
		for ch in ['"', '(', ')']:
			self.assertNotIn(ch, observado)


class TestUUID(unittest.TestCase):

	def test_formato(self):
		import uuid
		s = pyrandstring().getUUID()
		self.assertEqual(len(s), 36)
		self.assertEqual(s.count('-'), 4)
		# debe ser parseable y de version 4 (aleatorio)
		self.assertEqual(uuid.UUID(s).version, 4)

	def test_es_str(self):
		self.assertIsInstance(pyrandstring().getUUID(), str)

	def test_sin_colisiones(self):
		p = pyrandstring()
		generados = [p.getUUID() for _ in range(500)]
		self.assertEqual(len(set(generados)), 500)


class TestStringList(unittest.TestCase):

	def test_cantidad(self):
		p = pyrandstring()
		self.assertEqual(len(p.getStringList(10)), 10)
		self.assertEqual(len(p.getStringList('7')), 7)
		self.assertEqual(p.getStringList(0), [])

	def test_respeta_length_y_seed(self):
		p = pyrandstring()
		lista = p.getStringList(20, 12, 'num')
		self.assertEqual(len(lista), 20)
		for s in lista:
			self.assertEqual(len(s), 12)
			self.assertTrue(s.isdigit())

	def test_usa_los_defaults_de_la_instancia(self):
		p = pyrandstring()
		p.length = 24
		p.seed = 'num'
		for s in p.getStringList(5):
			self.assertEqual(len(s), 24)
			self.assertTrue(s.isdigit())

	def test_no_pisa_los_defaults(self):
		p = pyrandstring()
		p.getStringList(3, 5, 'num')
		self.assertEqual(p.length, 18)
		self.assertEqual(p.seed, 'all')

	def test_elementos_distintos(self):
		p = pyrandstring()
		lista = p.getStringList(500, 24)
		self.assertEqual(len(set(lista)), 500)


class TestUnique(unittest.TestCase):

	def test_formato(self):
		s = pyrandstring().getStringUnique()
		timestamp, sufijo = s.split('_')
		self.assertTrue(timestamp.isdigit())
		self.assertEqual(len(sufijo), 16)
		self.assertTrue(sufijo.isalnum())

	def test_sin_colisiones(self):
		p = pyrandstring()
		generados = [p.getStringUnique() for _ in range(500)]
		self.assertEqual(len(set(generados)), 500)


class TestAleatoriedad(unittest.TestCase):

	def test_no_repite(self):
		p = pyrandstring()
		generados = [p.getString(24) for _ in range(500)]
		self.assertEqual(len(set(generados)), 500)

	def test_fuente_criptografica(self):
		# El generador nunca debe ser el random global (Mersenne Twister, predecible).
		# Se busca en sys.modules porque el paquete rebinda 'pyrandstring' a la clase.
		import random
		import sys
		import pyrandstring.pyrandstring  # noqa: F401  (puebla sys.modules)

		choice = sys.modules['pyrandstring.pyrandstring']._choice
		self.assertIsNot(choice, random.choice)

		if sys.version_info >= (3, 6):
			import secrets
			self.assertIs(choice, secrets.choice)
		else:
			self.assertIsInstance(choice.__self__, random.SystemRandom)

	def test_fallback_27_es_system_random(self):
		# Ejercita la rama de Python 2.7 aun corriendo sobre 3.x: si 'secrets' no
		# esta disponible, debe caer en random.SystemRandom (os.urandom), no en
		# random.choice. Sin esto la rama 2.7 solo se probaria en un 2.7 real.
		import random
		import sys
		try:
			import builtins
		except ImportError:
			import __builtin__ as builtins

		real_import = builtins.__import__
		previos = dict((k, v) for k, v in sys.modules.items()
			if k.startswith('pyrandstring'))

		def sin_secrets(name, *args, **kwargs):
			if name == 'secrets':
				raise ImportError('simulando Python 2.7')
			return real_import(name, *args, **kwargs)

		try:
			builtins.__import__ = sin_secrets
			for nombre in list(previos):
				del sys.modules[nombre]

			import pyrandstring.pyrandstring  # noqa: F401
			modulo = sys.modules['pyrandstring.pyrandstring']
			self.assertIsInstance(modulo._choice.__self__, random.SystemRandom)
			self.assertIsNot(modulo._choice, random.choice)

			# y el resultado sigue siendo correcto por esa via
			p = modulo.pyrandstring()
			self.assertEqual(len(p.getString(20, 'anum')), 20)
			self.assertIn('h', ''.join(p.getString(500, 'abc') for _ in range(10)))
		finally:
			builtins.__import__ = real_import
			for nombre in list(sys.modules):
				if nombre.startswith('pyrandstring'):
					del sys.modules[nombre]
			sys.modules.update(previos)


class TestImports(unittest.TestCase):

	def test_formas_de_import(self):
		import pyrandstring as paquete
		from pyrandstring import pyrandstring as desde_paquete
		from pyrandstring.pyrandstring import pyrandstring as desde_modulo

		self.assertIs(desde_paquete, desde_modulo)
		self.assertIs(paquete.pyrandstring, desde_modulo)
		# Patron historico: el nombre importado servia de modulo.
		self.assertIs(desde_paquete.pyrandstring, desde_modulo)
		self.assertEqual(len(desde_paquete.pyrandstring().getString()), 18)


if __name__ == '__main__':
	unittest.main()
