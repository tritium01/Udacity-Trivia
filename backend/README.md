# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7
In order for current dependecies to work please use python 3.7 

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<question_id>/questions'
POST '/questions'
POST '/questions/search'
POST '/quizzes/'
DELETE '/questions/<question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
-Fetches all the questions in their table
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with multiple categories, questions are formatted and paginated to a max of 10, other key:value pairs include total amount of questions, categories and the current category in the selection. By default current category is None.
{'success': True,
'questions': [questions]
'total_questions': 14,
'categories': categories, 
'current_category': current_category} 

GET '/categories/<category_id>/questions'
-Fetches specific questions inside a category using a integer value for the category id
-Request Arguments: URI param category id 
-Returns: An object containing the following key:value pairs:
{"success": True,
"questions": formatted_questions,
"total_questions": len(formatted_questions),
"current_category": category.type}

POST '/questions'
-Creates a new question using a json object
-Request Arguments: Object containing the following key:value pairs:
{question: question,
answer: answer,
difficulty: difficulty(integer value),
category: category (integer value)}
-Return a object with a success key and value True

POST '/questions/search'
-Using a POST request a search query is made in order to find the questions that have a matching word in them
-Request Arguments: Uses an object as follows: {searchTerm: searchTerm}
-Returns an object the following key:value pairs:
{"success": True,
"questions": formatted_questions,
"total_questions": length of questions,
"current_category": None}
Please note that values returned are also paginated to return 10 items

POST '/quizzes/'
-Using a post request questions are returned filtering from the correct category and never repeating a question on that current quiz
-Required Arguments: uses two key:value pairs in order o find out the category and the questions previously used they are describe as follows:
{previous_questions: previousQuestions,
quiz_category: quizCategory}
-Returns an with two key:value pairs. Pay attention to the key question which returns the next question to be used in the test.
{'success': True,
'question': next_question}

DELETE '/questions/<question_id>'
-Deletes a question based on a integer id provided as a parameter
-Required Arguments: question_id as a param used to delete that question
-Returns an object with a key of success and value of true
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```