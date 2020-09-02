from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required , get_jwt_identity
from models.post import PostModel

class Post(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title',
    type=str,
    required=True,
    help="This field is required!")
    
    parser.add_argument('body',
    type=str,
    required=True,
    help="This field is required!")

   
    def get(self,title):
        postResult = PostModel.find_by_title(title)
        
        if postResult:
            return postResult.json()
        return {'message':'No post found'}, 404

class PostWithId(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title',
    type=str,
    required=True,
    help="This field is required!")
    
    parser.add_argument('body',
    type=str,
    required=True,
    help="This field is required!")
    
    @jwt_required
    def get(self,id):
        # print(get_jwt_identity())
        postResult = PostModel.find_by_id(id)
        if postResult:
            return postResult.json()
        return {'message': ' No post with found'}, 404


class PostList(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('title',
    type=str,
    required=True,
    help="This field is required!")
    
    parser.add_argument('body',
    type=str,
    required=True,
    help="This field is required!")

    def get(self):
        return {'posts': [post.json() for post in PostModel.find_all()]}

    @jwt_required
    def post(self):
        
        data = Post.parser.parse_args()
        if PostModel.find_by_title(data['title']):
            return {'message': "A post with title '{}' already exists.".format(data['title'])}, 400
        user_id = get_jwt_identity()
        # print(user_id)
        post = PostModel(data['title'], data['body'],user_id)

        try:
            post.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return post.json(), 201

