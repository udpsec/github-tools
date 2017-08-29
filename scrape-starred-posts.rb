# Script to download starred posts from Google Reader (including post content).
# Requires that your starred posts are in a public feed.
#
# You can find the public feed by going to "Reader settings", then "Folders and Tags",
# setting "starred items" to public and then going to "view public page". That url is the
# one to pass to the script.
#
# I guess it would work for other folders too.
#
# Usage:
#
#   ruby scrape-starred-posts.rb "http://view public page starred posts link" > all_starred_posts.json

require 'net/http'
require 'nokogiri'
require 'json'

module GoogleReader
  class StarredFetcher
    class Page
      def initialize(url)
        @url = url
        $stderr.puts "new page:" + @url
      end

      def html
        @html ||= Net::HTTP.get(URI.parse(@url))
      end

      def doc
        @doc ||= Nokogiri::HTML(html)
      end

      def items
        doc.search(".item").map {|el| Item.new(el) }
      end

      def next
        Page.new(next_page_url) if next_page_url
      end

      def next_page_url
        doc.search("#more").first.search("a").first.attributes["href"].value
      rescue
        nil
      end
    end

    class Item
      def initialize(el)
        @el = el
      end

      def title
        @el.search(".item-title").text
      end

      def href
        @el.search(".item-title").children.first.children.first.attributes["href"].value
      end

      def blog_href
        blog_info.first.search("a").first.attributes["href"].value
      end

      def blog_title
        blog_info.first.search("a").first.text
      end

      def author
        blog_info.map {|e| e.text =~ /by (.*) on/; $1 }.compact.first
      end

      def blog_info
        @item_info ||= @el.search(".item-info")
      end

      def date
        blog_info.map {|e| e.text =~ /on (\d\d?\/\d\d?\/\d\d?)/; $1}.compact.first
      end

      def body
        @el.search(".item-body").children.to_s
      end

      def to_hash
        {:title => title, :href => href, :blog => {:href => blog_href, :title => blog_title}, :author => author, :date => date, :body => body}
      end
    end

    def initialize(first_page_url)
      @first_page_url = first_page_url
    end

    def first_page
      Page.new(@first_page_url)
    end

    def each_item
      @all ||= begin
        page = first_page
        while page
          page.items.each do |item|
            yield item
          end
          page = page.next
        end
      end
    end
  end
end

page_one = ARGV[0]
$stderr.puts "starting scrape at #{page_one}"
fetcher = GoogleReader::StarredFetcher.new(page_one)
puts "["
fetcher.each_item do |item|
  print JSON.pretty_generate(item.to_hash)
  puts ","
end
puts "  null"
puts "]"