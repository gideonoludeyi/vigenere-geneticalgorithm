import sys
import argparse
import pathlib

from geneticalgorithm.utils import decrypt


parser = argparse.ArgumentParser(
    prog="Decrypt")

parser.add_argument(
    "key",
    help="the key to use to decrypt the encrypted text",
    type=str)

parser.add_argument(
    "-f", "--file",
    dest="filepath",
    help="filepath to the encrypted data. [default: read from stdin]",
    type=pathlib.Path)


def main() -> int:
    args = parser.parse_args()

    if args.filepath is not None:
        with open(args.filepath) as f:
            text = f.read()
    else:
        text = "".join(sys.stdin)

    print(decrypt(args.key, text))

    return 0


if __name__ == "__main__":
    sys.exit(main())
