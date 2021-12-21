FROM continuumio/miniconda3

SHELL ["/bin/bash", "--login", "-c"]

COPY environment.yml /environment.yml
RUN set -ex && \
    conda env create -f /environment.yml
RUN conda init bash
RUN echo "conda activate vendors" >> ~/.bashrc
ENV BASH_ENV ~/.bashrc

RUN mkdir -p ppcf/vendors
RUN mkdir -p ppcf/shared
RUN mkdir -p ppcf/mediator/app/data


COPY app/data/public_key.pk ppcf/shared
COPY app/data/similarity_matrix.npy ppcf/mediator/app/data
COPY app/data/encrypted_mask.npy ppcf/mediator/app/data
COPY app/data/encrypted_user_item_matrix.npy ppcf/mediator/app/data

COPY . ppcf/vendors

WORKDIR ppcf/vendors

ENTRYPOINT ["./entrypoint.sh"]
