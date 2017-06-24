  window.fbAsyncInit = function() {
    FB.init({
      appId      : '432605433783166',
      xfbml      : true,
      version    : 'v2.9'
    });
	  FB.getLoginStatus(function(response){
		  statusChangeCallback(response);
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
		console.log("logged in");
		setElements(true);
		testAPI();
	}else {
		console.log("logged out");
		setElements(false);
	}
	logout.onclick = function(){
		FB.logout(function(response){
		setElements(false);
		});
	}
}
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}
function setElements(isLoggedIn){
	if(isLoggedIn){
		document.getElementById('profile').style.display='block';
		//document.getElementById('form').style.display='block';
		document.getElementById('fb-btn').style.display='none';
		document.getElementById('startMsg').innerHTML =""
		document.getElementById('personalityInfo').innerHTML="Your Personality";
		document.getElementById('recommendation').innerHTML="Recommendation";
	}else{
		document.getElementById('profile').style.display='none';
		//document.getElementById('form').style.display='none';
		document.getElementById('fb-btn').style.display='block';
		document.getElementById('startMsg').innerHTML ="Log in to determine your personality"
		document.getElementById('state').innerHTML = "" 
		document.getElementById('personalityInfo').innerHTML='';
		document.getElementById('recommendation').innerHTML='';
		document.getElementById('personality').style.display='none';

	}
}

function testAPI(){
	FB.api('/me?fields=name,posts',function(response){
		if(response && !response.error){
			console.log(response)
			buildProfile(response);
		}
	});
}
function buildProfile(user){
	let profile = `<h3>Welcome ${user.name}</h3> 
			<ul class ="list-group">
			<li class="list-group-item">User ID: ${user.id}</li>
			<li class="list-group-item "> Latest Post: ${user.posts.data[0].story}</li>
			</ul>
	`;
	let posts =`${user.posts.data[0].story}`;
	document.getElementById('state').innerHTML = profile;
	document.getElementById('posts').innerHTML = posts;
}
