# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from models import User, Question, Answer
from exts import db
# from decorators import login_required
from sqlalchemy import or_
from flask import Flask, g, jsonify, make_response, request, session
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import config
import os
import re
import json
from models import *
import gnucash_data.account as account

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')

auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True
app.config.from_object(config)
db.init_app(app)


@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if not admin:
        admin = Admin.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    return True


@app.route('/api/login', methods=['POST', 'GET'])
@auth.login_required
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})


@app.route('/api/setpwd', methods=['POST'])
@auth.login_required
def set_auth_pwd():
    data = json.loads(str(request.data))
    admin = Admin.query.filter_by(name=g.admin.name).first()
    if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
        admin.hash_password(data['newpass'])
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查输入"})


@app.route('/api/users/listpage', methods=['GET'])
@auth.login_required
def get_user_list():
    page_size = 4
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    query = db.session.query
    if name:
        Infos = query(JoinInfos).filter(
            JoinInfos.name.like('%{}%'.format(name)))
    else:
        Infos = query(JoinInfos)
    total = Infos.count()
    if not page:
        Infos = Infos.all()
    else:
        Infos = Infos.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'code': 200,
        'total': total,
        'page_size': page_size,
        'infos': [u.to_dict() for u in Infos]
    })


@app.route('/api/user/remove', methods=['GET'])
@auth.login_required
def remove_user():
    remove_id = request.args.get('id', type=int)
    if remove_id:
        remove_info = JoinInfos.query.get_or_404(remove_id)
        db.session.delete(remove_info)
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


@app.route('/api/user/bathremove', methods=['GET'])
@auth.login_required
def bathremove_user():
    remove_ids = request.args.get('ids')
    is_current = False
    if remove_ids:
        for remove_id in remove_ids:
            remove_info = JoinInfos.query.get(remove_id)
            if remove_info:
                is_current = True
                db.session.delete(remove_info)
            else:
                pass
        print(remove_ids, remove_info)
        if is_current:
            return jsonify({'code': 200, 'msg': "删除成功"})
        else:
            return jsonify({'code': 404, 'msg': "请正确选择"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


@app.route('/api/getdrawPieChart', methods=['GET'])
@auth.login_required
def getdrawPieChart():
    query = db.session.query
    Infos = query(JoinInfos)
    total = Infos.count()
    data_value = [0, 0, 0, 0, 0, 0, 0]  # 和下面组别一一对应
    group_value = ['视觉', '视频', '前端', '办公', '后端', '运营', '移动']
    for info in Infos:
        for num in range(0, 7):
            if group_value[num] in info.group:
                data_value[num] += 1
            else:
                pass
    return jsonify({'code': 200, 'value': data_value, 'total': total})


@app.route('/api/getdrawLineChart', methods=['GET'])
@auth.login_required
def getdrawLineChart():
    grade_value = []  # 年级汇总
    profess_value = []  # 学院汇总
    grade_data = {}  # 年级各学院字典
    Infos = JoinInfos.query.all()
    for info in Infos:
        if info.grade not in grade_value:
            grade_value.append(info.grade)
            grade_data[info.grade] = []
        if info.profess not in profess_value:
            profess_value.append(info.profess)
    for grade in grade_value:
        for profess in profess_value:
            grade_data[grade].append(0)
    for info in Infos:
        for grade in grade_value:
            for profess_local_num in range(0, len(profess_value)):
                if info.profess == profess_value[profess_local_num] and info.grade == grade:
                    grade_data[grade][profess_local_num] += 1
                else:
                    pass
    return jsonify({'code': 200, 'profess_value': profess_value, 'grade_value': grade_value, 'grade_data': grade_data})


# 获取当前储蓄金额
# 获取五大基本类型的当前balance


@auth.login_required
@app.route('/api/index', methods=['GET'])
def index():
    dic_5, dic_target = account.get_index_page_data()
    return jsonify({'code': 200,
                    'accounts': dic_5,
                    'dic_target': dic_target,
                    'showing_index': True, })


# 获取account 详情
# @auth.login_required
@app.route('/api/account/<account_guid>/', methods=['GET'])
def account_info(account_guid):
    page_num = request.args.get('page_num', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    account_info, total_size, txes = account.get_guid_info(guid=account_guid, page_num=page_num, page_size=page_size)
    return jsonify({'code': 200,
                    'account_info': account_info,
                    'total_size': int(total_size),
                    'list': txes, })


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# @app.route('/')
# def index():
#     context = {
#         'questions': Question.query.order_by('-create_time').all()
#     }
#     return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password ==
                                 password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认好在登录'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果被注册了就不能用了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码被注册，请更换手机'
        else:
            # password1 要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核实后再填写'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


# 判断用户是否登录，只要我们从session中拿到数据就好了   注销函数
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
# @login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
# @login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # title, content
    # 或 查找方式（通过标题和内容来查找）
    # questions = Question.query.filter(or_(Question.title.contains(q),
    #                                     Question.content.constraints(q))).order_by('-create_time')
    # 与 查找（只能通过标题来查找）
    questions = Question.query.filter(Question.title.contains(q), Question.content.contains(q))
    return render_template('index.html', questions=questions)


# 钩子函数(注销)
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
