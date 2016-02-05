# code for this partially borrowed from tjcsl/cslbot
import git
import json
import requests
import plugins
from ghinfo import *
from links import *
from control import *
from urllib.parse import quote as sanitize

def _initialise():
    plugins.register_admin_command(['pull', 'issue', 'commit'])
    plugins.register_user_command(['gh' , 'source'])

# helpers

def postissue(event, url, args):
    if str(args[0]).isdigit():
        try:
            i = getissue(int(args[0]))
            msg = _('{} ({}) State: {}<br>{}').format(i["title"], i["number"], i["state"], i["link"])
        except:
            msg = _('Invalid Issue Number')
    elif str(args[0]) == '--search':
        query = sanitize(' '.join(args[1:]))
        s = search(query)
        msg = _('Total Results: {}<br>First Result: {} ({})<br>State: {}<br>{}').format(s['total'], s['title'], s['number'], s['state'], s['link'])
    else:
        session = requests.Session()
        session.auth=(USERNAME, PASSWORD)
        # Create our issue
        text = ' '.join(args).split(' -d ')
        if len(text) == 2:
            desc = text[1]
            title = text[0]
        else:
            desc = "No description provided."
            title = text[0]
        issue = {'title': title,
                 'body': 'Issue created by {}. \n {}'.format(event.user.full_name, desc)}
        # Add the issue to our repository
        r = session.post(url, json.dumps(issue))
        get = requests.get(url)
        data = json.loads(get.text)
        link = shorten(str(data[0][u'html_url']))
        if r.status_code == 201:
            msg = _('Successfully created issue: {}').format(link)
        else:
            msg = _('Could not create issue.<br>Response: {}').format(r.content)
    return msg
    
def getsource():
    url = 'https://github.com/2019okulkarn/sodabot'
    short = shorten(url)
    title = get_title(url)
    msg = _('** {} ** - {}').format(title, short)
    return msg

def getopenissue(num, url):
    get = requests.get(url)
    data = json.loads(get.text)
    num = int(num) * -1
    link = shorten(str(data[num][u'html_url']))
    title = str(data[num][u'title'])
    number = str(data[num][u'number'])
    return {"title": title,
            "link": link,
            "number": number}

def getissue(num):
    issuesurl = 'https://api.github.com/repos/{}/{}/issues/{}'.format(REPO_OWNER, REPO_NAME, num)
    get = requests.get(issuesurl)
    data = json.loads(get.text)
    link = shorten(str(data[u'html_url']))
    number = str(data[u'number'])
    state = str(data[u'state'])
    title = str(data[u'title'])
    return {"title": title,
            "link": link,
            "number": number,
            "state": state}
def search(term):
    searchurl = 'https://api.github.com/search/issues?q=user:{}+repo:{}+{}'.format(REPO_OWNER, REPO_NAME, term)
    g = requests.get(searchurl)
    data = json.loads(g.text)
    first = data[u'items'][0]
    total = str(data[u'total_count'])
    link = shorten(str(first[u'html_url']))
    title = first[u'title']
    number = first[u'number']
    state = first[u'state']
    return {"title": title,
            "link": link,
            "number": number,
            "state": state,
            "total": total}

# begin commands
def gh(bot, event, *args):
    '''Retrieves link to source code of bot. Format is /bot gh'''
    msg = getsource()
    yield from bot.coro_send_message(event.conv, msg)

def source(bot, event, *args):
    try:
        '''Retrieves link to source code of bot. Format is /bot source [command]'''
        if len(args) == 1:
            url = 'https://github.com/2019okulkarn/sodabot/tree/master/hangupsbot/plugins/' + args[0] + '.py'
            link = shorten(url)
            title = get_title(url)
            msg = _('** {} ** - {}').format(title, link)
        else:
            msg = getsource()
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        simple = _('Oops! An Error Occurred')
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
    
# admin only commands
def pull(bot, event, *args):
    try:
        g = git.cmd.Git(git_dir)
        status = g.pull()
        msg = _('{}').format(status)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)
        
def commit(bot, event, *args):
    '''Get the latest commit on bot repo'''
    try:
        url = 'https://api.github.com/repos/{}/{}/git/refs/heads/master'.format(REPO_OWNER, REPO_NAME)
        get = requests.get(url)
        data = json.loads(get.text)
        commiturl = data[u'object'][u'url']
        getcommit = requests.get(commiturl)
        commitdata = json.loads(getcommit.text)
        link = shorten(str(commitdata[u'html_url']))
        committer = str(commitdata[u'committer'][u'name'])
        date = str(commitdata[u'committer'][u'date'])
        message = str(commitdata[u'message'])
        msg = _('The last commit was "{}" by {} at {}<br>{}').format(message, committer, date, link)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(e, event.text)
        simple = _('An Error Occurred. Please Try Again Later')
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)

def issue(bot, event, *args):
    '''Create an issue on github.com using the given parameters.'''
    url = 'https://api.github.com/repos/{}/{}/issues'.format(REPO_OWNER, REPO_NAME)
    try:
        if args:
            msg = postissue(event, url, args)
        else:
            i = getopenissue(0, url)
            msg = _('{} ({}) -- {}').format(i["title"], i["number"], i["link"])
        if not CONTROL == str(event.conv_id):
            yield from bot.coro_send_message(CONTROL, msg)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)
