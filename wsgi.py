import os
from flask import render_template
from myapp_sogou import make_app


application = make_app(version=os.environ.get('ENV', 'Local'))


@application.route('/info', methods=["GET"])
def index():
    return render_template('docs.html')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8700, debug=True)
