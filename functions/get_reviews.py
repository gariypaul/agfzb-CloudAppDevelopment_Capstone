import json
from flask import Flask, request, jsonify
from cloudant.client import Cloudant

app = Flask(__name__)

secret = {
    "URL": "https://52c0d074-8afe-4d63-87f8-bd5e6d7e8ad8-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "klGbAyO_sHmbvPfn5x0eh4isZw0dR7Yms-Bcn6ko7kfv",
    "USER_NAME": "52c0d074-8afe-4d63-87f8-bd5e6d7e8ad8-bluemix",
}

# Simulated Cloudant connection
client = Cloudant.iam(
    account_name=secret["USER_NAME"],
    api_key=secret["IAM_API_KEY"],
    url=secret["URL"],
    connect=True,
)
my_database = client["reviews"]

@app.route('/reviews', methods=['GET'])
def invoke_review():
    try:
        dealer_id = int(request.args.get("dealerId"))

        selector = {'dealership': {'$eq': dealer_id}}
        result_by_filter = my_database.get_query_result(
            selector, raw_result=True)
        reviews = result_by_filter["docs"]
        review_list=[]        
        for review in reviews:
            review_list.append(review)

        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': review_list}
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