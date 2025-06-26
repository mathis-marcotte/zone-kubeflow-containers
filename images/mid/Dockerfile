USER root

# APT operations
RUN wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        build-essential \
        gdb \
        sqlite3 \
        openmpi-bin \
        libopenmpi-dev \
        software-properties-common \
        dirmngr \
        gdebi-core \
        r-base \
        r-base-core \
        r-recommended \
        r-base-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install vscode and cleanup
ARG VSCODE_VERSION=4.99.4
ARG VSCODE_SHA=74c107b33643ed11223263b86431530fbc9c9f7c8202997579a6f0c41b4cb102
ARG VSCODE_URL=https://github.com/coder/code-server/releases/download/v${VSCODE_VERSION}/code-server_${VSCODE_VERSION}_amd64.deb

ENV CS_DISABLE_FILE_DOWNLOADS=1
ENV CS_TEMP_HOME=/etc/share/code-server
ENV CS_DEFAULT_HOME=$HOME/.local/share/code-server
ENV SERVICE_URL=https://extensions.coder.com/api

RUN wget -q "${VSCODE_URL}" -O ./vscode.deb && \
    echo "${VSCODE_SHA}  ./vscode.deb" | sha256sum -c - && \
    wget -q https://github.com/microsoft/vscode-cpptools/releases/download/v1.20.5/cpptools-linux.vsix && \
    dpkg -i ./vscode.deb && \
    rm ./vscode.deb && \
    rm -f /etc/apt/sources.list.d/vscode.list && \
    mkdir -p $CS_TEMP_HOME/Machine && \
    code-server --install-extension ms-python.python@2025.4.0 && \
    code-server --install-extension ms-python.debugpy@2025.4.0 && \
    code-server --install-extension REditorSupport.r@2.8.4 && \
    code-server --install-extension ms-ceintl.vscode-language-pack-fr@1.91.0 && \
    code-server --install-extension quarto.quarto@1.113.0 && \
    code-server --install-extension dvirtz.parquet-viewer@2.9.0 && \
    code-server --install-extension redhat.vscode-yaml@1.15.0 && \
    code-server --install-extension ms-vscode.azurecli@0.6.0 && \
    code-server --install-extension mblode.pretty-formatter@0.2.1 && \
    code-server --install-extension cpptools-linux.vsix && \
    rm cpptools-linux.vsix && \
    mv $CS_DEFAULT_HOME/* $CS_TEMP_HOME && \
    fix-permissions $CS_TEMP_HOME

# Environment and config setup
ENV EXTENSIONS_GALLERY='{"serviceUrl":"https://code-marketplace.das-prod-cc-00.cloudnative.cloud.statcan.ca/api",
                         "itemUrl":"https://code-marketplace.das-prod-cc-00.cloudnative.cloud.statcan.ca/item",
                         "resourceUrlTemplate":"https://code-marketplace.das-prod-cc-00.cloudnative.cloud.statcan.ca/files/{publisher}/{name}/{version}/{path}"}'
COPY vscode-overrides.json $CS_TEMP_HOME/Machine/settings.json
COPY languagepacks.json $CS_TEMP_HOME/
COPY coder.json $CS_TEMP_HOME/

# Conda and Jupyter setup
RUN pip install 'git+https://github.com/betatim/vscode-binder' && \
    mamba install --quiet --yes -c conda-forge \
        'nodejs' \
        'pkg-config' \
        'jupyterlab' \
        'jupyter_contrib_nbextensions' \
        'dash' \
        'plotly' \
        'ipywidgets' \
        'markupsafe' \
        'pyspark==3.5.5' \
        'ipympl' \
        'pexpect==4.9.0' \
        'jupyter-resource-usage' \
        'jupyter-server-proxy==4.2.0' \
        'jupyterlab-language-pack-fr-fr' \
        'jupyterlab_execute_time' \
        'nb_conda_kernels' \
        'jupyterlab-lsp' \
        'jupyter-lsp' \
        'r-arrow' \
        'r-aws.s3' \
        'r-base=4.4.1' \
        'r-catools' \
        'r-e1071' \
        'r-hdf5r' \
        'r-markdown' \
        'r-odbc' \
        'r-renv' \
        'r-rodbc' \
        'r-sf' \
        'r-sparklyr' \
        'r-tidyverse' && \
    jupyter server extension enable --py jupyter_server_proxy && \
    jupyter nbextension enable codefolding/main --sys-prefix && \
    jupyter labextension enable \
        '@jupyterlab/translation-extension' \
        '@jupyterlab/server-proxy' \
        'nbdime-jupyterlab' && \
    jupyter lab build && \
    jupyter lab clean && \
    clean-layer.sh && \
    rm -rf /home/$NB_USER/.cache/yarn /home/$NB_USER/.node-gyp && \
    fix-permissions $CONDA_DIR /home/$NB_USER

# Language servers
RUN julia -e 'using Pkg; Pkg.add("LanguageServer")' && \
    /opt/conda/bin/R --silent --slave --no-save --no-restore -e 'install.packages("languageserver", repos="https://cran.r-project.org/")' && \
    mamba install -c conda-forge 'python-lsp-server' && \
    npm i -g \
        'bash-language-server' \
        'dockerfile-language-server-nodejs' \
        'javascript-typescript-langserver' \
        'unified-language-server' \
        'yaml-language-server' && \
    npm cache clean --force && \
    clean-layer.sh && \ 
    fix-permissions $CONDA_DIR /home/$NB_USER

# OpenM++ installation with cleanup
ARG OMPP_VERSION="1.17.5"
ARG OMPP_PKG_DATE="20241021"
ARG SHA256ompp=79c4bf6e09c9c51f33986251f1f44279f29d4fe669b6e8f7d7597a406d24b5a9
ENV OMPP_INSTALL_DIR=/opt/openmpp/${OMPP_VERSION}

COPY jupyter-ompp-proxy/ /opt/jupyter-ompp-proxy/

RUN wget -q https://github.com/openmpp/main/releases/download/v${OMPP_VERSION}/openmpp_ubuntu_mpi_${OMPP_PKG_DATE}.tar.gz -O /tmp/ompp.tar.gz && \
    echo "${SHA256ompp} /tmp/ompp.tar.gz" | sha256sum -c - && \
    mkdir -p ${OMPP_INSTALL_DIR} && \
    tar -xf /tmp/ompp.tar.gz -C ${OMPP_INSTALL_DIR} --strip-components=1 && \
    rm /tmp/ompp.tar.gz && \
    sed -i -e 's/history/hash/' ${OMPP_INSTALL_DIR}/ompp-ui/quasar.config.js && \
    sed -i -e "s/OMS_URL:.*''/OMS_URL: '.'/" ${OMPP_INSTALL_DIR}/ompp-ui/quasar.config.js && \
    npm install --prefix ${OMPP_INSTALL_DIR}/ompp-ui @babel/traverse@7.23.2 && \
    npm run build --prefix ${OMPP_INSTALL_DIR}/ompp-ui && \
    rm -r ${OMPP_INSTALL_DIR}/html && \
    mv ${OMPP_INSTALL_DIR}/ompp-ui/dist/spa ${OMPP_INSTALL_DIR}/html && \
    rm -rf ${OMPP_INSTALL_DIR}/ompp-ui && \
    fix-permissions ${OMPP_INSTALL_DIR} && \
    pip install /opt/jupyter-ompp-proxy/

# MinIO Client
COPY --from=minio/mc:RELEASE.2024-11-17T19-35-25Z /bin/mc /usr/local/bin/mc

# Jupyter config
COPY jupyterlab-overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json
ENV DEFAULT_JUPYTER_URL=/lab
ENV GIT_EXAMPLE_NOTEBOOKS=https://gitlab.k8s.cloud.statcan.ca/business-transformation/aaw/aaw-contrib-jupyter-notebooks

# RStudio installation
ARG RSTUDIO_VERSION=2024.12.0-467
ARG SHA256=1493188cdabcc1047db27d1bd0e46947e39562cbd831158c7812f88d80e742b3

RUN curl --silent -L --fail "https://s3.amazonaws.com/rstudio-ide-build/server/jammy/amd64/rstudio-server-${RSTUDIO_VERSION}-amd64.deb" > /tmp/rstudio.deb && \
    echo "${SHA256} /tmp/rstudio.deb" | sha256sum -c - && \
    apt-get install -y /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb && \
    mkdir -p /etc/rstudio && \
    echo "www-frame-origin=none" >> /etc/rstudio/rserver.conf && \
    echo "www-enable-origin-check=1" >> /etc/rstudio/rserver.conf && \
    echo "www-same-site=lax" >> /etc/rstudio/rserver.conf && \
    echo "restrict-directory-view=1" >> /etc/rstudio/rsession.conf && \
    echo "session-default-working-dir=/home/jovyan/workspace" >> /etc/rstudio/rsession.conf && \
    echo "session-default-new-project-dir=/home/jovyan/workspace" >> /etc/rstudio/rsession.conf && \
    echo "rsession-ld-library-path=/opt/conda/lib" >> /etc/rstudio/rserver.conf

ENV PATH=$PATH:/usr/lib/rstudio-server/bin
ENV SPARK_HOME="/opt/conda/lib/python3.12/site-packages/pyspark"

# Python package management
RUN pip install \
        'jupyter-rsession-proxy==2.2.0' \
        'wheel==0.40.0' \
        'setuptools==67.6.0' \
        'pyjwt==2.6.0' \
        'oauthlib==3.2.2' \
        'mpmath==1.3.0' \
        'lxml==5.3.1' \
        'pyarrow==14.0.1' \
        'cryptography==41.0.6' && \
    fix-permissions $CONDA_DIR /home/$NB_USER

# Final environment setup
ENV DEFAULT_JUPYTER_URL="/rstudio"
ENV GIT_EXAMPLE_NOTEBOOKS=https://gitlab.k8s.cloud.statcan.ca/business-transformation/aaw/aaw-contrib-r-notebooks.git
