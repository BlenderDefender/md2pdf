#!/usr/bin/env python3
import os
from os import path as p

import subprocess
import shutil

import click

import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


EXISTING_FILE = click.Path(exists=True, dir_okay=False, resolve_path=True)

def run_shell_command(command: str, log_msg: str = "", verbose_logging: bool = False) -> None:

    if log_msg:
        click.echo(log_msg)

    if verbose_logging:
        subprocess.call(command, shell=True)
        return

    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def convert(markdown_file: str, css_file: str, engine: str, generate_html: bool, verbose_logging: bool, math_engine: str) -> None:
    """Converts the markdown file to a PDF-document, using the given options.

    Args:
        markdown_file (str): The path to the markdown file.
        css_file (str): The path to the CSS stylesheet, may be "".
        engine (str): The engine to use for PDF-Generation
        generate_html (bool): Whether to generate the HTML file for easier styling.
        math_engine (str): Use a different math engine.
    """

    pdf_file = p.splitext(markdown_file)[0] + ".pdf"

    tmp_unprocessed_md = "/tmp/u_file.md"
    tmp_preprocessed_md = "/tmp/file.md"
    tmp_css = "/tmp/styles.css"
    
    tmp_pdf = "/tmp/file.pdf"
    tmp_html = "/tmp/file.html"


    if p.exists(tmp_unprocessed_md):
        os.remove(tmp_unprocessed_md)

    if p.exists(tmp_preprocessed_md):
        os.remove(tmp_preprocessed_md)

    if p.exists(tmp_css):
        os.remove(tmp_css)

    shutil.copy(markdown_file, tmp_unprocessed_md)
    run_shell_command(f"pandoc -f markdown --to markdown --filter pandoc-include --output={tmp_preprocessed_md} /tmp/u_file.md", verbose_logging=verbose_logging)
    run_shell_command(f"codebraid pandoc -f markdown --to markdown --output={tmp_preprocessed_md} /tmp/file.md  --overwrite --cache-dir=/tmp", verbose_logging=verbose_logging)

    convert = f"pandoc -f markdown --output={tmp_pdf} --pdf-engine={engine}"

    if css_file:
        shutil.copy(css_file, tmp_css)
        convert += f" --css={tmp_css}"

    if math_engine:
        convert += f" --{math_engine}"

    convert += f" {tmp_preprocessed_md}"

    run_shell_command(convert, f"Converting '{p.basename(markdown_file)}'...", verbose_logging)

    if generate_html:
        to_html = f"codebraid pandoc -f markdown --output={tmp_html} {tmp_preprocessed_md} --overwrite --cache-dir=/tmp"

        if math_engine:
            to_html += f" --{math_engine}"

        run_shell_command(to_html, "Generating HTML...", verbose_logging)

    if p.exists(pdf_file):
        os.remove(pdf_file)

    shutil.move(tmp_pdf, pdf_file)

    if p.exists(tmp_html):
        shutil.move(tmp_html,
                    p.splitext(pdf_file)[0] + ".html")

    click.echo(f"Sucessfully converted '{p.basename(markdown_file)}' to PDF!")

class EventHandler(FileSystemEventHandler):
    def __init__(self, markdown_file: str, css_file: str, *args):
        self.markdown_file = markdown_file
        self.css_file = css_file
        self.args = args

    def on_modified(self, event):
        if event.src_path in [self.markdown_file, self.css_file]:
            click.echo(f"{event.src_path} has changed")
            convert(self.markdown_file, self.css_file, *self.args)


@click.command()
@click.argument("md", type=EXISTING_FILE, nargs=-1)
@click.argument("css", type=EXISTING_FILE)
@click.option('-e', '--engine', default="weasyprint", help='The engine you want to use for converting the file to a PDF.  Defaults to "weasyprint"', type=click.Choice(["weasyprint", "wkhtmltopdf", "pdflatex"], case_sensitive=True))
@click.option('-w', '--watch', help='Watch the markdown file MD and the stylesheet CSS for changes.', is_flag=True)
@click.option('--generate-html', '-H', help='Output the generated HTML for easier editing of the CSS-Stylesheet.', is_flag=True)
@click.option('--verbose-logging', '-V', help='Print more detailed logs to the console.', is_flag=True)
@click.option('--math-engine', default="", help='Use one of these math engines for converting TeX Math. Defaults to an empty string.', type=click.Choice(["mathjax", "mathml", "webtex", "katex", "gladtex", ""], case_sensitive=True))
def cli(md: str, css: str, engine: str, watch: bool, generate_html: bool, verbose_logging: bool, math_engine: str):
    """Converts Markdown file MD and stylesheet CSS to a PDF document."""
    for f in md:
        convert(f, css, engine, generate_html, verbose_logging, math_engine)

    if watch:
        observer = Observer()

        for f in md:
            click.echo(f"Watching {f} and {css} for changes. Press CTRL+C to quit.")

            markdown_path = os.path.dirname(f)
            css_path = os.path.dirname(css)


            event_handler = EventHandler(
                f, css, engine, generate_html, verbose_logging, math_engine)
            observer.schedule(event_handler, markdown_path)

            if markdown_path != css_path:
                observer.schedule(event_handler, css_path)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    cli()
