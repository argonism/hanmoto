from hanmoto import Hanmoto, HmtImage


def print_image(printer_host: str, image_path: str) -> None:
    hmt = Hanmoto.from_network("en", printer_host)
    img = HmtImage(image_path)
    with hmt:
        hmt.print_sequence([img])


if __name__ == "__main__":
    image_path = "tests/resources/salt.png"
    printer_host = "192.168.xx.xx"
    print_image(printer_host, image_path)
