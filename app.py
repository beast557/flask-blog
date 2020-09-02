from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager

from db import db
from security import authenticate, identity
from resources.user import UserRegister, UserLogin
from resources.post import Post , PostWithId,PostList
from resources.comment import Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app) 

class Test(Resource):
    def post(self):
        return {"message":"something"}


api.add_resource(UserRegister, '/register')
api.add_resource(Test, '/test')
api.add_resource(UserLogin, '/login')
api.add_resource(PostWithId, '/post/<int:id>')
api.add_resource(Post, '/post/<string:title>')
api.add_resource(PostList, '/posts')
api.add_resource(Comment, '/comment')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)