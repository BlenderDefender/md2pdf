FROM ubuntu:mantic

RUN apt-get update \
 && apt-get install --yes \
      pandoc \
      wkhtmltopdf \
      texlive \
      build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
 # https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
 && pip3 install --break-system-packages weasyprint \
    click\
    watchdog\
    pandoc-include\
    codebraid\
 && pandoc --version


RUN mkdir /app

COPY md2pdf.py /usr/bin/md2pdf
RUN chmod +x /usr/bin/md2pdf

# RUN curl https://github.com/KaTeX/KaTeX/releases/download/v0.16.10/katex.tar.gz -o ./katex.tar.gz && tar -xvzf ./katex.tar.gz -C /usr/share/javascript/katex/

# COPY ./katex/ /usr/share/javascript/katex/

WORKDIR /app
