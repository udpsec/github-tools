
import sys
import time
import concurrent.futures
from queue import Queue

from github import Github


def remove_star(user, q_starred_reports):
    repo = q_starred_reports.get(block=True)
    print("Removing: ", repo.full_name)
    while user.has_in_starred(repo):
        user.remove_from_starred(repo)
        # Be nice and don't hammer github's api.  Instead, throttle requests:
        time.sleep(1.5)


def purge_stars(user):
    q_starred_repos = Queue()
    repos = list(user.get_starred())
    for x in repos:
        q_starred_repos.put(x)

    print("\n\nYou have: {} starred repos.  Are you sure you want to remove __ALL"
          " OF THEM__ from your profile?\n".format(len(repos)))

    response = input("Enter 'Y' or 'N': ")

    if response.upper() != 'Y':
        sys.exit()

    print("\n\n** Proceeding with the great purge! **\n\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(remove_star, user, q_starred_repos) for x in repos]

    concurrent.futures.wait(futures)


def main(argv=sys.argv):
    try:
        # First argument:  username , Second argument:  password
        g = Github(argv[1], argv[2])
    except IndexError:
        print("\nERROR:  Must provide username and password as arguments:  "
              "purge_github_stars <username> <password>")
        sys.exit()

    purge_stars(g.get_user())
