FROM python:3.5.2

MAINTAINER @joshuacook

# Pick up some TF dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python3-dev \
        rsync \
        software-properties-common \
        unzip \
        libgtk2.0-0 \
        openssh-server \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh tmp/Miniconda3-4.2.12-Linux-x86_64.sh
RUN bash tmp/Miniconda3-4.2.12-Linux-x86_64.sh -b
ENV PATH $PATH:/root/miniconda3/bin/

COPY environment.yml .
RUN conda env create -f environment.yml

# Cleanup tarballs and downloaded package files
RUN conda clean -tp -y

RUN git clone https://github.com/mwolfram/cv_workbench.git

# Allow root access over ssh
RUN echo "root:Docker!" | chpasswd
RUN sed -i '/PermitRootLogin without-password/c\PermitRootLogin yes' /etc/ssh/sshd_config

# TensorBoard
EXPOSE 6006
# Flask Server
EXPOSE 4567
# SSH
EXPOSE 6666

ENV PATH=$PATH:/root/miniconda3/bin/

RUN bash -c "echo 'export PATH=$PATH:/root/miniconda3/bin/' >> /root/.bashrc"
RUN bash -c "echo 'source activate cv-workbench' >> /root/.bashrc"

CMD cd cv_workbench && git pull && /etc/init.d/ssh start &&  bash
