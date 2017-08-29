/*

nodejs

Clone all starred repositories
Planned on running this on a cron to clone/pull repos I have starred.

Right now can only do the first 30 because of github api limit.
Need to paginate!

It's sloppy. It's dirty. But it werks.

requires: readline-sync, request

inspired from: http://paazmaya.com/clone-your-starred-github-repositories-via-script

*/


var fs = require('fs');

// Used for pagination in future
var pageCount = 3;

var cloneUrls = [];

// Grab User & Pass, or hardcode it
var readlineSync = require('readline-sync');
var user = readlineSync.question('username: ');
var pass = readlineSync.question('password: ');

// For hardcoding uses:
/*
var user      = [username]
var pass  = [password]
*/

var request = require('request'),
    username = user,
    password = pass,
    url = "https://api.github.com/user/starred",
    auth = "Basic " + new Buffer(username + ":" + password).toString("base64");

request(
    {
        url : url,
        headers : {
            'User-Agent': 'request',
            "Authorization" : auth
        }
    },
    function (error, response, body) {
        gitStarred(body);
    }
);


// Parse the json response
function gitStarred(response) {
  response.toString();
  var data = JSON.parse(response);
    data.forEach(function (item) {
    cloneUrls.push(item.clone_url);
  });


// If clone fails, try pulling
function gitPull(url) {
    console.log("Already cloned, Pulling instead....");
    var repo = url.match(/\w(\-|\w)+.git/);
    repo = repo[0];
    repo = repo.split(".");
    exec('git -C ' + repo[0] + ' pull',  function (error, stdout, stderr) {
            //console.log('stderr: ' + stderr);
    });
}

console.log('Amount of starred repositories: ' + cloneUrls.length);


var exec = require('child_process').exec;
var next = function (index) {
  if (index >= cloneUrls.length) {
    return;
  }
  var url = cloneUrls[index];

  exec('git clone ' + url, function (error, stdout, stderr) {
    console.log("Cloning: " + url);
    if (error !== null) {
      gitPull(url);
    }
    next(++index);
  });

};
next(0);
}
