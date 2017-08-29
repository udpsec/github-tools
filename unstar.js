var github = require('github');
var util = require('util');

const TOKEN = "";
const USER = "";

var g = new github({version: "3.0.0"});

g.authenticate({
    type: "oauth",
    token: TOKEN
});

g.repos.getStarredFromUser({
    user: USER,
    page: 0
}, cb);

function cb(err, res) {
    if(util.isArray(res)) {
        res.forEach(function(repo) {
            g.repos.unStar({
                user: repo.owner.login,
                repo: repo.name
            }, function() {
                console.log("unStar " + repo.full_name);
            });
        });
    }

    if(g.hasNextPage(res.meta.link)) {
        g.getNextPage(res.meta.link, cb);
    }
}
