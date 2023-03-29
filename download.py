import requests
import base64
import time
url = 'http://169.254.25.79/camera/download.php'

while True:
    # Send GET request to download.php
    response = requests.get(url)

    # Get response content as a string
    content = response.content

    # Decode base64 string to bytes
    decoded = base64.b64decode(content)

    # Save bytes to a PNG file
    with open('downloaded.png', 'wb') as f:
        f.write(decoded)
    print(time.time())
    time.sleep(1)
