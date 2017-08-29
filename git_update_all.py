## USAGE

# Before running this
#   ...

# Command line
# python git_update_all.py


import getpass
import glob
import json
import os
import re
import requests
from urlparse import urljoin
from subprocess import call


SCRIPT_VERSION = "0.0.1"
GITHUB_API = "https://api.github.com"

path = ""
username = ""
password = ""


def userInput():
    global path
    global username
    global password

    path = raw_input("[git_update_all] > Environment path: ")
    username = raw_input("[git_update_all] > Github username: ")
    password = getpass.getpass("[git_update_all] > Github password: ")


def buildBaseDirectory(path):
    print "[git_update_all] BUILD BASE DIRECTORY"

    path = os.path.abspath(path)
    os.chdir(path)
    baseDirectory = os.path.join(path, "dev")

    if not os.path.exists(baseDirectory):
        os.makedirs(baseDirectory)

    return baseDirectory

def buildUserDirectory(baseDirectory):
    print "[git_update_all] BUILD USER DIRECTORY"

    os.chdir(baseDirectory)
    userDirectory = os.path.join(baseDirectory, username)

    if not os.path.exists(userDirectory):
        os.makedirs(userDirectory)

    return userDirectory

def buildOrganizationDirectory(baseDirectory, organization):
    print "[git_update_all] BUILD ORGANIZATION DIRECTORY (%s)" % organization

    os.chdir(baseDirectory)
    organizationDirectory = os.path.join(baseDirectory, organization)

    if not os.path.exists(organizationDirectory):
        os.makedirs(organizationDirectory)

    return organizationDirectory

def buildStarredDirectory(baseDirectory):
    print "[git_update_all] BUILD STARRED DIRECTORY"

    os.chdir(baseDirectory)
    starredDirectory = os.path.join(baseDirectory, "starred")

    if not os.path.exists(starredDirectory):
        os.makedirs(starredDirectory)

    return starredDirectory


def getAuthorization():
    print "[git_update_all] GET GITHUB AUTHORIZATION"

    url = urljoin(GITHUB_API, "authorizations")
    payload = {"scopes": ["repo"], "note": "git_update_all.py"}

    response = requests.post(url, auth=(username, password), data=json.dumps(payload))
    j = json.loads(response.text)

    if response.status_code == 401 and response.headers["X-GitHub-OTP"]:
        code = raw_input("[git_update_all] > Github authentication code: ")

        headers = {"X-GitHub-OTP": code}
        response = requests.post(url, auth=(username, password), data=json.dumps(payload), headers=headers)
        j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return

    return j

def deleteAuthorization(authorization):
    print "[git_update_all] DELETE GITHUB AUTHORIZATION"

    payload = {"access_token": authorization["token"]}

    url = authorization["url"]
    response = requests.delete(url, data=json.dumps(payload))
    j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return


def getUserRepositories(token, userDirectory, link=None):
    if link is None:
        print "[git_update_all] GET USER'S REPOSITORIES"
        url = urljoin(GITHUB_API, "user/repos")
    else:
        url = link

    payload = {"access_token": token}

    response = requests.get(url, params=payload)
    j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return

    for repo in j:
        cloneOrPullRepository(repo, userDirectory)

    if "next" in response.links:
        getUserRepositories(token, userDirectory, response.links["next"]["url"])

def getUserOrganizations(token):
    print "[git_update_all] GET USER'S ORGANIZATIONS"

    url = urljoin(GITHUB_API, "user/orgs")
    payload = {"access_token": token}

    response = requests.get(url, params=payload)
    j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return

    return j

def getOrganizationRepositories(token, organization, organizationDirectory, link=None):
    if link is None:
        print "[git_update_all] GET ORGANIZATION'S REPOSITORIES (%s)" % organization["login"]
        url = urljoin(GITHUB_API, organization["repos_url"])
    else:
        url = link

    payload = {"access_token": token}

    response = requests.get(url, params=payload)
    j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return

    for repo in j:
        cloneOrPullRepository(repo, organizationDirectory)

    if "next" in response.links:
        getOrganizationRepositories(token, organization, organizationDirectory, response.links["next"]["url"])

def getStarredRepositories(token, starredDirectory, link=None):
    if link is None:
        print "[git_update_all] GET USER'S STARRED REPOSITORIES"
        url = urljoin(GITHUB_API, "user/starred")
    else:
        url = link

    payload = {"access_token": token}

    response = requests.get(url, params=payload)
    j = json.loads(response.text)

    if response.status_code >= 400:
        msg = j.get("message", "UNDEFINED ERROR (no error description from server)")
        print "[!!!!!!!!!!!!!!] ERROR: %s" % msg
        return

    for repo in j:
        cloneOrPullRepository(repo, starredDirectory)

    if "next" in response.links:
        getStarredRepositories(token, starredDirectory, response.links["next"]["url"])


def cloneOrPullRepository(repo, currentDirectory):
    print "[git_update_all] CLONE OR PULL REPOSITORY (%s)" % repo["name"]

    os.chdir(currentDirectory)
    repoDirectory = os.path.join(currentDirectory, repo["name"])

    if os.path.exists(repoDirectory):
        os.chdir(repoDirectory)
        call(["git", "pull"])
    else:
        call(["git", "clone", repo["ssh_url"]])



def main():
    print "[git_update_all] GIT UPDATE ALL"

    userInput()
    authorization = getAuthorization()

    baseDirectory = buildBaseDirectory(path)

    userDirectory = buildUserDirectory(baseDirectory)
    getUserRepositories(authorization["token"], userDirectory)

    organizations = getUserOrganizations(authorization["token"])

    for organization in organizations:
        clone = raw_input("[git_update_all] > Clone organization \"%s\" ? (y/n): " % organization["login"])

        if clone == "y":
            organizationDirectory = buildOrganizationDirectory(baseDirectory, organization["login"])
            getOrganizationRepositories(authorization["token"], organization, organizationDirectory)

    starredDirectory = buildStarredDirectory(baseDirectory)
    getStarredRepositories(authorization["token"], starredDirectory)

    deleteAuthorization(authorization)


if __name__ == "__main__":
    main()
