from flask import Flask

app = Flask(__name__)

@app.route('/launch', methods=['GET'])
def launch_python_file():

    
    user_uid = request.args.get('uid')
    print('User UID:', user_uid)
    return 'Success'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
