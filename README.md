# pyrandstring

Random string generation (passwords, identifiers) backed by a cryptographically
secure source from the standard library.

Works on Python 2.7 and 3.x. On Python 3.6+ it uses `secrets.choice`; on earlier
versions it falls back to `random.SystemRandom`, which draws from `os.urandom` -
the same source `secrets` uses internally. The global `random` generator, which
is predictable, is never used.

## Installation

```bash
pip install pyrandstring
```

## Usage

```python
from pyrandstring import pyrandstring

p = pyrandstring()

p.getString()              # 18 characters from the full alphabet
p.getString(32)            # 32 characters from the full alphabet
p.getString(12, 'anum')    # 12 alphanumeric characters
p.getStringUnique()        # '1706462498_Xk2pQm9WvBn4TzLc'
p.getUUID()                # '4e9abb2e-9bcc-40c7-bd6f-3021c5e3a0ad'
p.getStringList(3, 12)     # ['6nINov%F(W6s', ',m4AwzBPlPe2', 'AeV7SNGclLVM']
```

Defaults can be set per instance:

```python
p = pyrandstring()
p.length = 32
p.seed = 'bash'

p.getString()              # 32 characters, 'bash' alphabet
```

Passing `length` or `seed` to `getString()` affects that call only; the
instance defaults are left untouched.

## Alphabets

| `seed`  | Characters | Size |
|---------|------------|------|
| `abc`   | `A-Z` `a-z` | 52 |
| `num`   | `0-9` | 10 |
| `anum`  | `A-Z` `a-z` `0-9` | 62 |
| `all`   | `anum` + ``!"#$%&()*+,-./{\|}~@`` | 81 |
| `bash`  | `all` without `"` `(` `)` | 78 |
| `zsh`   | alias of `bash` | 78 |

`all` is the default alphabet. `bash` omits the symbols that need escaping when
the string is passed through a shell; `zsh` is an alias for it.

An unknown `seed` raises `KeyError`.

## API

### `getString(length=None, seed=None)`

Returns a random string of length `length`. When omitted, uses `self.length`
(18) and `self.seed` (`'all'`).

### `getStringUnique()`

Returns `<unix_timestamp>_<16 alphanumeric characters>`. Intended for filenames
and keys that also need to sort by time.

### `getUUID()`

Returns a random UUID (version 4) as a string.

### `getStringList(quantity, length=None, seed=None)`

Returns a list of `quantity` random strings. `length` and `seed` behave exactly
as in `getString()`, and the instance defaults are left untouched.

```python
p.getStringList(5, 16, 'anum')
```

## Tests

```bash
python -m unittest discover tests -v
```

## License

GPL-3.0. See [LICENSE.txt](LICENSE.txt).
