#!/usr/bin/env ruby
# encoding: utf-8

# Usage:
# Export your bookmarks to HTML and then run
# GITHUB_USERNAME=username GITHUB_PASSWORD=password ./star_github_repositories.rb bookmarks.html

require "octokit"

class HTMLBookmarkFile < Struct.new(:path)
  def repos
    @repos ||= begin
      content = File.read(path)
      _repos = content.scan(%r{https?://github\.com/([^:?]+?)/([^:?]+?)[/"]})
      _repos.map { |(owner, repo)| Repo.new(owner, repo) }
    end
  end
end

Github = Octokit::Client.new(login: ENV['GITHUB_USERNAME'], password: ENV['GITHUB_PASSWORD'])

class Repo < Struct.new(:owner, :repo)
  def full_name
    [owner, repo].join('/')
  end

  def star!
    Github.star(full_name)
  end

  def unstar!
    Github.unstar(full_name)
  end

  def starred?
    Github.root.rels[:starred].send(method, uri: {owner: owner, repo: repo}).status == 204
  rescue => e
    false
  end
end

bookmark_file_path = ARGV[0]
abort if bookmark_file_path.nil? or bookmark_file_path.empty?

HTMLBookmarkFile.new(bookmark_file_path).repos.each do |repo|
  if repo.starred?
    state = "STARRED"
  else
    state = repo.star! ? "SUCCESS" : "ERROR  "
  end
  puts "[#{state}] starring #{repo.full_name}"
end