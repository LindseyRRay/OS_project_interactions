import json
import os
import subprocess
import re
import funcy


from dev import DATA_DIR, DELIM, JSIPFS_REPO_PATH, JSIPFS_START, JS_IPFS_PARSED_COMMITS_FILENAME, GIT_LOG_FORMAT

from test_parselog import run_loc_test, count_png_errors, check_test_dict
from test_data import TEST_COM10, TEST_COM1000
from helpers import serialize_to_dict


from objects import Commit, Commit_info, Statistic, FileChange
# this is max characters at the end of a regex
MAX_EXTENSION = 10


def is_match(reg, line):
    m = re.search(reg, line)
    return bool(m is not None)


def as_list(elements):
    items = [e for e in elements if e]
    return items or None


def fix_parents(parents_string):
    return as_list(parents_string.split())


def fix_refs(refs_string):
    return as_list(refs_string.strip()[1:-1].split(', '))


def is_commit(line, delim=DELIM):
    commit_reg = r'[a-f0-9]{32}' + delim + '[a-f0-9]{7}' + delim + '[a-f0-9]{32}'
    return is_match(commit_reg, line)


def make_commit(line):
    #     commit_line = re.sub(r'----',' ', commit_line.decode('utf-8'))
    comm_args = line.split(DELIM)
    comm_args.append(line)
    commit = Commit_info(*comm_args)
    parents = fix_parents(commit.parents)
    return commit._replace(parents=parents)


def is_stats(line):
    stats_reg = r'\d{1,MAX_EXTENSION}}\t\d{1,MAX_EXTENSION}}\t.+\.\w{1,6}'
    return is_match(stats_reg, line)


def make_stats(line):
    return Statistic(*line.split('\t'))


def make_diff(line):
    return line


def is_blank(line):
    return bool(line is None or line is '')


def make_cmd(git_log_format=GIT_LOG_FORMAT, start=None, end=None, no_renames=False, no_merges=False, show_diff=True,
             branch=None):
    '''
    start and end dates should be in YYYY-MM-DD str format
    '''
    git_log = ['git', 'log', '--all', '--numstat', '--format=format:{0}'.format(git_log_format)]
    if start is not None:
        git_log.append('--since')
        git_log.append(start)
    if end is not None:
        git_log.append('--until')
        git_log.append(end)
    if no_renames:
        git_log.append('--no-renames')
    if no_merges:
        git_log.append('--no-merges')
    if show_diff:
        git_log.append('--patch')
    if branch is not None:
        git_log.append(str(branch))
    return git_log


def process_lines(line):
    # most of the unicode decode errors/stats error caused by config files
    try:
        line = line.decode('utf-8')
    except UnicodeDecodeError as e:
        print('Unicode error')
        print(line)
        return ('error', line)
    # turn bytes object into a string
    if is_blank(line):
        return (None, None)
    if is_commit(line):
        return ('commit', make_commit(line))
    try:
        if is_stats(line):
            return ('statistic', make_stats(line))
    except TypeError:
        print(line)
        return ('error', line)
        # if not stat or not a commit line, must be blank or a diff
    return ('diff', make_diff(line))


def yield_commits(repo_path, **kwargs):
    proc = subprocess.Popen(make_cmd(**kwargs), stdout=subprocess.PIPE, cwd=repo_path)
    for line in proc.stdout:
        yield line.strip()


# for processing text with diffs, I need to group commit, statistics and patch together in one group identified by the hash
# and report back
# I need some type of iterator that goes throuhgh line by line

def process_list_git_objs(lst):
    '''
    Input is a list of git commit_info objects, Commit_info or Staticts Or Diffs
    The goal is to group all the stats and diffs to one commit object
    list should be a list of tuples (string_identifier, object)
    I also need to work on not keeping track of config or boilerplat files, because these tend to mess up the parser
    '''
    errors = []
    commit_objs = []
    curr_commit = None
    for item_name, item_obj in lst:
        if item_name == 'commit':
            # append old curr commit
            if curr_commit is not None:
                commit_objs.append(curr_commit)
            # create a new commit obj to add to
            curr_commit = Commit(item_obj)
        elif item_name == 'error':
            errors.append(item_obj)
        elif item_name == 'statistic':
            curr_commit.statistics_list.append(item_obj)
        elif item_name == 'diff':
            curr_commit.diffs_list.append(item_obj)
        elif item_name is None:
            # this is a blank line
            continue
    # after loop, append last commit object and return list of obj
    commit_objs.append(curr_commit)
    return commit_objs, errors


def is_index(line):
    '''Check for an Index line like: 'index 582ba6e..0cd52f1 100644'
    '''
    i_reg = r'index [a-f0-9]{7}\.{2}[a-f0-9]{7}\s([0-9]{5,7})'
    m = is_match(i_reg, line)
    if m:
        return True
    # for new files different index syntax
    i_reg = r'index [a-f0-9]{7}\.{2}[a-f0-9]{7}'
    return is_match(i_reg, line)


def parse_filetype(line):
    i_reg = r'index [a-f0-9]{7}\.{2}[a-f0-9]{7}\s([0-9]{5,7})'
    m = re.search(i_reg, line)
    if m:
        return m.groups()[0]
    # try new file match - no file type
    return None


def check_start_diff(line):
    '''
    Check for the start of a file changed in the diff output
    '''
    d_reg = r'diff --git a/(.+\.\w{1,MAX_EXTENSION}})\b\s+\bb/(.+\.\w{1,MAX_EXTENSION}})'
    return is_match(d_reg, line)


def parse_filename(line):
    '''
    Parse Filename changed from start of the diff
    '''
    d_reg = r'diff --git a/(.+\.\w{1,MAX_EXTENSION}})\b\s+\bb/(.+\.\w{1,MAX_EXTENSION}})'
    m = re.search(d_reg, line)
    names = m.groups()
    # note the filenames should be identical except in the case of a rename
    return names[1]


def is_location_filename_info(line):
    '''
    The format is the @@ from-file-range to-file-range @@ [header].
     The from-file-range is in the form -<start line>,<number of lines>,
     and to-file-range is +<start line>,<number of lines>.
     Both start-line and number-of-lines refer to position and length of hunk in preimage and postimage, respectively.
     If number-of-lines not shown it means that it is 0.
     Sample: '@@ -15,27 +15,33 @@ module.exports = function libp2p (self) {'
    '''
    l_reg = r'@@ -([0-9]+),([0-9]+)\s\+([0-9]+),([0-9]+)\s@@\s*(.*)'
    return is_match(l_reg, line)


def parse_location_filename_info(line):
    '''Pull out location of code change and function name if available'''
    l_reg = r'@@ -([0-9]+),([0-9]+)\s\+([0-9]+),([0-9]+)\s@@\s*(.*)'
    m = re.search(l_reg, line)
    g = m.groups()
    # this should be start, num changed to file is startline, num-lines
    if len(g[-1]) > 0 and re.match(r'\D+', g[-1]) is not None:
        return g[:-1], g[-1]
    return g[:-1], None


def is_filenames_changed(line):
    '''
    Check for preimage and post image filenames
    Samples:
    '--- a/src/core/components/libp2p.js',
    '+++ b/src/core/components/libp2p.js'
    Note that new files will have /dev/null as the old filename
    '''
    l_reg = r'--- a/(.+\.\w{1,MAX_EXTENSION}})|\+\+\+ b/(.+\.\w{1,MAX_EXTENSION}})'
    filenames = is_match(l_reg, line)
    if filenames:
        return True
    l_reg = r'--- /dev/null|\+\+\+ /dev/null'
    new = is_match(l_reg, line)
    return new


def get_filenames_changed(line):
    '''
    Extract Filename
    Samples:
    '--- a/src/core/components/libp2p.js',
    '+++ b/src/core/components/libp2p.js'
    '''
    # first check for filenames of newly created files
    l_reg = r'--- /dev/null'
    m = re.search(l_reg, line)
    if m:
        return '/dev/null', None
    l_reg = r'\+\+\+ /dev/null'
    m = re.search(l_reg, line)
    if m:
        return None, '/dev/null'
    l_reg = r'--- a/(.+\.\w{1,MAX_EXTENSION})|\+\+\+ b/(.+\.\w{1,MAX_EXTENSION}})'
    m = re.search(l_reg, line)
    g = m.groups()
    return g


def is_raw_diff(line):
    l_reg = r'- (.+)|\+ (.+)|(.+)'
    return is_match(l_reg, line)


def is_rename(line):
    '''renames start with a special function under the function name
     'similarity index 68%',
     'rename from src/core/namesys/index.js',
     'rename to src/core/ipns/index.js'
     '''
    return (line.startswith('similarity index') or line.startswith('rename '))


def is_deletion(line):
    '''
    Deletions start with 'deleted file'
    '''
    return (line.startswith('deleted file'))


def is_new_file(line):
    '''
    Create files have a special line 'new file mode
    '''
    return (line.startswith('new file mode'))


def make_file_obj(change_dict, last_change_text):
    '''wrapper to make FileChange Obj'''
    if len(last_change_text) > 0:
        change_dict['list_changes'].append(last_change_text)
    return FileChange(**change_dict)


def create_file_obj_dict(namedtup):
    # create fields with all the info we are saving from the diff text
    change_dict = dict(zip(namedtup.__dict__['_fields'], funcy.repeat(None)))
    change_dict['raw_diff'] = []
    change_dict['filename_old'] = ''
    change_dict['filename_new'] = ''
    change_dict['functions_changed'] = []
    change_dict['locations_changed'] = []
    change_dict['list_changes'] = []
    change_dict['num_changes'] = 0
    change_dict['is_rename'] = False
    change_dict['is_new'] = False
    change_dict['is_deletion'] = False

    return change_dict


def parse_diff_text(lst_diff_lines):
    '''
    Parse the Output of the diff into a list of changes by line and code changed
    One diff text is made up of multiple file changes
    Each file changed is noted by a line as follows:
    'diff --git a/src/core/components/libp2p.js b/src/core/components/libp2p.js'
    "git diff" header in the form diff --git a/file1 b/file2.
    the --git indicates the diff is in git form
    The a/ and b/ filenames are the same unless rename/copy is involved (which we have excluded)
    Next lines is an index line:
    'index 582ba6e..0cd52f1 100644'
    100644 means that it is ordinary file and not e.g. symlink, and that it doesn't have executable permission bit),
    The index bit indicates a  shortened hash of preimage (the version of file before given change) and postimage
    (the version of file after change)
    The next two lines:
     '--- a/src/core/components/libp2p.js',
     '+++ b/src/core/components/libp2p.js'
    are the source (preimage) and destination (postimage) file names.
    If file was created the source is /dev/null; if file was deleted, the target is /dev/null
    The next lines shows where the changes occured and name of function where it occurred
    '@@ -15,27 +15,33 @@ module.exports = function libp2p (self) {'
     The format is the @@ from-file-range to-file-range @@ [header].
     The from-file-range is in the form -<start line>,<number of lines>,
     and to-file-range is +<start line>,<number of lines>.
     Both start-line and number-of-lines refer to position and length of hunk in preimage and postimage, respectively.
     If number-of-lines not shown it means that it is 0.

     Note that one diff can have multiple location change lines, each with a text diff below

     Next comes the description of where files differ.
     The lines common to both files begin with a space character.
     The lines that actually differ between the two files have one of the following indicator
     characters in the left print column:

    '+' -- A line was added here to the first file.
    '-' -- A line was removed here from the first file.
    https://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
    '''
    change_objs = []

    curr_file = None
    change_dict = create_file_obj_dict(FileChange)
    curr_changes = []

    for line in lst_diff_lines:

        start = check_start_diff(line)
        if is_blank(line):
            continue

        elif start:
            # check if curr_obj is none, if not append to list of change objects
            if curr_file is not None:
                # decide how to make objc
                curr_obj = make_file_obj(change_dict, curr_changes)
                change_objs.append(curr_obj)
            curr_file = parse_filename(line)
            change_dict = create_file_obj_dict(FileChange)
            curr_changes = []
            change_dict['raw_diff'].append(line)

        elif is_index(line):
            change_dict['filetype'] = parse_filetype(line)
            change_dict['raw_diff'].append(line)

        elif is_rename(line):
            # rename diffs have a segment of text
            change_dict['is_rename'] = True
            change_dict['raw_diff'].append(line)

        elif is_new_file(line):
            # newly created files have a line indicating that new file mode
            change_dict['is_new'] = True
            change_dict['raw_diff'].append(line)

        elif is_deletion(line):
            # newly created files have a line indicating that new file mode
            change_dict['is_deletion'] = True
            change_dict['raw_diff'].append(line)

        elif is_filenames_changed(line):
            # keep track of files that changed
            l = get_filenames_changed(line)
            # if a filename is in the first group, it is the old filename
            # if it is in the second position, it is the new filename
            change_dict['raw_diff'].append(line)
            if l[0] is None:
                change_dict['filename_new'] = l[1]
            elif l[1] is None:
                change_dict['filename_old'] = l[0]
            else:
                print('Error in filename parsing ', l, line)

        elif is_location_filename_info(line):
            # in this, we need to add function name changed to list, add location changed to list
            # and then start a new change text block to append the raw text to
            change_dict['raw_diff'].append(line)
            loc_info, funcname = parse_location_filename_info(line)
            change_dict['locations_changed'].append(loc_info)
            change_dict['functions_changed'].append(funcname)
            # increment number of changes
            change_dict['num_changes'] += 1
            # create a new block of text for list changes and append
            if len(curr_changes) > 0:
                change_dict['list_changes'].append(curr_changes)
            curr_changes = []

        elif is_raw_diff(line):
            # get last entry in change dict and append line
            curr_changes.append(line)
            change_dict['raw_diff'].append(line)

        else:
            print('LINE NOT CAPTURED ', line)

    # add last created object to list of current objects and return
    curr_obj = make_file_obj(change_dict, curr_changes)
    change_objs.append(curr_obj)
    return change_objs


def gen_parse_log(repo_path, **kwargs):
    cs = map(process_lines, yield_commits(repo_path, **kwargs))
    commits, errors = process_list_git_objs(cs)
    for com in commits:
        diff_objs = parse_diff_text(com.diffs_list)
        com.diff_objs_list = diff_objs
    return commits


def gen_save_commitlog(repo_path, saving_to_fname, **kwargs):
    commits = gen_parse_log(repo_path, **kwargs)
    errors = run_loc_test(commits)
    count_png_errors(errors)
    # select commit
    to_test = list(filter(lambda x: x.commit_info.sha1 == TEST_COM10['sha1'], commits))[0]
    check_test_dict(to_test, TEST_COM10)

    to_test = list(filter(lambda x: x.commit_info.sha1 == TEST_COM1000['sha1'], commits))[0]
    check_test_dict(to_test, TEST_COM1000)

    coms = list(map(serialize_to_dict, commits))

    print('Saving to ', os.path.join(DATA_DIR, saving_to_fname))
    with open(os.path.join(DATA_DIR, saving_to_fname), 'w') as f:
        json.dump(coms, f)