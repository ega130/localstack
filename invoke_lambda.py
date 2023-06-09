import boto3
import base64
import json
from utils.choose_lambda_function import choose_lambda_function

# LocalStackのエンドポイントを指定
localstack_endpoint = 'http://localhost:4566'

# Lambdaクライアントを作成
# このクライアントは、LocalStackを使用してLambda関数を実行するために使用されます。
lambda_client = boto3.client('lambda', endpoint_url=localstack_endpoint, region_name='us-east-1')

# 登録済みのLambda関数一覧を取得
functions = lambda_client.list_functions()
function_names = [function['FunctionName'] for function in functions['Functions']]

# 関数を選択
selected_function = choose_lambda_function(function_names)

# eventディクショナリを作成
event = {}

if selected_function == "upload_image_lambda":
    # 標準入力からpng_image_pathを取得
    png_image_path = input("Enter the path to the PNG image: ")

    # 画像をbase64エンコード
    with open(png_image_path, 'rb') as file:
        png_image_base64 = base64.b64encode(file.read()).decode('utf-8')

    # eventディクショナリにpng_image_base64を追加
    event["png_image_base64"] = png_image_base64
elif selected_function == "full_name_lambda":
    # 標準入力からfirst_nameとlast_nameを取得
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")

    # eventディクショナリにfirst_nameとlast_nameを追加
    event["first_name"] = first_name
    event["last_name"] = last_name

# Lambda関数を実行してeventディクショナリを渡す
# LocalStackは、Lambda関数の実行イベントを受信し、新しい環境を開始します。
# Dockerコンテナ用のサービスエンドポイントが作成され、関数が実行されるエグゼキュータに割り当てられます。
# Lambda関数用のDockerコンテナが作成され、設定が適用されます。
# Lambda関数を実行するために必要なランタイムおよび依存関係がインストールされます。
response = lambda_client.invoke(
    FunctionName=selected_function,
    Payload=json.dumps(event)  # eventディクショナリをJSONに変換してPayload引数に渡す
)

# 実行が終了すると、invoke_lambda.py スクリプトの実行結果が出力されます。
# これにより、AWS Lambda関数が正しく実行されたことが確認できます。
output = response['Payload'].read().decode('utf-8')
print("Lambda output:", output)
