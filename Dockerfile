FROM python:3.11 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./src .

# update PATH environment variable
ENV PATH=/root/.local:$PATH

ENTRYPOINT [ "python", "auto_submit_tips.py" ]
