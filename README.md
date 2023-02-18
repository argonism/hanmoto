# Tofu

Tofu makes your esc/pos printer accessible through API endpoint and offer you easy to use python esc/pos printer interface.

## Installation

install with pip
``` bash
$ pip install tofu-printer
```

or you can install with python poetry from source code.

``` bash
$ git clone https://github.com/argonism/Tofu.git
$ cd Tofu
$ poetry install
```

## Usage

### printer as API endpoint
``` bash
$ cd Tofu
$ TOFU_PRINTER_IP={Put your printer IP address here}
$ uvicorn tofu.api:app --port 1885 --host 0.0.0.0
```

### in python

``` python
from tofu.printer import Tofu, TofuText
tofu_printer = Tofu.from_network()
with tofu_printer:
    texts = [
        TofuText("hello tofu!").center().bold(),
        TofuText("tofu is a food prepared by coagulating soy milk.").right()
    ]
    tofu_printer.print_sequence(texts)
```
