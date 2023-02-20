# hanmoto

hanmoto makes your esc/pos printer accessible through Web API endpoint and offer you high level python esc/pos printer library.

## Installation

install with pip
``` bash
$ pip install hanmoto
```

or you can install with poetry from source code.

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

### In python

``` python
from hanmoto.printer import Hanmoto, hmtText, HmtImage
hmt = Hanmoto.from_network()
with hmt:
    sequence = [
        HmtImage("../header.png").center(),
        hmtText("hello hanmoto!").center().bold(),
    ]
    hmt.print_sequence(sequence)
```
