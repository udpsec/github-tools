#!/usr/bin/env python
""" Fed up with GitHub stars being essentially useless, I decided to give them
    some purpose.

    Run this script occasionally (via cron or similar) to keep a local and
    up-to-date copy of your starred repos (and even delete repos which
    have been unstarred!).

    Three variables may or may not need configuring to run this script in your
    environment, they are ``github_username``, ``starred_dir`` and ``cleanup``.
    Their purpose should be somewhat obvious.
"""
from __future__ import print_function

import getpass
import os
import subprocess

import requests

GITHUB_USERNAME = getpass.getuser()
STARRED_DIR = os.path.expanduser('~/Source/Starred')
DELETE_UNSTARRED = True


def main(user, dest, cleanup):
    """
        ``user`` - GitHub username
        ``dest`` - Destination folder for Starred repos
        ``cleanup`` - Delete repos that have been Unstarred
    """
    url = 'https://api.github.com/users/{}/starred'.format(user)
    starred_repos = {}
    page = 1
    while True:
        data = requests.get(url, params=dict(per_page=100, page=page)).json()
        if not data:
            break
        for repo in data:
            repo_dir = repo['full_name'].replace('/', '_')
            starred_repos[repo_dir] = repo['clone_url']
        page += 1
    for (repo_name, repo_url) in starred_repos.iteritems():
        workdir = os.path.join(dest, repo_name)
        if os.path.isdir(workdir):
            cmd = ['git', '-C', workdir, 'pull']
        else:
            cmd = ['git', 'clone', repo_url, workdir]
        print("Processing {}".format(repo_name))
        subprocess.call(cmd)
    if cleanup:
        for repo in os.listdir(dest):
            repo_path = os.path.join(dest, repo)
            if not os.path.isdir(repo_path) or repo.startswith('.'):
                continue
            if repo not in starred_repos:
                subprocess.call(['rm', '-r', repo_path])

if __name__ == '__main__':
    main(GITHUB_USERNAME, STARRED_DIR, DELETE_UNSTARRED)