require "octokit"
require "pinboard"

# After running this script, you can use [this IFTTT recipe](https://ifttt.com/recipes/71035) 
# for future sync **automatically**.

pinboard = Pinboard::Client.new(:token => 'TOKEN') # get the token here: https://pinboard.in/settings/password
github = Octokit::Client.new(:login => 'USERNAME', :password => 'PASSWORD')
total_starred = 9999 # get the count here: https://github.com/stars

starred_repos = github.starred
last_response = github.last_response

while starred_repos.count < total_starred
  p last_response.rels[:next].href
  last_response = last_response.rels[:next].get
  starred_repos.concat last_response.data
end
github_repo_base_url = 'https://github.com/'
starred_repos.each.with_index do |repo, index|
  url = github_repo_base_url + repo.full_name
  p "#{index + 1} done #{total_starred - index - 1} left: #{url}"
  pinboard.add(
    :url => url,
    :description => repo.full_name,
    :extended => repo.description,
    :tags => ['github']
  )
end