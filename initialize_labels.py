import json
import requests
from getpass import getpass

ISSUE_LABELS = {'category:issue': '5319e7',
                'category:pull': 'd4c5f9',
                'priority:low': 'dddddd',
                'priority:normal': 'fa9300',
                'priority:high': 'f0423d',
                'type:bug': 'f0423d',
                'type:enhancement': 'fa9300',
                'type:feature': '55ac55',
                'type:invalid': 'dddddd',
                'type:question': '548ca8',
                }


class GitHubIssue(object):

    def __init__(self, username, password, repository, organization=None):
        self.username = username
        self.password = password
        self.repository = repository
        self.organization_name = organization
        self.repo_username = self.organization_name if self.organization_name else self.username
        self.headers = {'content-type': 'application/json'}

    def get_and_delete(self):
        labels = self._get_labels()
        if labels:
            for label in labels:
                self._delete_label(label['name'])
        else:
            print "No existing labels"

    def create_new_label(self, name, color):
        payload = {'name': name, 'color': color}
        url = "https://api.github.com/repos/%s/%s/labels" % (self.repo_username, self.repository)
        r = requests.post(url, headers=self.headers, data=json.dumps(payload), auth=(self.username, self.password))
        if r.status_code == 201:
            print "New Label %s Created" % name

    def _get_labels(self):
        url = "https://api.github.com/repos/%s/%s/labels" % (self.repo_username, self.repository)
        r = requests.get(url, headers=self.headers, auth=(self.username, self.password))
        if r.status_code == 200:
            return r.json()
        return None

    def _delete_label(self, name):
        url = "https://api.github.com/repos/%s/%s/labels/%s" % (self.repo_username, self.repository, name)
        r = requests.delete(url, headers=self.headers, auth=(self.username, self.password))
        if r.status_code == 204:
            print "Deleted label %s from %s" % (name, self.repository)


username = raw_input("GitHub Username: ")
password = getpass("GitHub Password: ")
organization = raw_input("GitHub Organization (If indicated, grab from organization repo instead. You can leave this blank): ")
repository = raw_input("GitHub Repo name: ")


issue = GitHubIssue(username, password, repository, organization)
issue.get_and_delete()
for label, color in ISSUE_LABELS.items():
    issue.create_new_label(label, color)
