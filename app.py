from flask        import Flask, request, jsonify
from flask.json   import JSONEncoder

app          = Flask(__name__)
app.id_count = 1
app.users    ={}
app.tweets   =[]

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    user                = request.json
    user['id']          = app.id_count
    app.users[app.id_count] = user
    app.id_count            = app.id_count + 1

    return jsonify(user)

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['user_id'])
    tweet   = payload['tweet']

    if user_id not in app.users:
        return 'invalid_user', 400

    if len(tweet) > 300:
        return 'exceed_word_limits', 400

    user_id = int(payload['user_id'])
    app.tweets.append(
        {
            'user_id' : user_id,
            'tweet'   : tweet
        }
    )
    return '', 200

@app.route('/follow', methods=['POST'])
def follow():
    payload     = request.json
    user_id     = int(payload['user_id'])
    followee_id = int(payload['followee_id'])

    if user_id not in app.users or followee_id not in app.users:
        return 'invalid_user', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(followee_id)
    return jsonify(user)

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload     = request.json
    user_id     = int(payload['user_id'])
    followee_id = int(payload['followee_id'])

    if user_id not in app.users or followee_id not in app.users:
        return 'invalid_user', 400
    user = app.users[user_id]
    user.setdefault('follow', set()).discard(followee_id)

    return jsonify(user)
