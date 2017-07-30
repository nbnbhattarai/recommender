window.fbAsyncInit = function() {
  FB.init({
    appId            : '432605433783166',
    autoLogAppEvents : true,
    xfbml            : true,
    version          : 'v2.10'
  });
  FB.getLoginStatus(function(response){
    statusChangeCallback(response)
  });
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/sdk.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

function statusChangeCallback(response){
	if(response.status == 'connected'){
		console.log("logged in and authenticated");
    var uid = response.authResponse.uerID;

		setElements(true);
		testAPI();
	}else{
		console.log("logged out");
		setElements(false);
	}
}

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

function testAPI(){
  // get data if not alredy loggedin
  console.log("Outside getCookie");
  var session_cookie = getCookie('sessionid')
  var logined_cookie = getCookie('logined')
  console.log('session_cookie: ', session_cookie, ' logined_cookie: ', logined_cookie);
  if (session_cookie == null){
    console.log('Inside getCookie');
    FB.api('/me?fields=name,id,posts.limit(999)', function(response){
      if(response && !response.error){
          // getting posts to send to django server
          var posts = {};
          var i = 0;
          for (let x in response.posts.data){
            console.log('inside')
            if(response.posts.data[x].message){
              posts[i] = response.posts.data[x].message;
              i++;
            }
          }
          console.log(posts)
          var json_posts = JSON.stringify(posts);
          var to_django = {'name': response.name, 'id': response.id, 'posts' : json_posts };
          post_to_url('http://localhost:8000', to_django)
          console.log(to_django);
        }
        console.log('buildProfile');
        buildProfile(response);
        buildFeed(posts)
      });
  }else{
    console.log('Already Loggedin');
  }
}

function setElements(isLoggedIn){
	if(isLoggedIn){
    document.getElementById('fb-logout-btn').style.display = 'block';
    document.getElementById('login-segment').style.display = 'none';
    //document.getElementById('feed').style.display = 'block';
    document.getElementById('fb-login-btn').style.display = 'none';
    //document.getElementById('heading').style.display = 'none';
	}else{
    document.getElementById('fb-logout-btn').style.display = 'none';
    document.getElementById('login-segment').style.display = 'block';
    //document.getElementById('feed').style.display = 'none';
    document.getElementById('fb-login-btn').style.display = 'block';
    //document.getElementById('heading').style.display = 'block';
	}
}

function logout(){
  FB.logout(function(response){
    setElements(false);
    window.location = "http://localhost:8000/logout"
  });
}

function buildProfile(user){
	let profile = `<h3>Welcome ${user.name}</h3>
			<ul class ="list-group">
			<li class="list-group-item">User ID: ${user.id}</li>
      <li class="list-group-item "> Latest Post: ${user.posts.data[0].message}</li>
			</ul>
	`;
	document.getElementById('profile').innerHTML = profile;
}

function buildFeed(posts){
  let output = '<h3>Latest Posts</h3>';
  for(let i in posts.data){
    if(posts.data[i].message){
      console.log('Message :' + posts.data[i].message);
      output += `
        <div class="well">
          ${posts.data[i].message} <span>${posts.data[i].created_time}</span>
        </div>
      `;
    }
  }

  document.getElementById('feed').innerHTML = output;
}

// Sending data to django server using post method
// jQuery for csrf validation
// get cookie using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    csrfField = document.createElement("input");
    var csrftoken = getCookie('csrftoken')
    console.log("token" + csrftoken)
    csrfField.setAttribute("type", "hidden");
    csrfField.setAttribute("name", "csrfmiddlewaretoken");
    csrfField.setAttribute("value", csrftoken)
    form.appendChild(csrfField)

    document.body.appendChild(form);
    form.submit();
}

function getCookie2(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    // because unescape has been deprecated, replaced with decodeURI
    //return unescape(dc.substring(begin + prefix.length, end));
    return decodeURI(dc.substring(begin + prefix.length, end));
}
