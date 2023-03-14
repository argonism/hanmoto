import uvicorn

from hanmoto.api import load_app
from hanmoto.config import (
    HmtApiConf,
    HmtConf,
    HmtDummyConf,
    HmtNetworkConf,
    HmtPrinterConf,
    HmtPrinterType,
)
from hanmoto.exceptions import HmtValueException
from hanmoto.options import parse_options


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
            printer_type=printer_type,
            conf=HmtNetworkConf(**args_dict),
            lang=args.lang,
        )
    elif printer_type is HmtPrinterType.dummy:
        printer_conf = HmtPrinterConf(
            printer_type=printer_type,
            conf=HmtDummyConf(**args_dict),
            lang=args.lang,
        )
    else:
        raise HmtValueException(f"Unknown printer type: {printer_type}")

    api_conf = HmtApiConf(**args_dict)
    return HmtConf(printer_conf=printer_conf, api_conf=api_conf)


def run() -> None:
    conf = load_conf_from_cli()
    app = load_app(conf)
    api_conf = conf.api_conf
    uvicorn.run(
        app,
        host=api_conf.api_host,
    )
