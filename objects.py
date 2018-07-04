import collections


Commit_info = collections.namedtuple(
    'commit_info', ['sha1', 'git_hash', 'parents',
                    'author_email', 'author_name', 'subject', 'timestamp', 'date_time',
                    'commiter_email', 'commiter_name', 'commit_body', 'raw_text'])

Statistic = collections.namedtuple('statistic', ['additions', 'deletions', 'filename'])


FileChange = collections.namedtuple('filechange',
                                    ['filename_old', 'filename_new', 'raw_diff',
                                     'filetype', 'index_info', 'functions_changed',
                                     'locations_changed',
                                     'list_changes', 'num_changes', 'is_rename', 'is_new', 'is_deletion'])


class Commit(object):

    def __init__(self, commit_info):
        self.commit_info = commit_info
        self.statistics_list = []
        self.diffs_list = []
        self.diff_objs_list = []

