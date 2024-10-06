#!/usr/bin/env python3

import argparse 
import functools
import subprocess
import sys

def setup_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('application', type=str)
    return parser.parse_args()

def get_manpage_path(application: str) -> str:
    cp: subprocess.CompletedProcess = subprocess.run(['man', '-w', application],
                                                     capture_output=True,
                                                     text=True)
    if cp.returncode != 0:
        print(cp.stderr, file=sys.stderr)
        return None

    return cp.stdout.strip()

def convert_manpage(application: str, manpage_path: str) -> str:
    args: list = ['pandoc', '-i', manpage_path, '-f', 'man', '-t', 'asciidoc']
    cp: subprocess.CompletedProcess = subprocess.run(args, capture_output=True,
                                                     text=True)
    if cp.returncode != 0:
        print(cp.stderr, file=sys.stderr)
        return None

    return cp.stdout

def convert_asciidoc_to_html(application: str) -> bool:
    cp: subprocess.CompletedProcess = (
        subprocess.run(
            args=['asciidoctor', f'{application}.adoc'],
            capture_output=True,
            text=True
        )
    )
    if cp.returncode != 0:
        print(cp.err, file=sys.stderr)
        return False
    else:
        print(cp.stdout)
        return True

def save_as_asciidoc(application, asciidoc_text) -> None:
    with open(f'{application}.adoc', mode='w') as fp:
        printf = functools.partial(print, file=fp)
        printf(f'= {application} man page')
        printf(':toc: left')
        printf(':toclevels: 5')
        printf(':linkcss:')
        printf(':css: asciidoc.css')
        printf()
        printf(asciidoc_text)

def main():
    args: argparse.Name = setup_cli()
    application = args.application
    if not (manpage_path := get_manpage_path(application)):
        sys.exit(1)
    if not (asciidoc_text := convert_manpage(application, manpage_path)):
        sys.exit(1)
    save_as_asciidoc(application, asciidoc_text)
    if not convert_asciidoc_to_html(application):
        sys.exit(1)

if __name__ == '__main__':
    main()