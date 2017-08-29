# https://github.com/octokit/octokit.rb

require 'octokit'
Octokit.configure do |c|
  c.login =  ENV['GH_UID']
  c.password = ENV['GH_PWD']
end

begin; Octokit.starred.each {|r| puts Octokit.client.unstar r.full_name}; end while Octokit.starred.size > 0;