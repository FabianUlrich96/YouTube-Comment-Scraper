FROM continuumio/miniconda3
RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y build-essential

COPY requirements.txt /
RUN ["conda", "create", "-n", "flaskenv", "python=3.7"]

RUN /bin/bash -c "source activate flaskenv  && pip install --trusted-host pypi.python.org -r /requirements.txt"

WORKDIR /flaskapp

COPY . ./

EXPOSE 5000
EXPOSE 1020

CMD /bin/bash -c "source activate flaskenv && python -u app.py"
