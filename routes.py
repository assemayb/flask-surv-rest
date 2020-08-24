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
                creator_name = User.query.get(survey.creator).name
                questions_num = Question.query.filter_by(
                    survey=survey.id).count()
                sur_data['creator_name'] = creator_name
                sur_data['questions_num'] = questions_num
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


@app.route("/user-surveys", methods=["GET"])
def get_user_surveys():
    request_data = json.loads(request.data)
    request_username = request_data['username']
    request_user_id = User.query.filter_by(name=request_username).first().id
    all_user_surveys = Survey.query.filter_by(creator=request_user_id)
    response = []
    for survey in all_user_surveys:
        survey_dict = {"id": survey.id,
                       "theme": survey.theme, "creator": survey.creator, "created_at": survey.created_at}
        response.append(survey_dict)
    return send_response("200", json.dumps(response, default=str))


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
                return send_response("200", {"msg": "question and answers added"})
            else:
                return send_response("400", {"msg": "Enter all required data fields"})
        else:
            return send_response("400", {"msg": "survey does not exist"})

    elif request.method == "GET":
        survey_id = request.args.get('id')
        sur = Survey.query.get(survey_id)
        
        if sur != None:
            response_data = {}
            response_data['title'] = sur.theme
            response_data['creator'] = sur.creator
            response_data['questions'] = []
            survey_questions = Question.query.filter_by(survey=survey_id)
            for q in survey_questions:
                print(q.content)

            for sq in survey_questions:
                question_id = sq.id
                question_title = sq.content
                data_dic = {"id": question_id, "question_title": question_title}
                question_answers = Answer.query.filter_by(question=question_id)
                data_dic['answers'] = []
                for ans in question_answers:
                    data_dic['answers'].append(ans.content)
                response_data['questions'].append(data_dic)
        return send_response("200", response_data)


@app.route("/survey-delete", methods=["DELETE"])
def delete_surv():
    req_id = request.args.get('id')
    req_user = request.args.get('username')
    survey = Survey.query.get(req_id)
    if survey is None:
        return send_response("400", {"msg": "no survey with this id is available!"})
    print(survey.creator)
    if req_user == survey.creator:
        db.session.delete(survey)
        db.session.commit()
        print(f"===> survey {survey.theme} deleted")
        survey_questions = Question.query.filter_by(survey=req_id)
        for single_question in survey_questions:
            questiond_id = single_question.id
            db.session.delete(single_question)
            db.session.commit()
            print(f"====>Question {single_question.content} Deleted")
            associated_ans = Answer.query.filter_by(question=questiond_id)
            for ans in associated_ans:
                db.session.delete(ans)
                db.session.commit()
                print(f"===>Answer {ans.content} Deleted")
        return send_response("200", {"msg": "ok done!"})
    else:
        return send_response("403", {"msg": "survey isn't created by you!"})


# TEMP LOGIN
@app.route("/login", methods=["POST"])
def login_user():
    user_data = json.loads(request.data)
    username = user_data['username']
    password = user_data['password']
    print(user_data)
    does_exist = User.query.filter_by(name=username).first()
    if does_exist:
        # CREATING A MOCK ACCESS TOKEN
        access = [f"{i}cv" for i in range(10)]
        refresh = [f"{i}ks" for i in range(10)]
        accessToken = ""
        refreshToken = ""
        for i in range(len(access)):
            accessToken += access[i]
            refreshToken += refresh[i]
        print(accessToken, refreshToken)
        response_dic = {"username": username,
                        "accessToken": accessToken, "refreshToken": refreshToken}
        return send_response("200", response_dic)
    else:
        return send_response("400", {"msg": "no user"})


# CREATE NEW USER
@app.route("/create-user", methods=["POST"])
def create_user():
    request_data = json.loads(request.data)
    username, password = request_data['username'], request_data['password']
    email = request_data['email']
    users_exists = User.query.filter_by(name=username).first()
    if users_exists:
        return send_response("400", {"msg": "user with this name does exist"})
    new_user = User(
        name=username,
        password_hash=password,
        email=email
    )
    db.session.add(new_user)
    db.session.commit()
    return send_response("200", {"msg": "ok cool User Added"})
