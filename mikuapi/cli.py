# mikuapi/cli.py

import argparse
import uvicorn
import sys
import os
sys.path.append(os.getcwd())

VERSION = "0.1.0"


def run_server(args):
    print("\nMikuAPI")
    print("-" * 40)
    print(f"Application : {args.target}")
    print(f"Host        : {args.host}")
    print(f"Port        : {args.port}")
    print(f"Reload      : {args.reload}")
    print("-" * 40)
    print(f"Running on http://{args.host}:{args.port}\n")

    uvicorn.run(
        args.target,
        host=args.host,
        port=args.port,
        reload=args.reload
    )


def show_info(_):
    print("\nMikuAPI")
    print("-" * 40)
    print("A lightweight Python web framework")
    print(f"Version : {VERSION}")
    print("-" * 40 + "\n")


def show_version(_):
    print(VERSION)


def create_parser():
    parser = argparse.ArgumentParser(
        prog="mikuapi",
        description="MikuAPI Command Line Interface"
    )

    sub = parser.add_subparsers(dest="command")

    # run
    run = sub.add_parser("run", help="Run application")
    run.add_argument("target", help="module:app (example: main:app)")
    run.add_argument("--host", default="127.0.0.1")
    run.add_argument("--port", type=int, default=8000)
    run.add_argument("--reload", action="store_true")
    run.set_defaults(func=run_server)

    # info
    info = sub.add_parser("info", help="Show framework info")
    info.set_defaults(func=show_info)

    # version
    version = sub.add_parser("version", help="Show version")
    version.set_defaults(func=show_version)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\nStopped\n")
    except Exception as e:
        print(f"\nError: {e}\n")