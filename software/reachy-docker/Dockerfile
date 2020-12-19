FROM ekkus93/ubuntu_desktop:latest
LABEL maintainer="phillipcchin@gmail.com"

RUN sed -i 's#http://archive.ubuntu.com/ubuntu/#mirror://mirrors.ubuntu.com/mirrors.txt#' /etc/apt/sources.list

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y

# mqtt
RUN apt-get update && \
    apt-get install mosquitto mosquitto-clients -y
#COPY ./mqtt_passwd.txt /tmp/mosquitto_passwd.txt
#RUN mosquitto_passwd -c /tmp/mqtt_passwd.txt
#RUN echo "\nallow_anonymous false\npassword_file" >> /etc/mosquitto/passwd

# Anaconda
COPY ./Anaconda3-2020.07-Linux-x86_64.sh /tmp/
#RUN curl https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh -s -o /tmp/Anaconda3-2020.07-Linux-x86_64.sh
RUN cd /tmp && bash ./Anaconda3-2020.07-Linux-x86_64.sh -b -p /opt/anaconda && rm Anaconda3-2020.07-Linux-x86_64.sh
RUN /opt/anaconda/bin/conda update -n base conda
RUN /opt/anaconda/bin/conda install pip
RUN /opt/anaconda/bin/pip install --upgrade pip
RUN apt-get install -y swig

# create reachy user
RUN useradd -ms /bin/bash reachyuser
RUN echo "reachyuser:makinghardwarelesshard*" | chpasswd

SHELL ["/bin/bash", "-c"]

# set sudo for reachyuser
RUN usermod -aG sudo reachyuser
RUN chmod u+w /etc/sudoers && \
    sed -i "s#%sudo\s*ALL=(ALL:ALL)\s*ALL#%sudo   ALL=(ALL:ALL) NOPASSWD:ALL#" /etc/sudoers && \
    chmod u-w /etc/sudoers

COPY environment.yml /tmp
RUN chown reachyuser /tmp/environment.yml

COPY ./run.sh /tmp
RUN chown reachyuser /tmp/run.sh
COPY ./run_reachy.sh /tmp
RUN chown reachyuser /tmp/run_reachy.sh

USER reachyuser
WORKDIR /home/reachyuser

RUN cd /tmp && /opt/anaconda/bin/conda env create -f environment.yml && rm -f environment.yml
ENV PATH /opt/anaconda/bin:$PATH

SHELL ["/bin/bash", "-c"]

RUN echo "export PATH=$PATH:/usr/sbin" >> /home/reachyuser/.bashrc
RUN echo "source activate reachy-docker" >> /home/reachyuser/.bashrc
RUN echo "export PATH=$PATH:/usr/sbin" >> /home/reachyuser/.bash_profile
RUN echo "source activate reachy-docker" >> /home/reachyuser/.bash_profile

RUN /opt/anaconda/bin/conda init bash

USER root

RUN /opt/anaconda/bin/conda init bash

ENV TERM xterm-256color
VOLUME ["/reachy"]

RUN chmod ugo+x /tmp/run.sh
CMD ["/tmp/run.sh"]