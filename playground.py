from escpos.printer import Network


def jpInit(tofu: Network) -> Network:
    tofu.charcode("CP932")
    tofu._raw(b"\x1c\x43\x01")
    return tofu


def jpText(
    tofu: Network, txt: str, dw: bool = False, dh: bool = False
) -> None:
    tofu._raw(b"\x1c\x26")  # Kanji mode ON
    n = 0x00
    if dw:
        n += 0x04
    if dh:
        n += 0x08
    if n != 0x00:
        tofu._raw(b"\x1c\x21" + n.to_bytes(1, byteorder="big"))  # Char size ON
    tofu._raw(txt.encode("shift_jis", "ignore"))
    if n != 0x00:
        tofu._raw(b"\x1c\x21\x00")  # Char size OFF
    tofu._raw(b"\x1c\x2e")  # Kanji mode OFF


def main() -> None:
    tofu = Network("192.168.11.22")
    jpInit(tofu)
    jpText(tofu, "テキスト例１２３４５６７８９０1234567890")
    tofu.ln()
    # tofu.image("kdb_icon-export.png")
    # tofu.image("学生証筑波大学長之印.png", center=False)
    # tofu.barcode('1324354657687', 'EAN13', 64, 2, '', '')
    tofu.cut()


if __name__ == "__main__":
    main()
