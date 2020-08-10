import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
resposne = requests.get(url, timeout=(20, 10))
print('Status code:', resposne.status_code)

response_dict = resposne.json()

repo_dicts = response_dict['items']

names, stars, description, plot_dicts = [], [], [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])
    description.append(repo_dict['description'])
    plot_dict = {'value': repo_dict['stargazers_count'], 'label': str(repo_dict['description'])}
    plot_dicts.append(plot_dict)

style = LS('#333366', base_style=LCS)

config = pygal.Config()
config.x_label_rotation = 45
config.show_legend = False
config.title_font_size = 24
config.label_font_size = 12
config.major_label_font_size = 18
config.truncate_label = 15
config.width = 1000

chart = pygal.Bar(style=style, config=config)
chart._title = 'Most-Starred Python Projects on Github'
chart.x_labels = names
# chart.add('Stars', stars, label=description)
chart.add('Stars', plot_dicts)
chart.render_to_file('python_repos.svg')
