import os
import requests
import json

class NullException(ValueError):
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}

t = os.environ.get('t')
headers = {"User-Agent": "shitbox",
           "Authorization": "token " + t}


def get_url_for_lang(lang):
    if lang == "Rust":
        return "https://api.github.com/search/issues?q=is:issue+label:E-easy"

def get_json(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError

def get_data_for_issue(issue_array=[]):
    data_obj = {}
    if len(issue_array) == 0:
        raise NullException("There are no Issue to report")
    else:
        for issue in issue_array:
            data_obj[issue] = {}
            data = get_json(issue)
            data_obj[issue]["repo"] = data["html_url"]
            data_obj[issue]["title"] = data["title"]
    return data_obj

def  get_github_issues(language, issue_array=[]):
    url = get_url_for_lang(language)
    try:
        data = get_json(url)
    except ConnectionError:
        return(None)

    items = data["items"]
    for item in items:
        issue_array.append(item["url"])
    try:
        obj = get_data_for_issue(issue_array)
        #print(obj)
        return(obj)
    except NullException as e:
        print(e.strerror)
        return(None)
    except ConnectionError:
        return(None)

def write_to_file(filename):
    obj = get_github_issues("Rust")
    with open(filename,"w") as f:
        json.dump(obj, f)
        f.close()

if __name__ == "__main__":
    write_to_file("foo.txt")
