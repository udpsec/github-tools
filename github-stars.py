import pandas as pd
from github import Github

g = Github("username", "password")

final = ({'url':r.html_url , 'name': r.name} for r in g.get_user().get_starred())
pd.DataFrame(final).to_excel('Github Stars 20160101.xlsx')