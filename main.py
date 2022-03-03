import flask
import databases
import time
app = flask.Flask(__name__)


@app.route('/api/v1/addUser', methods=['POST'])
def add_user():
    content = flask.request.get_json()
    if content is None:
        return flask.jsonify({'error': 'No data'}), 400
    if 'identity' not in content:
        return flask.jsonify({'error': 'No identity'}), 400
    if 'data' not in content:
        return flask.jsonify({'error': 'No data'}), 400
    identity = content['identity']
    data = content['data']
    if identity is None or identity == '':
        return flask.jsonify({'error': 'No identity'}), 400
    if data is None or data == '':
        return flask.jsonify({'error': 'No data'}), 400
    try:
        if len(data) > 11 and data[0:11] == "data:image/":
            start = time.time()
            user_id = databases.add_user(data, identity)
            return flask.jsonify({'success': 'User added', 'id': user_id, 'elapsed': time.time() - start}), 200
        else:
            return flask.jsonify({'error': 'No image/Invalid Image'}), 400
    except Exception as e:
        return flask.jsonify({'error': 'Invalid data/Internal Error', 'stacktrace': e}), 400


@app.route('/api/v1/whoIs', methods=['POST'])
def who_is():
    content = flask.request.get_json()
    if content is None:
        return flask.jsonify({'error': 'No data'}), 400
    data = content['data']
    if data is None or data == '':
        return flask.jsonify({'error': 'No data'}), 400
    try:
        if len(data) > 11 and data[0:11] == "data:image/":
            start = time.time()
            identity = databases.index(data)
            return flask.jsonify({'success': 'Identity found', 'identity': identity, 'elapsed': time.time() - start}), 200
        else:
            return flask.jsonify({'error': 'No image/Invalid Image'}), 400
    except Exception as e:
        return flask.jsonify({'error': 'Invalid data/Internal Error', 'stacktrace': e}), 400


@app.route('/')
def root():
    return 'Alive'


if __name__ == '__main__':
    app.run(port=8080)