from flask import Flask, jsonify
import requests
from firebase_admin import credentials, storage
import firebase_admin

app = Flask(__name__)

@app.route('/storage-usage', methods=['GET'])
def get_storage_usage():
    # Download the service account key file from the URL
    url = 'https://firebasestorage.googleapis.com/v0/b/raz-app-83361.appspot.com/o/_%2Fraz-app-83361-firebase-adminsdk-mtvdd-234e20e082.json?alt=media&token=72ff3535-5549-4bf8-8676-a0869e5269cc'
    response = requests.get(url)
    with open('serviceAccountKey.json', 'wb') as f:
        f.write(response.content)

    # Initialize Firebase app with the downloaded credential
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {'storageBucket': 'raz-app-83361.appspot.com'})

    # Get the storage client
    client = storage.bucket()

    blobs = client.list_blobs()
    current_usage = sum([blob.size for blob in blobs])

    # Get the total allocation based on the pricing plan
    # Replace the values in <pricing-plan> with your actual pricing plan
    total_allocation = 5 * 1024 * 1024 * 1024  # 5 GB in bytes

    remaining_storage = (total_allocation - current_usage) / 1024**3

    response_data = {
        'remaining_storage': remaining_storage
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
