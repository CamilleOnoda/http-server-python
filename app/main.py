from .server import Server
from .config import ServerConfig
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--directory",
                        type=str,
                        help="Absolute path to the file directory.")
    args = parser.parse_args()

    if args.directory:
        path_directory = Path(args.directory).resolve(strict=False)
        if not path_directory.exists():
            raise FileNotFoundError(f"Error: Directory '{path_directory}' does not exist.")
        if not path_directory.is_dir():
            raise NotADirectoryError(f"Error: '{path_directory}' is not a directory.")        
    else:
        path_directory = Path("/tmp").resolve()

    server_config = ServerConfig(host="127.0.0.1",
                                 port=4221,
                                 root_dir=path_directory)
    print(f"Serving files from: {server_config.root_dir}")

    Server(server_config).serve_forever()


if __name__ == "__main__":
    main()
