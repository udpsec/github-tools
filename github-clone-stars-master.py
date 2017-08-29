#!/usr/bin/env python3
__author__ = 'pete404'
if __name__ == '__main__':
    import json, argparse
    
    import requests
    
    parser = argparse.ArgumentParser(description="Clones all of a github user's starred repositories.")
    
    parser.add_argument("user", help="The github user of the starred repositories.")
    parser.add_argument("-v", "--verbose", help="Enables verbose output.", action="store_true")
    parser.add_argument("--bare", help="Enables cloning to a bare git repository.", action="store_true")
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Username: ", args.user, "\nBare repository? ", args.bare)
        print("Connecting...")
    
    header = {"user-agent" : "pete404/github-clone-stars"}
    #Following api documentation at: https://developer.github.com/v3/activity/starring/#list-repositories-being-starred
    star_request = requests.get("http://api.github.com/users/" + args.user + "/starred", headers=header)
    #alternatively access the user url, parse the starred url, and access it (more requests though)
    #star_request = requests.get("http://api.github.com/users/" + args.user, headers=header)
    #user = json.loads(star_request.json())
    #
    #
    
    if args.verbose:
        print("Parsing request")
    
    stars = json.loads(star_request.json())
    
    print(stars[1]["clone_url"])