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
    else:
        path_directory = Path("/tmp/").resolve()

    if not path_directory.exists():
        print(f"[Directory] '{path_directory} does not exist. Creating it...'")
        path_directory.mkdir(parents=True, exist_ok=True)
    elif not path_directory.is_dir():
        raise NotADirectoryError(f"Error: '{path_directory}' is not a directory.")    

    server_config = ServerConfig(host="127.0.0.1",
                                 port=4221,
                                 root_dir=path_directory)
    print(f"[Serving files from] {server_config.root_dir}")

    Server(server_config).serve_forever()


if __name__ == "__main__":
    main()
