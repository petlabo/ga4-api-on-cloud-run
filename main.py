import os
from flask import Flask, jsonify, request
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest
)

app = Flask(__name__)

# Cloud Runからサービスアカウントへと認証が問い合わせされる。
client = BetaAnalyticsDataClient()

@app.route("/")
def get_ga4_report():
    try:
        # あなたのプロパティID 9桁ほどの数字
        property_id = os.environ.get("GA_PROPERTY_ID", "<YOUR-GA-PROPERTY-ID>")
        
        # パラメータの取得 (例: /?dimensions=city,country&metrics=activeUsers,sessions&start_date=2026-01-01&end_date=today)
        dim_param = request.args.get('dimensions', 'city').split(',')
        met_param = request.args.get('metrics', 'activeUsers').split(',')
        start_date = request.args.get('start_date', '2026-01-01')
        end_date = request.args.get('end_date', 'today')

        # リクエストオブジェクトの構築
        ga_request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name=name.strip()) for name in dim_param],
            metrics=[Metric(name=name.strip()) for name in met_param],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        )
        
        response = client.run_report(ga_request)
        
        # 取得したデータを動的に辞書形式に変換
        output = []
        for row in response.rows:
            row_data = {}
            # ディメンションの取得
            for i, dim in enumerate(dim_param):
                row_data[dim.strip()] = row.dimension_values[i].value
            # メトリクスの取得
            for i, met in enumerate(met_param):
                row_data[met.strip()] = row.metric_values[i].value
            
            output.append(row_data)
            
        return jsonify({
            "status": "success", 
            "parameters": {
                "dimensions": dim_param,
                "metrics": met_param,
                "date_range": [start_date, end_date]
            },
            "data": output
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
