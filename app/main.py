from .server import Server
from .config import ServerConfig
from pathlib import Path
import argparse



def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--directory", help="Absolute path to the file directory.")
    args = parser.parse_args()
            
    try:
        if args.directory:
            path_directory = Path(args.directory).resolve()
        else:
            path_directory = None

    except FileNotFoundError:
        print(f"Error: Directory '{args.directory}' does not exist.")
        return
    
    server_config = ServerConfig(host="127.0.0.1",
                                        port=4221,
                                        directory=path_directory)

    Server(server_config).serve_forever()


if __name__ == "__main__":
    main()
