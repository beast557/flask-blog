from flask_restful import Resource, reqparse
from models.comment import CommentModel
from flask_jwt_extended import jwt_required , get_jwt_identity

class Comment(Resource):
    parser = reqparse.RequestParser()
    
    parser.add_argument('body',
    type=str,
    required=True,
    help="This field is required!")

    parser.add_argument('post_id',
    type=int,
    required=True,
    help="This field is required!")

    @jwt_required
    def post(self):
        data = Comment.parser.parse_args()
        body =  data['body']
        post_id =  data['post_id']
        user_id = get_jwt_identity()

        comment = CommentModel(body,user_id,post_id)

        if comment.find_same_comment(user_id,post_id,body):
            return {"message": "You already commented that already."}, 500 
        
        try:
            comment.save_to_db()
        except:
            return {"message": "An error occurred posting this comment."}, 500

        return comment.json(), 201
