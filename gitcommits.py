import requests
from requests.auth import HTTPBasicAuth

list_of_repos = []
fork_score, star_score, commit_score = (0,)*3

#Note, you cannot get ALL commits a user has ever made. What this script does is iterate through a user's local repositories
#and count how many git commits have been made and how many times a repository of yours has been forked or starred
def compile_raw_gitscore(username='arshbot'):
    get_user_repos(username)
    get_num_of_github_commits(username)
    get_num_of_stars_and_forks(username)
    return {'fork_score': fork_score, 'star_score': star_score, 'commit_score': commit_score}

def get_user_repos(username='arshbot'):
    global list_of_repos
    r = requests.get('https://api.github.com/users/'+username+'/repos', auth=HTTPBasicAuth('arshbot', 'e172a7f23e13fc855016bb391bd5f504f3f13d86'))
    repos = r.json()
    if str(r) == '<Response [404]>':
        print "Shit ain't found"
        return []
    elif str(r) == '<Response [200]>':
        for r in repos:
            list_of_repos.append(r['name'])
        #print list_of_repos
        return list_of_repos

def get_num_of_stars_and_forks(username='arshbot'):
    global fork_score 
    global star_score
    for r in list_of_repos:
        rc = requests.get('https://api.github.com/repos/'+username+'/'+r, auth=HTTPBasicAuth('arshbot', 'e172a7f23e13fc855016bb391bd5f504f3f13d86'))
        rc_json = rc.json()
        fork_score += rc_json['forks']
        star_score += rc_json['stargazers_count']

def get_num_of_github_commits(username='arshbot'):
    global list_of_repos
    global commit_score
    for r in list_of_repos:
        rc = requests.get('https://api.github.com/repos/'+username+'/'+r+'/commits', auth=HTTPBasicAuth('arshbot', 'e172a7f23e13fc855016bb391bd5f504f3f13d86'))
        if str(r) == '<Response [404]>':
            print "Shit ain't found for your repo: "+r
            break
        repos=rc.json()
        commit_score+=len(repos)