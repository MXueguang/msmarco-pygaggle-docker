FROM python:3.6-slim

RUN mkdir -p /usr/share/man/man1 && \
    apt update && \
    apt install -y bash \
                   build-essential \
		   git \
                   curl \
                   ca-certificates \
	           openjdk-11-jdk-headless && \
    rm -rf /var/lib/apt/lists

WORKDIR /home
COPY requirements.txt /home/

RUN git clone https://github.com/castorini/pygaggle.git
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r pygaggle/requirements.txt \
    pip install --no-cache-dir -r requirements.txt

#RUN python -c "from pyserini.search import SimpleSearcher; SimpleSearcher.from_prebuilt_index('msmarco-doc-slim')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
