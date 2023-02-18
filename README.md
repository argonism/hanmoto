# hanmoto

hanmoto makes your esc/pos printer accessible through Web API endpoint and offer you easy to use python esc/pos printer interface.

## Installation

install with pip
``` bash
$ pip install hanmoto
```

or you can install with python poetry from source code.

``` bash
$ git clone https://github.com/argonism/hanmoto.git
$ cd hanmoto
$ poetry install
```

## Usage

### printer as API endpoint
``` bash
$ cd hanmoto
$ HANMOTO_PRINTER_IP={Put your printer IP address here}
$ uvicorn hanmoto.api:app --port 1885 --host 0.0.0.0
```

### in python

``` python
from hanmoto.printer import Hanmoto, hmtText
hmt = Hanmoto.from_network()
with hmt:
    texts = [
        hmtText("hello hanmoto!").center().bold(),
        hmtText("hanmoto-n").right()
    ]
    hmt.print_sequence(texts)
```
