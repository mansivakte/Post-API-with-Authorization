from flask import Blueprint, Flask, jsonify, request
from .model import Post
from app.db import db
from app.commom import loginRequired
import datetime

post_blueprint = Blueprint('post_blueprint', __name__)

#Create Post => POST
@post_blueprint.route('/posts', methods=['POST'])
@loginRequired
def createPost(userid):
    payload = request.json
    post = Post( title = payload['title'], body = payload['body'], created_by = userid)
    db.session.add(post)
    db.session.commit()
    return {'status': 'Successfully created a new post'}

#Get all posts => GET
@post_blueprint.route('/post', methods=['GET'])
def getAllPosts():
    try:
        post = Post.query.filter_by(is_deleted= False).all()
        postlist = []
        for i in post:
            a = {
                'id':i.id,
                'title':i.title,
                'body':i.body,
                'created_by': i.created_by,
                'created_date':i.created_date,
                'updated_by': i.updated_by,
                'updated_date': i.updated_date
            }
            postlist.append(a)
        return {'Status': True, 'Message':' ', 'Data':postlist }
    except:
        return {'Status': False, 'Message':' Something wents wrong ', 'Data':None }

#Get post by ID => GET
@post_blueprint.route('/post/<id>', methods = ['GET'])
def getPostById(id):
    try:
        post = Post.query.filter_by(id=id).first()
        if not post:
            return {'Status': True, 'Message':'', 'data':{}}
        a = {
            'id':post.id,
            'title':post.title,
            'body':post.body,
            'created_by': post.created_by,
            'created_date':post.created_date,
            'updated_by': post.updated_by,
            'updated_date': post.updated_date
        }
        return {'Status': True, 'Message':'', 'Data':a}
    except:
        return {'Status': False, 'Message':' Something wents wrong ', 'Data':None}

#Update post => PUT
@post_blueprint.route('/post/<id>', methods = ['PUT'])
@loginRequired
def updatePost(userid,id):
    try:
        payload = request.json
        post = Post.query.filter_by(id=id).first()
        post.updated = True
        post.updated_date = datetime.datetime.now()
        post.updated_by = userid
        post.title = payload['title']
        post.body = payload['body']
        db.session.commit()
        return {'Status': True, 'Message':'', 'Data':''}
    except:
        return {'Status': False, 'Message':' Something wents wrong ', 'Data':None}

#Delete post => DELETE
@post_blueprint.route('/post/<id>', methods=['DELETE'])
@loginRequired
def deletePost(id):
    try:
        post = Post.query.filter_by(id=id).first()
        if not post:
            return {"Satus" : True, "Message" : "No record found", "Data" : None}
        post.is_deleted = True
        db.session.commit()
        return {'Status': True, 'Message':'', 'Data':''}
    except:
        return {'Status': False, 'Message':' Something wents wrong ', 'Data':None}

    