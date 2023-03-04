from argparse import ArgumentParser, Namespace, _SubParsersAction


def subparse_network(subparsers: _SubParsersAction) -> None:
    parser_network = subparsers.add_parser(
        "network", help="connect with network"
    )

    parser_network.add_argument(
        "host",
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


def server_options(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--api_host",
        default="127.0.0.1",
        type=str,
        help="fastapi app server port to listen",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=10002,
        type=int,
        help="fastapi app server port to listen",
    )
    parser.add_argument(
        "--reload",
        default=False,
        action="store_true",
        help="same as fastapi --reload option. \
            if true, source code changes will be reflected immediately",
    )


def parse_options() -> Namespace:
    parser = ArgumentParser(
        description="hanmoto makes your esc/pos printer accessible through Web API endpoint"
    )
    server_options(parser)

    subparsers = parser.add_subparsers(
        dest="printer_type", help="printer connection type"
    )
    subparse_network(subparsers)
    subparse_dummy(subparsers)

    args = parser.parse_args()
    return args
