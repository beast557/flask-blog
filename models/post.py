from db import db

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    userdetails = db.relationship('UserModel')
    comments = db.relationship('CommentModel', lazy='dynamic')


    def __init__(self, title, body,user_id):
        self.title = title
        self.body = body
        self.user_id = user_id
        

    def json(self):
        return {
            'id':self.id,
            'title':self.title,
            'body':self.body,
            'user':self.userdetails.json(),
            'comments':[comment.json() for comment in self.comments.all()]
            
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    