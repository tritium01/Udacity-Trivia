import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories= dict(Category.query.with_entities(Category.id, Category.type).group_by(Category.id, Category.type).order_by(Category.id).all())

    return jsonify({
      'success': True,
      "categories": categories
    })

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    categories= dict(Category.query.with_entities(Category.id, Category.type).group_by(Category.id, Category.type).order_by(Category.id).all())
    current_category = 'none'
    current_questions = pagination_questions(request, selection)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'current_category': current_category
    })

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
  
    if question is None:
      abort(404)
        
    try:
      question.delete()
      return jsonify({
        "success": True
      })
    except:
      print(sys.exc_info())
      abort(422)

  ''' 
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()

    if data is None:
      abort(404)
      
    try:
      question = Question(
      question= data.get('question'),
      answer= data.get('answer'),
      category= data.get('category'),
      difficulty= data.get('difficulty')
      )
      question.insert()
      
      return jsonify({
        "success": True
      })
    
    except:
      abort(422)
  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    data = request.get_json()
    search_term = data.get('searchTerm')
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    formatted_questions = [question.format() for question in questions]
    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "current_category": None
    })
  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category_questions(category_id):
    category = Category.query.filter_by(id = category_id).one_or_none()
    questions = Question.query.filter(Question.category == category_id).all()
    formatted_questions = [question.format() for question in questions]
    
    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "current_category": category.type
    }) 
    
    
  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
    data = request.get_json()
    category = data.get('quiz_category')
    prev_question = data.get('previous_questions')
    print(category, prev_question)
    if category['id'] == 0:
      questions = Question.query.filter(Question.id.notin_(prev_question)).all()
    else:
      questions = Question.query.filter(Question.category == category['id']).filter(Question.id.notin_(prev_question)).all()

    if len(questions) == 0:
      return jsonify({
        'success': True,
        'question': False
      })
      
    else:
      new_question = random.choices(questions, k=1)
      next_question = Question.query.filter(Question.id == new_question[0].id).one_or_none()
    
      return jsonify({
        'success': True,
        'question': next_question.format()
      })
  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.errorhandler(400)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'message': '400 Sorry, the requested resource was not found'
    })
    
  @app.errorhandler(404)
  def page_not_found(e):
    return jsonify({
      'success': False,
      'message': '404 Bad request, try again'
    })
  
  @app.errorhandler(405)
  def unp_entity(e):
    return jsonify({
      'success': False,
      'message': '405 Sorry, this method is not allowed for the endpoint requested, try again!'
    })
    
  @app.errorhandler(422)
  def method_not_allowed(e):
    return jsonify({
      'success': False,
      'message': '422 Sorry, it appears your request was succesfully sent but it was formated/written in the wrong manner, try again!'
    })
  @app.errorhandler(500)
  def method_not_allowed(e):
    return jsonify({
      'success': False,
      'message': '500 Internal error, please try again later'
    })
  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  return app

    