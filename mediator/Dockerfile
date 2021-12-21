FROM continuumio/miniconda3

SHELL ["/bin/bash", "--login", "-c"]

COPY environment.yml /environment.yml
RUN set -ex && \
    conda env create -f /environment.yml
RUN conda init bash
RUN echo "conda activate mediator" >> ~/.bashrc
ENV BASH_ENV ~/.bashrc

RUN mkdir -p ppcf/mediator
RUN mkdir -p ppcf/shared

COPY app/data/public_key.pk ppcf/shared

COPY . ppcf/mediator

WORKDIR ppcf/mediator

ENTRYPOINT ["./entrypoint.sh"]
