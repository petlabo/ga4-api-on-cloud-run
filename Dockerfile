# Pythonの公式イメージを使用
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# Gunicornを使用してアプリケーションを起動
# PORT環境変数はCloud Runによって自動的に設定されます
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
