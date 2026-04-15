# GA4 Cloud Run Reporting API

Google Analytics4(GA4)のデータをクエリパラメータで柔軟に取得できる、Cloud Run用のFlaskアプリケーションです。

## 1. サービスアカウントの作成と権限設定

Cloud RunからGA4にアクセスするために、サービスアカウントの設定が必要です。

### ① Google Cloud でのサービスアカウント作成
1. [Google Cloud Console](https://console.cloud.google.com/) の「IAM と管理」>「サービスアカウント」に移動します。
2. 「サービスアカウントを作成」をクリックします。
3. 名前（例: `ga4-reporter`）を入力し、作成します。
4. **ロールの割り当ては不要です**（GA4側の設定で権限を付与します）。
5. 作成したサービスアカウントの **メールアドレス** をコピーしておきます。

### ② Google Analytics4 での閲覧権限付与
1. [Google Analytics](https://analytics.google.com/) にログインし、対象のプロパティの「管理」を開きます。
2. プロパティ列の「プロパティのアクセス管理」をクリックします。
3. 「＋」ボタン >「ユーザーを追加」をクリックします。
4. 先ほどコピーした **サービスアカウントのメールアドレス** を入力します。
5. 役割として **「閲覧者」** を選択し、追加します。

## 2. デプロイ手順

`gcloud`を使用して、Cloud Runにデプロイします。
## 2. デプロイ手順

### ① Google Cloudプロジェクトの設定
1. [Google Cloudコンソール](https://console.cloud.google.com/) にアクセスします。
2. 検索バーで **「APIとサービス」** を検索し、「有効な API とサービス」を開きます。
3. 「＋ APIとサービスの有効化」をクリックします。
4. 以下の2つのAPIを検索し、それぞれ **「有効にする」** をクリックします。
   - **Cloud Run Admin API**
   - **Artifact Registry API**
   - **Google Analytics Data API**
  ※前者2点は基本的に有効化されている。

### ② デプロイの実行
ディレクトリ内で以下のコマンドを実行します。

```bash
gcloud run deploy ga4-report-service \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars GA_PROPERTY_ID=[GA4側のID] \
  --service-account [作成したサービスアカウントのメールアドレス] \
  --project [プロジェクトID]
```

## 3. APIの使い方

デプロイ後に発行される URL（例: `https://ga4-xxx.run.app/`）にパラメータを付けてアクセスします。

### パラメータの指定方法
1 つ目のパラメータは `?` で始め、2 つ目以降は `&` で繋ぎます。
- `dimensions`: 取得したいディメンション（カンマ区切り）。例: `city,deviceCategory`
- `metrics`: 取得したいメトリクス（カンマ区切り）。例: `activeUsers,sessions`
- `start_date`: 開始日（YYYY-MM-DD または `30daysAgo` など）。
- `end_date`: 終了日。

### リクエスト例
```text
https://[YOUR-CLOUD-RUN-URL]/?dimensions=city,country&metrics=activeUsers,sessions&start_date=2026-01-01&end_date=today
```
*※パラメータの順番は自由です。*

## ディレクトリ構成
- `main.py`: アプリケーション本体（パラメータ処理・GA4クエリ実行）
- `requirements.txt`: Pythonパッケージ依存関係
- `Dockerfile`: コンテナイメージ作成用設定
- `README.md`: このドキュメント
