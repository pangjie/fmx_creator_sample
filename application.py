import jwt
import base64

from functools import wraps
from flask import Flask
from flask import request
from flask import jsonify
from flask import _request_ctx_stack
from werkzeug.local import LocalProxy
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config')

db = SQLAlchemy(application)
from models import *  # noqa
db.create_all()


current_user = LocalProxy(lambda: _request_ctx_stack.top.current_user)
db_user = LocalProxy(lambda: User(uid=current_user['sub']))
db_skill = LocalProxy(lambda: Skill(uid=current_user['sub']))
db_role = LocalProxy(lambda: Role(uid=current_user['sub']))
db_work = LocalProxy(lambda: Work(uid=current_user['sub']))


# Authentication attribute/annotation
def authenticate(error):
    resp = jsonify(error)
    resp.status_code = 401
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return authenticate({'code': 'authorization_header_missing',
                                 'description': application.config['AUTH_H_MISS']})
        parts = auth.split()
        if parts[0].lower() != 'bearer':
            return {'code': 'invalid_header',
                    'description': application.config['INV_HEADER_0']}
        elif len(parts) == 1:
            return {'code': 'invalid_header',
                    'description': 'Token not found'}
        elif len(parts) > 2:
            return {'code': 'invalid_header',
                    'description': application.config['INV_HEADER_2']}
        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                base64.b64decode(application.config['CLIENT_SC']
                                    .replace("_", "/")
                                    .replace("-", "+")),
                audience='dHCeAvImpUyvxssQpYZCG86OyZSJlXhH')
        except jwt.ExpiredSignature:
            return authenticate({'code': 'token_expired',
                                 'description': 'token is expired'})
        except jwt.InvalidAudienceError:
            return authenticate({'code': 'invalid_audience',
                                 'description': application.config['INV_AUDIENCE']})
        except jwt.DecodeError:
            return authenticate({'code': 'token_invalid_signature',
                                 'description': 'token signature is invalid'})
        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)
    return decorated


# Controllers API

# This part doesn't need authentication
@application.route("/")
@cross_origin(headers=['Content-Type', 'Authorization'])
def index():
    return application.send_static_file('index.html')


# This part need authentication

# Profile Function

# Get Profile
@application.route("/get_profile")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_profile():
    if db_user.exist():
        user_profile = db_user.profile().tojson()
        return jsonify({'user': user_profile,
                        'result': True})
    else:
        return jsonify({'result': False})


# Save Profile
@application.route("/save_profile", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def save_profile():
    user = User(uid=current_user['sub'],
                email=request.json['user']['email'],
                user_type=request.json['user']['user_type'],
                given_name=request.json['user']['given_name'],
                family_name=request.json['user']['family_name'],
                phone=request.json['user']['phone'],
                address=request.json['user']['address'],
                city=request.json['user']['city'],
                state=request.json['user']['state'],
                linkedin=request.json['user']['linkedin'],
                website=request.json['user']['website'],
                zipcode=request.json['user']['zipcode'],)
    if db_user.exist():
        user.update()
    else:
        user.save()
    return jsonify({'result': 'success'})


# Skill Function

# Get Skill List
@application.route("/get_skill")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_skill():
    if db_skill.exist():
        skill_tags = db_skill.skills().tojson()['skill_list']
        return jsonify({'skill': skill_tags,
                        'result': True})
    else:
        return jsonify({'result': False})


# Save Skill List
@application.route("/save_skill", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def save_skill():
    # skill_list = ','.join(request.json['skill'])
    skill_list = request.json['skill']
    if db_skill.exist():
        Skill(uid=current_user['sub'], skill_list=skill_list).update()
    else:
        Skill(uid=current_user['sub'], skill_list=skill_list).save()
    return jsonify({'result': 'success'})


# Role_list Function

# Save Role List
@application.route("/save_role", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def save_role():
    role_list = request.json['role']
    if db_role.exist():
        Role(uid=current_user['sub'], role_list=role_list).update()
    else:
        Role(uid=current_user['sub'], role_list=role_list).save()
    return jsonify({'result': 'success'})


# Get Role List
@application.route("/get_role")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_role():
    if db_role.exist():
        role_tags = db_role.roles().tojson()['role_list']
        return jsonify({'role': role_tags,
                        'result': True})
    else:
        return jsonify({'result': False})


# Work_list

# Get Work List
@application.route("/get_work")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_work():
    if db_work.exist():
        work_tags = db_work.works().tojson()['work_list']
        return jsonify({'work': work_tags,
                        'result': True})
    else:
        return jsonify({'result': False})


# Save Work List
@application.route("/save_work", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def save_work():
    work_list = request.json['work']
    if db_work.exist():
        Work(uid=current_user['sub'], work_list=work_list).update()
    else:
        Work(uid=current_user['sub'], work_list=work_list).save()
    return jsonify({'result': 'success'})


# Project GET&SAVE

# Get all projects which belong to the authorized user
@application.route("/get_project")
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_project():
    # t = Project.query.filter((Project.uid == current_user['sub']))
    # a = Project.query.filter((Project.uid == current_user['sub']))\
    #                  .filter((Project.status == 'new')).count()
    # b = Project.query.filter((Project.uid == current_user['sub']))\
    #                  .filter((Project.status == 'delete')).count()
    # c = Project.query.filter((Project.uid == current_user['sub']))\
    #                  .filter((Project.status == 'assigning')).count()
    # d = Project.query.filter((Project.uid == current_user['sub']))\
    #                  .filter((Project.status == 'working')).count()
    # print t.count()
    # print a + b + c + d

    project_list = Project(uid=current_user['sub']).list()
    return jsonify({'project_list': project_list,
                    'result': True})


# Post a new project as a poster
@application.route("/post_project", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def post_project():
    new_project = request.json['project']
    print(new_project['pid'])
    Project(uid=current_user['sub'],
            pid=new_project['pid'],
            status=new_project['status'],
            name=new_project['name'],
            description=new_project['description'],
            budget=new_project['budget']).save()
    return jsonify({'result': 'success'})


# Get some kind of project
@application.route("/show_project/<string:status>", methods=['POST'])
@application.route("/show_project/<int:id>", methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def show_project(**kwargs):
    # status = kwargs.get('status', "")
    # id = kwargs.get('id', "")
    # print(status)
    # print("This is id: " + str(id))
    # status_count = Project.query.filter(Project.status == status).count()
    # print("The amount of project with this status is " + str(status_count))
    return jsonify({'result': True})


if __name__ == '__main__':
    application.run()