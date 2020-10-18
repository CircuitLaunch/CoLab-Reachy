FROM ubuntu:18.04
LABEL maintainer="phillipcchin@gmail.com"

RUN apt-get update && apt-get upgrade -y
RUN apt-get install wget screen bzip2 curl -y

RUN apt-get install build-essential -y
RUN apt-get install emacs -y

# Anaconda
# COPY ./Anaconda3-2020.07-Linux-x86_64.sh /tmp/
RUN curl https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh -s -o /tmp/Anaconda3-2020.07-Linux-x86_64.sh
RUN cd /tmp && bash ./Anaconda3-2020.07-Linux-x86_64.sh -b -p /opt/anaconda && rm Anaconda3-2020.07-Linux-x86_64.sh
RUN /opt/anaconda/bin/conda update -n base conda
RUN /opt/anaconda/bin/conda install pip
RUN /opt/anaconda/bin/pip install --upgrade pip

COPY environment.yml /tmp
RUN cd /tmp && /opt/anaconda/bin/conda env create -f environment.yml && rm environment.yml
ENV PATH /opt/anaconda/bin:$PATH

SHELL ["/bin/bash", "-c"]

RUN echo "source activate reachy-docker" >> ~root/.bashrc

ENV TERM xterm-256color
VOLUME ["/reachy"]

COPY ./run.sh /tmp
RUN chmod ugo+x /tmp/run.sh
CMD ["/tmp/run.sh"]