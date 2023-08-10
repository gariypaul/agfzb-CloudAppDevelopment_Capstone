import json
from flask import Flask, request, jsonify
from cloudant.client import Cloudant

app = Flask(__name__)

# Simulated secret information
secret = {
    "URL": "https://a7637d95-13fd-4d36-bd33-c43326d44b48-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "KvcAgqnvLvK8TRAqUujdAmrtR8mVwTjK2yHxDBDU9GQ1",
    "ACCOUNT_NAME": "a7637d95-13fd-4d36-bd33-c43326d44b48-bluemix",
}

# Simulated Cloudant connection
client = Cloudant.iam(
    account_name=secret["ACCOUNT_NAME"],
    api_key=secret["IAM_API_KEY"],
    url=secret["URL"],
    connect=True,
)
my_database = client["reviews"]

@app.route('/review', methods=['POST'])
def invoke_review():
    try:
        data = request.json
        dealer_id = data.get("dealerId")
        
        if dealer_id is None:
            return jsonify({
                'statusCode': 400,
                'message': "Missing 'dealerId' parameter"
            })

        selector = {'dealership': {'$eq': int(dealer_id)}}
        result_by_filter = my_database.get_query_result(selector, raw_result=True)

        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': result_by_filter}
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'statusCode': 500,
            'message': "Something went wrong",
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
