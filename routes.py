import time
import json
import random
from main import app, db
from models import User, Survey, Question, Answer, FormMetaData, FormData
from flask import request, Response, make_response, jsonify


def random_token_generator():
    token = ""
    all_small_letters = [chr(i) for i in range(97, 123)]
    nums = [str(i) for i in range(10)]
    chars = [str(i) for i in range(10) if i % random.randint(2, 5) == 0]
    for i in range(6):
        num = random.choice(nums)
        letter = random.choice(all_small_letters)
        char = random.choice(chars)
        token += num + letter + char
    return token


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
        username = req_data['username']
        creator_id = User.query.filter_by(name=username).first().id
        new_survey = Survey(
            theme=theme_name,
            creator=creator_id
        )
        db.session.add(new_survey)
        db.session.commit()
        return send_response("200", {"msg": "Survey Created!"})


@app.route("/user-surveys", methods=["GET"])
def get_user_surveys():
    request_username = request.args['username']
    request_user_id = User.query.filter_by(name=request_username).first().id
    all_user_surveys = Survey.query.filter_by(creator=request_user_id)
    response = []
    for survey in all_user_surveys:
        creator_name = User.query.get(survey.creator).name
        questions_num = Question.query.filter_by(
            survey=survey.id).count()
        survey_dict = {"id": survey.id,
                       "theme": survey.theme, "creator": survey.creator, "created_at": survey.created_at}
        survey_dict['creator_name'] = creator_name
        survey_dict['questions_num'] = questions_num
        submitted_surv_num = FormMetaData.query.filter_by(
            survey=survey.id).count()
        survey_dict['submitted_surv_num'] = submitted_surv_num
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
                is_quest_submitted = Question.query.filter_by(
                    content=question).first()
                if is_quest_submitted is None:
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
                    return send_response("400", {"msg": "this question exists"})
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
            creator_name = User.query.get(sur.creator).name
            response_data['creator_name'] = creator_name
            response_data['questions'] = []
            survey_questions = Question.query.filter_by(survey=survey_id)
            for sq in survey_questions:
                question_id = sq.id
                question_title = sq.content
                data_dic = {"id": question_id,
                            "question_title": question_title}
                question_answers = Answer.query.filter_by(question=question_id)
                data_dic['answers'] = []
                for ans in question_answers:
                    ansDict = {"answer_id": ans.id,
                               "answer_value": ans.content}
                    data_dic['answers'].append(ansDict)
                response_data['questions'].append(data_dic)
        return send_response("200", response_data)

# UPDATING SURVEY DATA


@app.route("/survey-update", methods=["POST"])
def update_survey():
    try:
        survey_id = request.args.get("id")
        survey = Survey.query.get(int(survey_id))
        request_data = json.loads(request.data)
        questions_ids = request_data["changedQuestionsIDs"]
        submitted_data = request_data["dataToSubmit"]
        print(questions_ids)
        for q in submitted_data:
            question_id = q['id']
            print(question_id, type(question_id))
            if question_id in questions_ids:
                question_ans = q['answers']
                question = Question.query.get(question_id)
                question.content = q.get('question_title')
                db.session.commit()
                question_old_answers = Answer.query.filter_by(
                    question=question_id)
                index = 0
                for old_ans in question_old_answers:
                    old_ans.content = question_ans[index]['answer_value']
                    db.session.commit()
                    index += 1
        return send_response("200", {"msg": "ok Survey has been updated"})
    except Exception as e:
        print(e)
        return send_response("400", {"msg": "error!"})


# CHECK THE USER FROM META DATA
@app.route("/check-user", methods=["GET"])
def check_user():
    survey_id = int(request.args.get("survey"))
    req_ip = request.remote_addr
    time.sleep(1)
    ip = FormMetaData.query.filter_by(survey=survey_id, user_ip=req_ip).first()
    is_ip_saved = True if ip is not None else False
    print(is_ip_saved)
    if is_ip_saved:
        return send_response("204", {"msg": f"{req_ip} is not fine"})
    else:
        return send_response("200", {"msg": f"{req_ip} is fine"})

# SUBMIT FORM


@app.route("/submit-form", methods=["POST"])
def submit_form():
    client_request_ip = request.remote_addr
    survey_id = int(request.args.get("survey"))
    submitted_data = json.loads(request.data)
    survey_data = submitted_data['submittedData']
    if (client_request_ip and survey_id):
        for single_item in survey_data:
            question_val = single_item["quesVal"]
            answer_val = single_item["ansVal"]
            new_form_data = FormData(
                survey=survey_id,
                question=question_val,
                answer=answer_val
            )
            db.session.add(new_form_data)
            db.session.commit()
            print("===> question has beed added")
        new_meta = FormMetaData(
            survey=survey_id,
            user_ip=client_request_ip
        )
        db.session.add(new_meta)
        db.session.commit()
        return send_response("200", {"msg": "Form Submitted Successfully."})
    else:
        return send_response("400", {"msg": "can't submit!"})


# GETTING A FORM DATA
@app.route("/form-data", methods=["GET"])
def get_form_data():
    try:
        survey_id = int(request.args.get("survey"))
        survey_title = Survey.query.get(survey_id).theme
        all_surv_questions = Question.query.filter_by(survey=survey_id)
        questions = []
        index = 0
        for question in all_surv_questions:
            question_id = question.id
            print(question_id)
            questions.append({"question": question.content, "answers": []})
            all_surv_answers = Answer.query.filter_by(question=question_id)
            surv_question_answers = [ans.content for ans in all_surv_answers]
            for idx, ans in enumerate(surv_question_answers):
                answered_times = FormData.query.filter_by(answer=ans, survey=survey_id).count()
                questions[index]["answers"].append({
                    "index": idx,
                    "val": ans,
                    "times": answered_times
                })
            index += 1
        result = {"survey_title":survey_title, "questions": questions}
        return send_response("200", result)
    except Exception as e:
        return send_response("400", {"msg": "bad request"})
        print(e)


# DELETE A SURVEY
@app.route("/survey-delete", methods=["DELETE"])
def delete_surv():
    req_id = request.args.get('id')
    print("req_id", req_id)
    req_user = request.args.get('username')
    req_user_id = User.query.filter_by(name=req_user).first().id
    survey = Survey.query.get(req_id)
    if survey is None:
        return send_response("400", {"msg": "no survey with this id is available!"})
    if req_user_id == survey.creator:
        survey_questions = Question.query.filter_by(survey=req_id)
        for single_question in survey_questions:
            questiond_id = single_question.id
            associated_ans = Answer.query.filter_by(question=questiond_id)
            for ans in associated_ans:
                db.session.delete(ans)
                db.session.commit()
            db.session.delete(single_question)
            db.session.commit()
        db.session.delete(survey)
        db.session.commit()
        survey_in_meta_form = FormMetaData.query.filter_by(
            survey=req_id).first()
        db.session.delete(survey_in_meta_form)
        db.session.commit()
        
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
        accessToken = random_token_generator()
        refreshToken = random_token_generator()
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
