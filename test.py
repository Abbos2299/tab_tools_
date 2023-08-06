from flask import Flask

app = Flask(__name__)

@app.route('/launch', methods=['GET'])
def launch_python_file():
    # Perform any actions you want to execute when the request is received
    # For example, you can launch a Python file or execute any other desired functionality
    print('Request accepted')
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
