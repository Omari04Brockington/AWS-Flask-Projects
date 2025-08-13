function loadDoc(url, func) {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error");
        } else {
            func(xhttp.response);
        }
    }
    xhttp.open("GET", url);
    xhttp.send();

}

function signup() {
    window.location.replace('/twittersign.html');
}

function signin() {
    window.location.replace('/twitterlogin.html');
}

function feed() {
    window.location.replace('twitterfeed.html');
}

function profile() {
    window.location.replace('twitteraccount.html')
}

function create_account() {
    let txtUser = document.getElementById("txtUser");
    let newPassword = document.getElementById("newPassword");
    let newEmail = document.getElementById("newEmail");


    let URL = "/example/createAccount?username=" + txtUser.value + "&password=" + newPassword.value + "&email=" + newEmail.value;


    loadDoc(URL, create_account_response);
}


function create_account_response(response) {
    let data = JSON.parse(response);
    let result = data["result"]
    if (result != 'OK') {
        alert(result);
    } else {
        result = "Welcome to The Lounge!";
        alert(result);
        window.location.replace('/twitteraccount.html');
    }

}

function login() {
    let txtEmail = document.getElementById("txtEmail");
    let txtPassword = document.getElementById("txtPassword");
    let chkRemember = document.getElementById("chkRemember");

    let URL = "/example/loginTwitter?email=" + txtEmail.value + "&password=" + txtPassword.value;
    if (chkRemember.checked) {
        URL += "&remember=yes";
    } else {
        URL += "&remember=no"
    }

    loadDoc(URL, login_response);
}

function login_response(response) {
    let data = JSON.parse(response);
    let result = data["result"];
    if (result != 'OK') {
        alert(result);
    } else {
        window.location.replace('/twitteraccount.html');
    }
}


function upload_profile_pic() {
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.status != 200) {
            console.log("Error")
        } else {
            upload_profile_pic_response(xhttp.response)
        }
    }

    xhttp.open('POST', '/example/uploadprofilepic', true)
    var formData = new FormData();
    formData.append('file', document.getElementById("image").files[0]);

    xhttp.send(formData);
}


function upload_profile_pic_response(response) {
    location.reload();
}

function show_profile_pic(){
    loadDoc('/example/showprofilepic', show_profile_pic_response);
}

function show_profile_pic_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let url = data["url"];
    let temp = "";
    let image = document.getElementById("image");
    for (let i = 0; i < items.length; i++) {
        temp += `
        <div class="profile-container">
            <img class="profile-image" src="${url}${items[i]['Username']}">
        </div>
        `;
    }

    let ProfilePic = document.getElementById("ProfilePic");
    ProfilePic.innerHTML = temp;

}

function tweet() {
    let tweet = document.getElementById("tweet").value;


    let URL = "/example/postTweet?tweet=" + tweet;


    loadDoc(URL, tweet_response);
}


function tweet_response(response) {
    let data = JSON.parse(response);
    let result = data['results']
    if (result === 'Please Enter Text') {
        alert(result);
    }
    else {
        let result = "You Posted!";
        alert(result);
        window.location.replace('/twitterfeed.html');
    }

}


function reply(TweetID) {
    let reply = document.getElementById("replies-" + TweetID).value;
    let URL = "/example/reply?TweetID=" + encodeURIComponent(TweetID)+ "&reply=" + encodeURIComponent(reply);


    loadDoc(URL, reply_response);
}


function reply_response(response) {
    let data = JSON.parse(response);
    let result = data['results']
    if (result === 'Please Enter Text') {
        alert(result);
    }
    else {
        let result = "You Responded!";
        alert(result);
        window.location.replace('/twitterfeed.html');
    }

}

function list_tweet() {
    loadDoc('/example/listTweet', list_tweet_response);
}

function list_tweet_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let temp = "";

    for (let i = 0; i < items.length; i++) {
        temp += `
            </br><div class="post-user">
            <button onclick="view_profile('${items[i]['Username']}')">${items[i]['Username']}️</button>
            <p class="post-tweet">${items[i]['Tweet']}</p>
            <div class="post-date">
                <p class="post-date">${items[i]['Date']}</p>
            </div>
                <div class="post-reply">
                    <a onclick="showReplies('${items[i]['TweetID']}');">Show</a> /
                    <a onclick="hide('reply-${items[i]['TweetID']}');">Hide Replies</a>
                    <div id="reply-${items[i]['TweetID']}" style="display: none;">
                        <div id="replyResults-${items[i]['TweetID']}"></div>
                        <br/><textarea id="replies-${items[i]['TweetID']}" rows="4" cols="50"></textarea>
                    <button onclick="reply('${items[i]['TweetID']}');">Reply!</button>
                    </div>
                </div>
        </div>
        `;
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;


}

function list_reply(TweetID) {
    let URL = '/example/listReply?TweetID=' + encodeURIComponent(TweetID);
    loadDoc(URL, function(response) {
        list_reply_response(response, TweetID);
    });
}


function list_reply_response(response, TweetID) {
    let data = JSON.parse(response);
    let items = data["items"];
    let temp = "";

    for (let i = 0; i < items.length; i++) {
        temp += `
            <div class="reply">
                <button onclick="view_profile('${items[i]['Username']}')">${items[i]['Username']}</button>
                <p class="post-reply">${items[i]['Reply']}</p>
                <div class="post-date">${items[i]['Date']}</div>
            </div>
        `;
    }

    let replyResults = document.getElementById("replyResults-" + TweetID);
    replyResults.innerHTML = temp;
}


function edit_tweets() {
    loadDoc('/example/editTweets', edit_tweets_response);
}

function edit_tweets_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let temp = "";

    for (let i = 0; i < items.length; i++) {
        temp += `
            <div class="post-tweet">
                <button onclick="delete_tweet('${items[i]['TweetID']}')">🗑️</button>
                <p class="post-tweet">${items[i]['Tweet']}</p>
                <div class="post-date">
                    <p class="post-date">${items[i]['Date']}</p>
                </div>
            </div>
        `;
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;

}

function delete_tweet(TweetID) {
    let URL = "/example/deleteTweet?TweetID=" + encodeURIComponent(TweetID);
    loadDoc(URL, delete_tweet_response);
}

function delete_tweet_response(response) {
    let data = JSON.parse(response);
    let result = "You Deleted a Post :(";
    window.location.replace('/twitterfeed.html');

}


function show_tweet() {
    const params = new URLSearchParams(window.location.search);
    const username = params.get('username');
    let URL = "/example/showTweet?username=" + encodeURIComponent(username);

    loadDoc(URL, show_tweet_response);
}

function show_tweet_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let temp = "";

    for (let i = 0; i < items.length; i++) {
        temp += `
            </br><div class="post-user">
            <p class="post-tweet">${items[i]['Tweet']}</p>
            <div class="post-date">
                <p class="post-date">${items[i]['Date']}</p>
            </div>
        </div>
        `;
    }

    let divResults = document.getElementById("divResults");
    divResults.innerHTML = temp;

}

function view_profile_pic() {
    const params = new URLSearchParams(window.location.search);
    const username = params.get('username');
    let URL = "/example/viewprofilePic?username=" + encodeURIComponent(username);

    loadDoc(URL, view_profile_pic_response);
}

function view_profile_pic_response(response) {
    let data = JSON.parse(response);
    let items = data["items"];
    let url = data["url"];
    let temp = "";
    let image = document.getElementById("image");
    for (let i = 0; i < items.length; i++) {
        temp += `
        <div class="profile-container">
            <img class="profile-image" src="${url}${items[i]['Username']}">
        </div>
        `;
    }

    let ProfilePic = document.getElementById("ProfilePic");
    ProfilePic.innerHTML = temp;

}

function view_profile(Username) {
    let URL = "/example/viewProfile?username=" + encodeURIComponent(Username);
    loadDoc(URL, view_profile_response);
}

function view_profile_response(response) {
    let data = JSON.parse(response);
    let result = data["result"];

    if (result === 'Not Found') {
        alert(result);
    }
    else {
        window.location.replace('/twitterviewer.html?username=' + encodeURIComponent(result));
    }
}

function show(name) {
    let div = document.getElementById(name);
    div.style.display = "block";
}

function hide(name) {
    let div = document.getElementById(name);
    div.style.display = "none";
}

function showReplies(TweetID) {
    show('reply-' + TweetID);
    list_reply(TweetID);
}

console.log("Script Loaded");