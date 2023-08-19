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

Use `hanmoto` command to start API server.

Following example starts API server with network connected printer.


``` bash
$ hanmoto network your.escpos.printer.ip
```

and sent request to API endpoint

``` bash
curl -X POST -H "Content-Type: application/json" -d '{"type": "text", "content": "hoge"}' http://localhost:8000/print/text
```

### In python

``` python
from hanmoto.printer import Hanmoto, hmtText, HmtImage
hmt = Hanmoto.from_network()
# set ip addr to environment varieble HANMOTO_PRINTER_IP
# or you can pass it directly like Hanmoto.from_network(192.168.1.13)
with hmt:
    sequence = [
        HmtImage("../header.png").center(),
        hmtText("hello hanmoto!").center().bold(),
    ]
    hmt.print_sequence(sequence)
```
