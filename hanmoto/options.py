from argparse import ArgumentParser, Namespace, _SubParsersAction

from hanmoto.exceptions import HmtValueException
from hanmoto.printer import (
    HmtConf,
    HmtNetworkConf,
    HmtPrinterConf,
    HmtPrinterType,
)


def subparse_network(subparsers: _SubParsersAction) -> None:
    parser_network = subparsers.add_parser(
        "network", help="connect with network"
    )

    parser_network.add_argument(
        "--host",
        default="",
        type=str,
        help="printer hostname or ip addr",
    )

    parser_network.add_argument(
        "-p",
        "--port",
        default=9100,
        type=int,
        help="printer port number",
    )

    parser_network.add_argument(
        "-t",
        "--timeout",
        default=60,
        type=int,
        help="timeout in seconds for the escpos-library",
    )


def subparse_dummy(subparsers: _SubParsersAction) -> None:
    subparsers.add_parser("dummy", help="use dummy printer")


def parse_options() -> Namespace:
    parser = ArgumentParser(
        description="hanmoto makes your esc/pos printer accessible through Web API endpoint"
    )
    subparsers = parser.add_subparsers(
        dest="printer_type", help="printer connection type"
    )
    subparse_network(subparsers)

    args = parser.parse_args()
    return args


def load_conf_from_cli() -> HmtConf:
    args = parse_options()
    args_dict = vars(args)
    printer_type_str = args_dict.pop("printer_type")
    if printer_type_str is None:
        raise HmtValueException(
            f"No printer type specified. Choose printer type you goning to use from:{HmtPrinterType.get_types()}"
        )
    printer_type = HmtPrinterType[printer_type_str]
    printer_conf = HmtPrinterConf()
    if printer_type is HmtPrinterType.network:
        printer_conf = HmtPrinterConf(
            printer_type=printer_type, conf=HmtNetworkConf(**args_dict)
        )
    else:
        raise HmtValueException(f"Unknown printer type: {printer_type}")

    return HmtConf(printer_conf=printer_conf)


if __name__ == "__main__":

    print(load_conf_from_cli())
