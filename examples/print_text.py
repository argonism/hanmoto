from hanmoto import Hanmoto, HmtText


def print_text(printer_host: str, text: str) -> None:
    hmt = Hanmoto.from_network("jp", printer_host)
    text_hmt = HmtText(text)
    with hmt:
        hmt.print_sequence([text_hmt])


if __name__ == "__main__":
    text = "Kept you waiting, huh?"
    printer_host = "192.168.xxx.xxx"
    print_text(printer_host, text)
