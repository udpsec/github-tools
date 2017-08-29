require 'octokit'
require 'pry'
require 'awesome_print'

Octokit.configure do |conf|
  conf.login = ''
  conf.password = ''
end

rate_limit = Octokit.client.rate_limit
puts '-' * 10
puts "GitHub API Rate Limit: #{rate_limit.remaining}/#{rate_limit.limit}\n"
puts '-' * 10

furu = Octokit.user('furu')

starred = furu.rels[:starred].get

starred_repos = []

starred_repos += starred.data

repo = starred_repos.first

puts <<EOS

#{repo.name}
---

* id                : #{repo.id}
* owener            : #{repo.owner.login}
* repository name   : #{repo.name}
* description       : #{repo.description}
* repository url    : https://github.com/#{repo.full_name}
* stargazers count  : #{repo.stargazers_count}
* language          : #{repo.language}
* owner avatar url  : 
* subscribers count : #{repo.rels[:self].get.data.subscribers_count}

EOS

# while starred.rels.has_key?(:next)
  # starred = starred.rels[:next].get

  # starred_repos += starred.data

  # sleep 1
# end

rate_limit_remaining_after_used = Octokit.client.rate_limit.remaining
consumed_api_count = rate_limit.remaining - rate_limit_remaining_after_used
puts '-' * 10
puts "Consumed GitHub API: #{consumed_api_count}\n"
puts '-' * 10

binding.pry