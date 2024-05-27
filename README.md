# Markdown to PDF

A Markdown to PDF converter based on Pandoc (and weasyprint), inspired by [spawnia/md-to-pdf](https://github.com/spawnia/md-to-pdf) and [ljpengelen/markdown-to-pdf](https://github.com/ljpengelen/markdown-to-pdf).

## Getting started

### Dependencies

If you want to use KaTeX, you need to download the release files [from the KaTeX GitHub repository](https://github.com/KaTeX/KaTeX/releases), extract them to `./katex` and update `Dockerfile`.

### Docker

It's recommended to use this tool from within a Docker container.
There is a pre-built image available on Dockerhub, you can pull it with

```sh
sudo docker pull blenderdefender/md2pdf
```

You can manually build an image by cloning this repository and executing the following command:

```sh
sudo docker build -t md2pdf .
```

After building the image, you can run it in a shell and attach the examples directory with the following command:

```sh
sudo docker run -it -v $(pwd)/examples:/app md2pdf bash
```

To generate a PDF version of the example CV, run

```sh
md2pdf cv.md cv.css
```

To display all available commands, run

```sh
md2pdf --help
```

## Supported features

### Pandoc Include

This tool supports including other files in your markdown documents using the syntax of [Pandoc Include.](https://github.com/DCsunset/pandoc-include?tab=readme-ov-file#syntax)

Basic syntax:

```
!include somefolder/somefile
```

For code blocks:

````markdown
```cpp
!include filename.cpp
```
````

Check the [Pandoc Include Repository](https://github.com/DCsunset/pandoc-include?tab=readme-ov-file#syntax) for more details.

### Codebraid

It's also possible to run code before converting the document by marking codeblocks with `{.language .cb-run}`

Example:

````markdown
```{.python .cb-run}
var = 'Hello from Python!'
var += ' $2^8 = {}$'.format(2**8)
```

```{.python .cb-run}
print(var)
```
````

Check the [Codebraid Repository](https://github.com/gpoore/codebraid?tab=readme-ov-file#code-options) for more details.

## CSS for print

If you want to design your own documents, take a look at [designing for print with CSS](https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/) by Rachel Andrew.
