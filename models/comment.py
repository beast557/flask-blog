from db import db

class CommentModel(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id')) 
    post = db.relationship('PostModel')

    def __init__(self, body,user_id, post_id):
        self.body = body
        self.user_id = user_id
        self.post_id = post_id

    def json(self):
        return {
            'id':self.id,
            'body':self.body,
            'user_id':self.user_id,
            'post_id':self.post_id
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_same_comment(cls, user_id, post_id, body):
        return cls.query.filter(CommentModel.user_id== user_id , CommentModel.post_id== post_id, CommentModel.body==body).first()
