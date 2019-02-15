from application import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))
    email = db.Column(db.String(64))
    user_type = db.Column(db.String(32))
    given_name = db.Column(db.String(32))
    family_name = db.Column(db.String(32))
    phone = db.Column(db.String(15))
    company = db.Column(db.String(15))
    address = db.Column(db.String(256))
    city = db.Column(db.String(32))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    linkedin = db.Column(db.String(256))
    website = db.Column(db.String(256))

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.email = kwargs.get('email', "")
        self.user_type = kwargs.get('user_type', "")
        self.given_name = kwargs.get('given_name', "")
        self.family_name = kwargs.get('family_name', "")
        self.phone = kwargs.get('phone', "")
        self.company = kwargs.get('company', "")
        self.address = kwargs.get('address', "")
        self.city = kwargs.get('city', "")
        self.state = kwargs.get('state', "")
        self.zipcode = kwargs.get('zipcode', "")
        self.linkedin = kwargs.get('linkedin', "")
        self.website = kwargs.get('website', "")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.query(User).filter(User.uid == self.uid)\
            .update({User.uid: self.uid,
                     User.email: self.email,
                     User.user_type: self.user_type,
                     User.given_name: self.given_name,
                     User.family_name: self.family_name,
                     User.phone: self.phone,
                     User.company: self.company,
                     User.address: self.address,
                     User.city: self.city,
                     User.state: self.state,
                     User.zipcode: self.zipcode,
                     User.linkedin: self.linkedin,
                     User.website: self.website})
        db.session.commit()

    def exist(self):
        for row in db.session.query(User).filter(User.uid == self.uid):
            return True
        return False

    def profile(self):
        return db.session.query(User).filter(User.uid == self.uid).first()

    def tojson(self):
        return {'email': self.email,
                'user_type': self.user_type,
                'given_name': self.given_name,
                'family_name': self.family_name,
                'phone': self.phone,
                'company': self.company,
                'address': self.address,
                'city': self.city,
                'state': self.state,
                'zipcode': self.zipcode,
                'linkedin': self.linkedin,
                'website': self.website}


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))
    skill_list = db.Column(db.String(1024))

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.skill_list = kwargs.get('skill_list', "")

    def exist(self):
        for row in db.session.query(Skill).filter(Skill.uid == self.uid):
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.query(Skill).filter(Skill.uid == self.uid)\
            .update({Skill.skill_list: self.skill_list})
        db.session.commit()

    def skills(self):
        return db.session.query(Skill).filter(Skill.uid == self.uid).first()

    def tojson(self):
        return {'skill_list': self.skill_list}


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))
    role_list = db.Column(db.String(512))

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.role_list = kwargs.get('role_list', "")

    def exist(self):
        for row in db.session.query(Role).filter(Role.uid == self.uid):
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.query(Role).filter(Role.uid == self.uid)\
            .update({Role.role_list: self.role_list})
        db.session.commit()

    def roles(self):
        return db.session.query(Role).filter(Role.uid == self.uid).first()

    def tojson(self):
        return {'role_list': self.role_list}


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))
    work_list = db.Column(db.String(2048))

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.work_list = kwargs.get('work_list', "")

    def exist(self):
        for row in db.session.query(Work).filter(Work.uid == self.uid):
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.query(Work).filter(Work.uid == self.uid)\
            .update({Work.work_list: self.work_list})
        db.session.commit()

    def works(self):
        return db.session.query(Work).filter(Work.uid == self.uid).first()

    def tojson(self):
        return {'work_list': self.work_list}


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.String(256))  # md5(project_name)
    name = db.Column(db.String(256))
    uid = db.Column(db.String(256))  # Poster uid
    status = db.Column(db.String(256))
    description = db.Column(db.String(1024))
    budget = db.Column(db.Integer)
    creator = db.Column(db.String(256))
    folder = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', "")
        self.pid = kwargs.get('pid', "")
        self.name = kwargs.get('name', "")
        self.uid = kwargs.get('uid', "")  # Poster uid
        self.status = kwargs.get('status', "")
        self.description = kwargs.get('description', "")
        self.budget = kwargs.get('budget', "")
        self.creator = kwargs.get('creator', "")
        self.folder = kwargs.get('folder', "")

    def exist(self):
        for row in db.session.query(Project).filter(Project.uid == self.uid)\
                                            .filter(Project.pid == self.pid):
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def list(self):
        project_list = []
        for row in db.session.query(Project).filter(Project.uid == self.uid):
            project_list.append({'name': row.name,
                                 'status': row.status,
                                 'create_time': row.create_time,
                                 'budget': row.budget})
        return project_list


class PRZ(db.Model):
    """PRZ(Project Running Zone)"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))  # Poster uid
    pid = db.Column(db.String(128))  # md5(project_name)
    creator = db.Column(db.String(256))
    status = db.Column(db.String(256))
    offer_price = db.Column(db.Integer)
    accept_price = db.Column(db.Integer)
    final_price = db.Column(db.Integer)

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.pid = kwargs.get('pid', "")
        self.creator = kwargs.get('creator', "")
        self.status = kwargs.get('status', "")
        self.offer_price = kwargs.get('offer_price', "")
        self.accept_price = kwargs.get('accept_price', "")
        self.final_price = kwargs.get('final_price', "")

    def save(self):
        db.session.add(self)
        db.session.commit()


class PH(db.Model):
    """Project History"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(128))
    pid = db.Column(db.String(128))
    log_tpye = db.Column(db.String(1024))
    log = db.Column(db.String(1024))

    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', "")
        self.pid = kwargs.get('pid', "")
        self.log_type = kwargs.get('log_type', "")
        self.log = kwargs.get('log', "")

    def save(self):
        db.session.add(self)
        db.session.commit()














