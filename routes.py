import json
from main import app, db
from models import User, Survey, Question, Answer
from flask import request, Response, make_response, jsonify


def send_response(status, response, mimetype='application/json'):
    if isinstance(response, dict):
        response = json.dumps(response)
    if not isinstance(status, str):
        status = str(status)
    return Response(status=status, response=response, mimetype=mimetype)


@app.route("/", methods=["GET"])
def get_index():
    if request.method == "GET":
        return send_response('200', {"msg": "okay! Welcome"})


@app.route("/users", methods=["GET"])
def get_user():
    try:
        users = User.query.all()
        if len(users) != 0:
            all_users = []
            for user in users:
                user_dict = {}
                user_dict['id'] = user.id
                user_dict['name'] = user.name
                user_dict['email'] = user.email
                # user_dict['password_hash'] = user.password_hash
                all_users.append(user_dict)
            return send_response("200", json.dumps(all_users))
        else:
            return send_response("204", "No Users")
    except Exception as e:
        print(e)


@app.route("/surveys", methods=["GET", "POST"])
def get_or_create_survey():
    if request.method == "GET":
        try:
            surveys = Survey.query.all()
            all_surveys = []
            for survey in surveys:
                sur_data = {}
                sur_data['id'] = survey.id
                sur_data['theme'] = survey.theme
                sur_data['creator'] = survey.creator
                sur_data['created_at'] = survey.created_at
                all_surveys.append(sur_data)
            return send_response("200", json.dumps(all_surveys, default=str))
        except Exception as e:
            print(e)
    elif request.method == "POST":
        req_data = json.loads(request.data)
        theme_name = req_data['theme']
        does_exist = Survey.query.filter_by(theme=theme_name).first()
        if does_exist:
            return send_response("404", {"msg": "Survey with name does exist"})
        user = req_data['username']
        new_survey = Survey(
            theme=theme_name,
            creator=user
        )
        db.session.add(new_survey)
        db.session.commit()


@app.route("/survey", methods=["POST", "GET"])
def add_to_survey():
    if request.method == "POST":
        survey_id = request.args.get('id')
        survey = Survey.query.get(survey_id)
        if survey is not None:
            survey_data = json.loads(request.data)
            question, answers = survey_data['title'], survey_data.get(
                'answers')
            if question and answers:
                prev_id = Question.query.count()
                q = Question(
                    content=question,
                    survey=survey_id
                )
                db.session.add(q)
                db.session.commit()
                print("question added")
                new_question_id = prev_id + 1
                for ans in answers:
                    a = Answer(content=ans, question=new_question_id)
                    db.session.add(a)
                    db.session.commit()
                    print(f" added answer'{a}'")
                return send_response("200", {"msg": "ok for now!"})
            else:
                return send_response("400", {"msg": "Enter all required data fields"})
        else:
            return send_response("400", {"msg": "survey does not exist"})

    elif request.method == "GET":
        survey_id = request.args.get('id')
        survey = Survey.query.get(survey_id)
        if survey:
            response_data = {}
            response_data['title'] = survey.theme
            response_data['creator'] = survey.creator
            response_data['questions'] = []
            survey_questions = Question.query.filter_by(survey=survey_id)
            for sq in survey_questions:
                questiod_id, questiod_title = sq.id, sq.content
                data_dic = {"id": questiod_id, "title": questiod_title}
                question_answers = Answer.query.filter_by(question=questiod_id)
                data_dic['answers'] = []
                for ans in question_answers:
                    data_dic['answers'].append(ans.content)
                response_data['questions'].append(data_dic)
        return send_response("200", response_data)
