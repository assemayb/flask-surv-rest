import json
from main import app, db
from models import User, Survey, Question, Answer
from flask import request, Response, make_response, jsonify


def send_response(status, response, mimetype='application/json'):
    if str(type(response)) == "<class 'dict'>":
        response = json.dumps(response)
    if str(type(status)) != "<class 'str'>":
        status = str(status)
    return Response(status=status, response=response, mimetype=mimetype)


@app.route("/", methods=["GET"])
def get_index():
    if request.method == "GET":
        return send_response('200', {"msg": "okay! Welcome"})


@app.route("/users", methods=["GET"])
def get_user():
    users = User.query.all()
    if len(users) != 0:
        all_users = []
        for user in users:
            user_dict = {}
            user_dict['id'] = user.id
            user_dict['name'] = user.name
            user_dict['email'] = user.email
            user_dict['password_hash'] = user.password_hash
            all_users.append(user_dict)
        return send_response("200", json.dumps(all_users))
    else:
        return send_response("204", "No Users")


@app.route("/survey", methods=["GET", "POST"])
def get_or_create_survey():
    if request.method == "GET":
        surveys = Survey.query.all()
        all_surveys = []
        for survey in surveys:
            sur_data = {}
            sur_data['id'] = survey.id
            sur_data['theme'] = survey.theme
            print(survey.creator)
            sur_data['creator'] = survey.creator
            sur_data['created_at'] = survey.created_at
            all_surveys.append(sur_data)
        return send_response("200", json.dumps(all_surveys, default=str))

    elif request.method == "POST":
        try:
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
            """ separate these you dipshit! """
            survey_id = Survey.query.filter_by(theme=theme_name).first().id
            questions_arr = req_data['questions']
            for question in questions_arr:
                question_title = question["title"]
                q = Question(content=question_title, survey=survey_id)
                db.session.add(q)
                db.session.commit()
                q_id = Question.query.filter_by(
                    content=question_title).first().id
                questions_answers = question["answers"]
                for ans in questions_answers:
                    answer_val = ans
                    a = Answer(content=answer_val, question=q_id)
                    db.session.add(a)
                    db.session.commit()
                    print("===> Answer for a question is added <===")
            return send_response("200", "data sent successfully")
        except Exception as e:
            print(e)
            return send_response("500", "something wrong occured!")
