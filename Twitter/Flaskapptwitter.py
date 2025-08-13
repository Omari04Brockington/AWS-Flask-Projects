
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, request, render_template, session, make_response
from flask_session import Session
import example
app = Flask(__name__)

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


########
def is_palindrome(s):
    count = len(s) // 2
    for i in range(count):
        if s[i] != s[-1 - 1]:
            return False
    return True

@app.route('/pal')
def pal():
    words = request.args.get('q')
    words = words.split(',')
    results = []
    for word in words:
        if is_palindrome(word):
            results.append(word)
    return {'results': results}
###############

@app.route('/example/listfiles')
def example_listfiles():
    return example.listfiles()

@app.route('/example/uploadfile', methods=['POST'])
def example_uploadfile():
    return example.uploadfile()

@app.route('/example/listimages')
def example_listimages():
    return example.listimages()



##############

@app.route('/example/course/<number>')
def example_course(number):
    course = example.find_course(number)
    return render_template('course.html', course=course)




@app.route('/')
def example_dashboard():
    return example.dashboard()

@app.route('/about')
def example_about():
    return example.about()

@app.route('/add')
def example_add():
    return example.add()

@app.route('/schedule/<search>')
def example_schedule(search):
    return example.schedule(search)

@app.route('/seidenberg')
def seidenberg():
    return redirect('https://www.pace.edu/seidenberg')

@app.route('/account')
def example_account():
    return example.account()

@app.route('/home/', defaults={'search': ''}) # I am trying to add default url if user doesn't put any input
@app.route('/home/<search>')
def example_home(search):
    if search is None:
        search = ''
    return example.home(search)


# A very simple Flask Hello World app for you to get started with...
#when browser connects, flask will give browser a session ID



# helper function: saying if theres no variable named email there
def is_logged_in():
    if not session.get('email'):
        return example.auto_login()
    return True



@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/account.html')
def account_html():
    if is_logged_in():
        return render_template('account.html', username=session.get('username'))
    else:
        return redirect('/login.html')

@app.route('/homepage.html')
def homepage_html():
    if is_logged_in():
        return render_template('homepage.html', username=session.get('username'))
    else:
        return redirect('/login.html')

@app.route('/editor.html')
def editor_html():
    if is_logged_in():
        return render_template('editor.html', username=session.get('username'))
    else:
        return redirect('/login.html')



@app.route('/logout.html')
def logout():
    session.pop('email', None)
    session.pop('username', None)
    response = make_response(redirect('/login.html'))
    response.delete_cookie('remember')
    return response


@app.route('/example/login')
def example_login():
    return example.login()

@app.route('/example/setname')
def example_setname():
    session['name'] = 'Testing'  # setting our session variable. not permanent, but given to user as they browse website
    return 'OK'

@app.route('/example/getname')
def example_getname():
    return 'Hello ' + session.get('name')

@app.route('/example/postblog')
def example_postblog():
    return example.postblog()

@app.route('/example/listblogs')
def example_listblogs():
    return example.listblogs()

@app.route('/example/deleteblog')
def example_deleteblog():
    return example.deleteblog()

@app.route('/example/createacc')
def example_createacc():
    return example.createacc()

#######################################################################################
# Final Project: Twitter

@app.route('/twitterlogin.html')
def twitterlogin_html():
    return render_template('twitterlogin.html')

@app.route('/twitteraccount.html')
def twitteraccount_html():
    if is_logged_in():
        return render_template('twitteraccount.html', username=session.get('username'))
    else:
        return redirect('/twitterlogin.html')

@app.route('/twitterfeed.html')
def twitterfeed_html():
    if is_logged_in():
        return render_template('twitterfeed.html', username=session.get('username'))
    else:
        return redirect('/twitterlogin.html')

@app.route('/twittersign.html')
def twittersign_html():
    return render_template('/twittersign.html')

@app.route('/twitterviewer.html')
def twitterviewer_html():
    username = request.args.get('username')
    if username == session.get('username'):
        return render_template('/twitteraccount.html', username=session.get('username'))
    else:
        return render_template('twitterviewer.html', username=username)



@app.route('/example/loginTwitter')
def example_loginTwitter():
    return example.loginTwitter()

@app.route('/logoutTwitter.html')
def logoutTwitter():
    session.pop('email', None)
    session.pop('username', None)
    response = make_response(redirect('/login.html'))
    response.delete_cookie('remember')
    return response

@app.route('/example/postTweet')
def example_postTweet():
    return example.postTweet()

@app.route('/example/reply')
def example_reply():
    return example.reply()

@app.route('/example/editTweets')
def example_editTweets():
    return example.editTweets()

@app.route('/example/listTweet')
def example_listTweet():
    return example.listTweet()

@app.route('/example/listReply')
def example_listReply():
    return example.listReply()

@app.route('/example/deleteTweet')
def example_deleteTweet():
    return example.deleteTweet()

@app.route('/example/createAccount')
def example_createAccount():
    return example.createAccount()


@app.route('/twitterlogout.html')
def twitterlogout():
    session.pop('email', None)
    session.pop('username', None)
    response = make_response(redirect('/twitterlogin.html'))
    response.delete_cookie('remember')
    return response

@app.route('/example/uploadprofilepic', methods=['POST'])
def example_uploadprofilepic():
    return example.uploadprofilepic()

@app.route('/example/showprofilepic')
def example_showprofilepic():
    return example.showprofilepic()

@app.route('/example/viewProfile')
def example_viewProfile():
    return example.viewProfile()

@app.route('/example/showTweet')
def example_showTweet():
    return example.showTweet()

@app.route('/example/viewprofilePic')
def example_viewprofilePic():
    return example.viewprofilePic()