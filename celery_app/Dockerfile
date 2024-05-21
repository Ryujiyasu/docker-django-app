FROM python:3.12.3-alpine3.19

ENV PYTHONUNBUFFERED 1

# 必要なパッケージをインストールする
RUN apk add --update --no-cache \
    mariadb-connector-c-dev \
    gcc \
    musl-dev \
    python3-dev \
    libc-dev \
    linux-headers \
    bash  # ここで bash を追加インストール

# 作業ディレクトリとポートの設定
WORKDIR /usr/src/app
EXPOSE 8000

# 依存関係をインストールする
COPY ./requirements.txt /requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

# アプリケーションのソースコードをコピー
COPY . /usr/src/app

# ユーザーを追加してパーミッションを変更する
RUN adduser --disabled-password --no-create-home app && \
    chown -R app:app /usr/src/app

# パスを設定してユーザーを切り替える
ENV PATH="/py/bin:$PATH"
USER app