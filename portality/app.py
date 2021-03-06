'''
This is the default app controller for portality.
For inclusion in your own project you should make your own version of this controller
and include the views you require, as well as writing new ones. Of course, views must 
also be backed up by models, so have a look at the example models and use them / write 
new ones as required too.
'''

from flask import request, render_template
from flask_login import login_user, current_user

import portality.models as models
from portality.core import app, login_manager

from portality.view.contact import blueprint as contact
from portality.view.query import blueprint as query
from portality.view.data import blueprint as data
from portality.view.explorer import blueprint as explorer
from portality.view.map import blueprint as ip_map


app.register_blueprint(contact, url_prefix='/contact')
app.register_blueprint(query, url_prefix='/query')
app.register_blueprint(data, url_prefix='/data')
app.register_blueprint(explorer, url_prefix='/explorer')
app.register_blueprint(ip_map, url_prefix='/map')

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_account_for_login_manager(userid):
    out = models.Account.pull(userid)
    return out

@app.context_processor
def set_current_context():
    """ Set some template context globals. """
    return dict(current_user=current_user, app=app)

@app.before_request
def standard_authentication():
    """Check remote_user on a per-request basis."""
    remote_user = request.headers.get('REMOTE_USER', '')
    if remote_user:
        user = models.Account.pull(remote_user)
        if user:
            login_user(user, remember=False)
    # add a check for provision of api key
    elif 'api_key' in request.values:
        res = models.Account.query(q='api_key:"' + request.values['api_key'] + '"')['hits']['hits']
        if len(res) == 1:
            user = models.Account.pull(res[0]['_source']['id'])
            if user:
                login_user(user, remember=False)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'])

    #TODO: Fix when loading with an empty index (e.g. indexError on data page).
