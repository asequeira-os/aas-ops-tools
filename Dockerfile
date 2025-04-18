FROM python:3.12.10-slim-bookworm
ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN apt-get update

# RUN apt install -y gcc g++ make curl wget git file tree vim emacs
# RUN apt install -y postgresql-client lsof unzip
RUN apt install -y curl git

# RUN pip install pipenv
# ENV _FORCE_AAS_BUILD=1

RUN mkdir -p /aas-docker
COPY scripts /aas-docker/
WORKDIR /aas-docker

RUN ./install-all.sh
COPY README.md /aas-docker

# # single quotes are important since $PATH should not expand
RUN echo 'export PS1="ops-tools ${PS1}"' >> /root/.bashrc
RUN echo 'export PATH=/root/go/bin:${PATH}' >> /root/.bashrc

WORKDIR /top

ENTRYPOINT [ "/aas-docker/entrypoint" ]
