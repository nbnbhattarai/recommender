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
		setElements(true);
		testAPI();
	}else {
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
    FB.api('/me?fields=name,id,feed', function(response){
      if(response && !response.error){
        console.log('fucking response 1')
        console.log(response);
        if (!getCookie('logined')){
          var to_django = {'name': response.name, 'id': response.id, 'status_data' : response.feed.data };
          post_to_url('http://localhost:8000', response)
        }
        buildProfile(response);
        buildFeed(response.feed)
      }

      // FB.api('/me/feed', function(response){
      //   if(response && !response.error){
      //     console.log('fucking response 2')
      //     console.log(response)
      //     buildFeed(response);
      //   }
      // });
    })
  }

function setElements(isLoggedIn){
	if(isLoggedIn){
    document.getElementById('logout').style.display = 'block';
    document.getElementById('profile').style.display = 'block';
    document.getElementById('feed').style.display = 'block';
    document.getElementById('fb-btn').style.display = 'none';
    document.getElementById('heading').style.display = 'none';
	}else{
    document.getElementById('logout').style.display = 'none';
    document.getElementById('profile').style.display = 'none';
    document.getElementById('feed').style.display = 'none';
    document.getElementById('fb-btn').style.display = 'block';
    document.getElementById('heading').style.display = 'block';
	}
}

function logout(){
  FB.logout(function(response){
    // $.removeCookie('logined', { path: '/' });
    setElements(false);
    window.location = "http://localhost:8000/logout"
  });
}

function buildProfile(user){
	let profile = `<h3>Welcome ${user.name}</h3>
			<ul class ="list-group">
			<li class="list-group-item">User ID: ${user.id}</li>
      <li class="list-group-item "> Latest Post: ${user.feed.data[0].story}</li>
			</ul>
	`;
	document.getElementById('profile').innerHTML = profile;
}

function buildFeed(feed){
  let output = '<h3>Latest Posts</h3>';
  for(let i in feed.data){
    if(feed.data[i].message){
      output += `
        <div class="well">
          ${feed.data[i].message} <span>${feed.data[i].created_time}</span>
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
