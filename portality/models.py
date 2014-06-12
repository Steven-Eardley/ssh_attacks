
from datetime import datetime

from portality.core import app

from portality.dao import DomainObject as DomainObject

'''
Define models in here. They should all inherit from the DomainObject.
Look in the dao.py to learn more about the default methods available to the Domain Object.
When using portality in your own flask app, perhaps better to make your own models file somewhere and copy these examples
'''

# an example account object, which requires the further additional imports
# There is a more complex example below that also requires these imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Account(DomainObject, UserMixin):
    __type__ = 'account'

    @classmethod
    def pull_by_email(cls,email):
        res = cls.query(q='email:"' + email + '"')
        if res.get('hits',{}).get('total',0) == 1:
            return cls(**res['hits']['hits'][0]['_source'])
        else:
            return None

    def set_password(self, password):
        self.data['password'] = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.data['password'], password)

    @property
    def is_super(self):
        return not self.is_anonymous() and self.id in app.config['SUPER_USER']
    
# Model for a ssh log entry
# Jun  7 23:57:02 Zeus sshd[22455]: Invalid user admin from 61.174.51.219

class SshEntry(DomainObject):
    __type__ = 'ssh_entry'

    def set_attack_time(self, thing):
        self.data['attack_time'] = thing

    def set_attack_name(self, name):
        self.data['attack_name'] = name

    def set_attack_ip(self, ip):
        self.data['attack_ip'] = ip


# a typical record object, with no special abilities
class Record(DomainObject):
    __type__ = 'record'

    
# a special object that allows a search onto all index types - FAILS TO CREATE INSTANCES
class Everything(DomainObject):
    __type__ = 'everything'

    @classmethod
    def target(cls):
        t = 'http://' + str(app.config['ELASTIC_SEARCH_HOST']).lstrip('http://').rstrip('/') + '/'
        t += app.config['ELASTIC_SEARCH_DB'] + '/'
        return t


# a page manager object, with a couple of extra methods
class Pages(DomainObject):
    __type__ = 'pages'

    @classmethod
    def pull_by_url(cls,url):
        res = cls.query(q={"query":{"term":{'url.exact':url}}})
        if res.get('hits',{}).get('total',0) == 1:
            return cls(**res['hits']['hits'][0]['_source'])
        else:
            return None

    def update_from_form(self, request):
        newdata = request.json if request.json else request.values
        for k, v in newdata.items():
            if k == 'tags':
                tags = []
                for tag in v.split(','):
                    if len(tag) > 0: tags.append(tag)
                self.data[k] = tags
            elif k in ['editable','accessible','visible','comments']:
                if v == "on":
                    self.data[k] = True
                else:
                    self.data[k] = False
            elif k not in ['submit']:
                self.data[k] = v
        if not self.data['url'].startswith('/'):
            self.data['url'] = '/' + self.data['url']
        if 'title' not in self.data or self.data['title'] == "":
            self.data['title'] = 'untitled'

    def save_from_form(self, request):
        self.update_from_form(request)
        self.save()
    

# You can make simple models that just reside in their own index type.
# Then other model types may rely on them, or they may be used on your frontend. Whatever.
class SearchHistory(DomainObject):
    __type__ = 'searchhistory'


# You could write a record model that stores versions of itself in an archive.
# In which case, here is an example of an Archive model.
class Archive(DomainObject):
    __type__ = 'archive'
    
    @classmethod
    def store(cls, data, action='update'):
        archive = Archive.get(data.get('_id',None))
        if not archive:
            archive = Archive(_id=data.get('_id',None))
        if archive:
            if 'store' not in archive.data: archive.data['store'] = []
            try:
                who = current_user.id
            except:
                who = data.get('_created_by','anonymous')
            archive.data['store'].insert(0, {
                'date':data.get('_last_modified', datetime.now().strftime("%Y-%m-%d %H%M")), 
                'user': who,
                'state': data, 
                'action':action
            })
            archive.save()
