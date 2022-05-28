FROM python:3.7-buster

RUN apt-get update && apt-get install -y \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install \
    pipenv

WORKDIR /

COPY Pipfile .

#RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --skip-lock
RUN pipenv install --skip-lock

ENV PYTHONPATH "${PYTHONPATH}:/src"

COPY src .

CMD ["pipenv", "run", "python3", "test.py"]