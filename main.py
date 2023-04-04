# redis
import redis
# time
import time
# Flask
import flask
# local files
import services


app: flask.app.Flask = flask.Flask(__name__)
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)


@app.route('/')
def main_page() -> dict:
    index: float = r.get('index')
    if not index:
        index = services.credit_his_calc()
        r.set('index', index)
    index = float(index)
    if index > 2:
        return flask.jsonify({"message": "Accepted"})
    else:
        return flask.jsonify({"message": "Not accepted"})


@app.route('/auth', methods=['GET', 'POST'])
def auth_page() -> dict:
    if flask.request.method == 'POST':
        login: str = r.get('login')
        pas: str = r.get('password')
        if not login:
            r.set('login', flask.request.form.get('log'))
            r.set('pas', flask.request.form.get('pas'))
            
        else:
            if (
                login == r.get('login')
            ) and (
                pas == r.get('password')
            ):
                return flask.redirect(
                    flask.url_for('main_page')
                )
            else:
                raise ValueError(
                    "wrong password or login"
                )

    return flask.render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True
    )
