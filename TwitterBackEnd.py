from flask import Flask, request, redirect, render_template, session, make_response
import json
import boto3
import uuid
from datetime import datetime
from datetime import date





def get_public_bucket():
    s3client = boto3.resource(service_name='s3',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET)

    bucket = s3client.Bucket(PUBLIC_BUCKET)
    return bucket

def get_public_table(table_name):
    dbclient = boto3.resource(service_name='dynamodb',
                          region_name='us-east-1',
                          aws_access_key_id=AWSKEY,
                          aws_secret_access_key=AWSSECRET)


    table = dbclient.Table(table_name)
    return table

def uploadfile():
    bucket = get_public_bucket()
    table = get_public_table('Images')

    file = request.files["file"]

    filename = file.filename

    #You can get other form elements like this: x = request.form.get('x')
    caption = request.form.get("caption")
    ImageID = str(uuid.uuid4())


    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = 'image/png'

    substrings = filename.split(".")
    filetype = substrings[-1]
    imageName = ImageID + "." + filetype

    image = {'ImageID': ImageID,
            'ImageName': imageName,
            'Caption': caption}

    bucket.upload_fileobj(file, imageName, ExtraArgs={'ContentType': ct })
    table.put_item(Item=image)
    return { 'results' : 'OK' }

def listfiles():
    bucket = get_public_bucket()
    items = []
    for item in bucket.objects.all():
        items.append(item.key)
    return { 'url' : 'https://obrockington-web-public.s3.us-east-1.amazonaws.com/', 'items': items }

def listimages():
    table = get_public_table('Images')
    items = []
    for item in table.scan()['Items']:
        d = {'ImageID': item['ImageID'], 'ImageName': item['ImageName'], 'Caption':item['Caption']}
        items.append(d)
    return { 'url' : 'https://obrockington-web-public.s3.us-east-1.amazonaws.com/', 'items': items }


def postblog():
    table = get_public_table('Blogs')


    title = request.args.get("title")
    text = request.args.get("text")

    BlogID = str(uuid.uuid4())

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    Date = today + " " + current_time

    blog = {'BlogID': BlogID,
            'Title': title,
            'Text': text,
            'Date': Date}


    table.put_item(Item=blog)

    return { 'results' : 'OK' }

def listblogs():
    table = get_public_table('Blogs')
    items = []
    for item in table.scan()['Items']:
        d = {'BlogID': item['BlogID'], 'Title': item['Title'], 'Text':item['Text'], 'Date':item['Date']}
        items.append(d)

    items = sorted(items, key=lambda x: x['Date'], reverse=True)
    return {'items': items }

def deleteblog():
    table = get_public_table('Blogs')

    blogID = request.args.get("blogid")


    table.delete_item(Key={'BlogID': blogID})



    return { 'results' : 'OK' }

def createacc():
    table = get_public_table('Users')

    email = request.args.get('email', '')
    password = request.args.get('password', '')
    username = request.args.get('username', '')

    if email == '' or password == '' or username == '':
        return {'result':'Bad Login'}

    if '@' not in email or '.' not in email:
        return {'result':'Invalid Email'}

    user = {'username': username,
            'email': email,
            'password': password}


    table.put_item(Item=user)


    return { 'results' : 'OK' }

###################################################################

def get_remember_key(email):
    table = get_public_table('Remember')
    key = str(uuid.uuid4()) + str(uuid.uuid4())
    item = {'key': key, 'email' : email }
    table.put_item(Item=item)
    return key

def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')

    if email == '' or password == '':
        return {'result':'Bad Login'}

    table = get_public_table('Users')
    item = table.get_item(Key={'email':email}) #trying to find email in table, if it's not found in table return not found

    if 'Item' not in item:
        return {'result':'Email not found'}

    user = item['Item']

    if password != user['password']:
        return {'result':'Password not valid.'}

    #at this point, the email and password are correct
    session['email'] = user['email']
    session['username'] = user['username']

    result = {'result':'OK'}

    response = make_response(result)

    remember = request.args.get('remember', 'no')
    if remember == 'no':
        response.delete_cookie('remember')
    else:
        key = get_remember_key(user['email'])
        response.set_cookie('remember', key, max_age=60*60*24*14) # REMEMBER FOR 14 DAYS

    return response

def auto_login():
    cookie = request.cookies.get('remember')
    if cookie is None:
        return False

    table = get_public_table('Remember')
    result = table.get_item(Key={'key':cookie})
    if 'Item' not in result:
        return False

    remember = result['Item']
    email = remember['email']

    table = get_public_table('Users')
    result = table.get_item(Key={'email':email})

    user = result['Item']

    session['email'] = user['email']
    session['username'] = user['username']

    return True

#####################################








def dashboard():
    return "Welcome Home!"

def about():
    return "Omari is a student."

def add():
    a = request.args.get('a')
    b = request.args.get('b')
    result = int(a) + int(b)

    return str(result) # need to return a string or dictionary

def schedule(search):
    f = open('/home/omariBrockington14/data/courses.json')
    courses = json.load(f)
    f.close()

    result_list = []
    search = search.lower()
    for course in courses:
        if search in course['number'].lower() or search in course['name'].lower():
            result_list.append(course)

    return { 'result': result_list }


def account():
    user = check_login()
    if user is None:
        return redirect('/')
    else:
        return 'Hello' + " " + user['name']

def check_login():
    return {'name': 'Omari'}

def find_course(number):
    number = number.lower()
    f = open('/home/omariBrockington14/data/courses.json')
    courses = json.load(f)
    f.close()

    for course in courses:
        if course['number'].lower() == number:
            return course

    return {}


def find_home(title):
    title = title.lower()
    f = open('/home/omariBrockington14/data/homes.json')
    homes = json.load(f)
    f.close()

    for home in homes:
        if home['title'].lower() == title:
            return home

    return {}



def home(search):
    f = open('/home/omariBrockington14/data/homes.json')
    homes = json.load(f)
    f.close()

    result_list = []
    search = search.lower() if search else ''
    sort = request.args.get("sort")
    rooms = request.args.get("bedrooms")



    for home in homes:
        if search in home['title'].lower() or search in home['description'].lower():
            if rooms == 'any':
                result_list.append(home)
            elif rooms == 'one':
                if int(home['num_bedrooms']) >= 1:
                    result_list.append(home)
            elif rooms == 'two':
                if int(home['num_bedrooms']) >= 2:
                    result_list.append(home)



    if sort == 'ascending':
        result_list.sort(key=lambda x: float(x['rent'].replace('$', '').replace(',','')))
    elif sort == 'descending':
        result_list.sort(key=lambda x: float(x['rent'].replace('$', '').replace(',','')), reverse=True)

    return { 'result': result_list }

######################################################################
# Final Project: Twitter
def createAccount():
    table = get_public_table('Users')

    email = request.args.get('email', '')
    password = request.args.get('password', '')
    username = request.args.get('username', '')

    if email == '' or password == '' or username == '':
        return {'result':'Bad Login'}

    if '@' not in email or '.' not in email:
        return {'result':'Invalid Email'}

    item = table.get_item(Key={'email':email}) #trying to find email in table, if it's not found in table return not found
    if 'Item' not in item:
        temp = ''
    else:
        check = item['Item']
        if email == check['email']:
            return {'result':'Email Already In Use!.'}

    user = {'username': username,
            'email': email,
            'password': password}

    table.put_item(Item=user)

    item = table.get_item(Key={'email':email})
    user = item['Item']

    session['email'] = user['email']
    session['username'] = user['username']


    return { 'result' : 'OK' }

###################################################################

def loginTwitter():
    email = request.args.get('email', '')
    password = request.args.get('password', '')

    if email == '' or password == '':
        return {'result':'Bad Login'}

    table = get_public_table('Users')
    item = table.get_item(Key={'email':email}) #trying to find email in table, if it's not found in table return not found

    if 'Item' not in item:
        return {'result':'Email not found'}

    user = item['Item']

    if password != user['password']:
        return {'result':'Password not valid.'}

    #at this point, the email and password are correct
    session['email'] = user['email']
    session['username'] = user['username']

    result = {'result':'OK'}

    response = make_response(result)

    remember = request.args.get('remember', 'no')
    if remember == 'no':
        response.delete_cookie('remember')
    else:
        key = get_remember_key(user['email'])
        response.set_cookie('remember', key, max_age=60*60*24*14) # REMEMBER FOR 14 DAYS

    return response

def uploadprofilepic():
    bucket = get_public_bucket()
    table = get_public_table('ProfilePics')

    file = request.files["file"]

    filename = file.filename

    #You can get other form elements like this: x = request.form.get('x')
    profilepicID = str(uuid.uuid4())


    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = 'image/png'



    profilepic = {'ProfileID': profilepicID,
            'Username': session['username']}

    bucket.upload_fileobj(file, session['username'], ExtraArgs={'ContentType': ct })
    table.put_item(Item=profilepic)
    return { 'results' : 'OK' }

def showprofilepic():
    table = get_public_table('ProfilePics')
    current_user = session['username']

    user_found = False

    items = []

    for item in table.scan()['Items']:
        if item['Username'] == current_user:
            items.append({'ProfileID': item['ProfileID'], 'Username': item['Username']})
            user_found = True
            break

    if not user_found:
        items.append({'ProfileID': 0000, 'Username': 'Default_Profile.png'})
    return { 'url' : 'https://obrockington-web-public.s3.us-east-1.amazonaws.com/', 'items': items }

def postTweet():
    table = get_public_table('Tweet')


    tweet = request.args.get("tweet")
    # make if statement if tweet empty and use js to send alert to user

    if tweet == "":
        return { 'results' : 'Please Enter Text' }

    TweetID = str(uuid.uuid4())

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    Date = today + " " + current_time

    tweets = {'TweetID': TweetID,
            'Username': session['username'],
            'Tweet': tweet,
            'Date': Date}


    table.put_item(Item=tweets)

    return { 'results' : 'OK' }

def reply():
    table = get_public_table('Replies')

    TweetID = request.args.get('TweetID')


    reply = request.args.get("reply")
    # make if statement if tweet empty and use js to send alert to user

    if reply == "":
        return { 'results' : 'Please Enter Text' }

    replyID = str(uuid.uuid4())

    today = date.today()
    today = today.strftime("%Y-%m-%d")
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    Date = today + " " + current_time

    replies = {'ReplyID': replyID,
            'TweetID' : TweetID,
            'Username': session['username'],
            'Reply': reply,
            'Date': Date}


    table.put_item(Item=replies)

    return { 'results' : 'OK' }

def listTweet():
    table = get_public_table('Tweet')
    items = []
    for item in table.scan()['Items']:
        d = {'TweetID': item['TweetID'], 'Username': item['Username'], 'Tweet':item['Tweet'], 'Date':item['Date']}
        items.append(d)

    items = sorted(items, key=lambda x: x['Date'], reverse=True)
    return {'items': items }

def listReply():
    table = get_public_table('Replies')
    items = []
    TweetID = request.args.get('TweetID')
    for item in table.scan()['Items']:
        if item['TweetID'] == TweetID:
            d = {'ReplyID': item['ReplyID'], 'Username': item['Username'], 'Reply':item['Reply'], 'TweetID': item['TweetID'], 'Date':item['Date']}
            items.append(d)

    items = sorted(items, key=lambda x: x['Date'], reverse=True)
    return {'items': items }


def editTweets():
    table = get_public_table('Tweet')
    items = []
    current_user = session['username']

    for item in table.scan()['Items']:
        if current_user == item['Username']:
            d = {'TweetID': item['TweetID'], 'Username': item['Username'], 'Tweet':item['Tweet'], 'Date':item['Date']}
            items.append(d)


    items = sorted(items, key=lambda x: x['Date'], reverse=True)
    return {'items': items }

def deleteTweet():
    table = get_public_table('Tweet')

    TweetID = request.args.get("TweetID")


    table.delete_item(Key={'TweetID': TweetID})



    return { 'results' : 'OK' }

def viewProfile():
    table = get_public_table('Users')

    user = request.args.get('username')

    result = {'result' : 'Not Found'}

    for item in table.scan()['Items']:
        if user == item['username']:
            result = {'result': user }
            break



    return result

def showTweet():
    table = get_public_table('Tweet')
    username = request.args.get('username')
    items = []

    for item in table.scan()['Items']:
        if username == item['Username']:
            d = {'TweetID': item['TweetID'], 'Username': item['Username'], 'Tweet':item['Tweet'], 'Date':item['Date']}
            items.append(d)

    items = sorted(items, key=lambda x: x['Date'], reverse=True)
    return {'items': items }

def viewprofilePic():
    table = get_public_table('ProfilePics')
    username = request.args.get('username')

    user_found = False

    items = []

    for item in table.scan()['Items']:
        if item['Username'] == username:
            items.append({'ProfileID': item['ProfileID'], 'Username': item['Username']})
            user_found = True
            break

    if not user_found:
        items.append({'ProfileID': 0000, 'Username': 'Default_Profile.png'})
    return { 'url' : 'https://obrockington-web-public.s3.us-east-1.amazonaws.com/', 'items': items }

#####################################