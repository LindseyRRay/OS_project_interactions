from analysis.dev import DATA_DIR, GIT_LOG_FORMAT, DELIM
from analysis.parsing_regex import JS_IPFS_REGEX_DICT, GO_ETHEREUM_REGEX_DICT
from analysis.test_parselog import run_loc_test, count_png_errors, check_test_dict
from analysis.test_data import TEST_COM10, TEST_COM1000, TEST_GOETH_2016, TEST_GOETH_2017, TEST_GOETH_2018
from analysis.helpers import serialize_to_dict
from analysis.objects import Commit, Commit_info, Statistic, FileChange
MAX_STATS_LEN = 10
MAX_FILE_EXT_LEN = 3
# for js-ipfs, this value should be 6 MAX_FILE_EXT_LEN = 6
# for go-etherem, hashes are 40 long and git id hash abbrev is 9
# for jsipfs the sha1 hash is 32 long and the git id is 7 long
    # search will look for match over the entire string, match will onlyu look for matches starting at the beginning
             branch=None, file_extensions=None):
    also file extensions should be of the form '\"*.go\"'  with the double quotes of they won't work as well
    for example ' "*.go" "*.md" '

    if file_extensions is not None:
        git_log.append(file_extensions)
    return ' '.join(git_log)
def process_lines(line, regex_dict):
        if not isinstance(line, str):
            line = line.decode('utf-8')
        print('Unicode error ', e)
    if is_commit(line, regex_dict['commit_reg']):
        print('IS COMMIT')
        if is_stats(line, regex_dict['stats_reg']):
            print('IS STAT')
            return ('statistic', make_stats(line, regex_dict['stats_reg']))
def yield_gitlog_lines(repo_path, **kwargs):
    command = make_cmd(**kwargs)
    print('command ', command)
    # shell = True indicates you are passing a string
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=repo_path, shell=True)
        try:
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
        except Exception as e:
            print(item_name)
            print(item_obj)
def is_commit(line, commit_reg):
    # js-ipfs commit_reg = r'[a-f0-9]{32}' + delim + '[a-f0-9]{7}' + delim + '[a-f0-9]{32}'
    # go-ether commit_reg = r'[a-f0-9]{40}' + delim + '[a-f0-9]{9}' + delim + '[a-f0-9]{40}'

    return is_match(commit_reg, line)


def make_commit(line):
    #     commit_line = re.sub(r'----',' ', commit_line.decode('utf-8'))
    comm_args = line.split(DELIM)
    comm_args.append(line)
    commit = Commit_info(*comm_args)
    parents = fix_parents(commit.parents)
    return commit._replace(parents=parents)


def is_stats(line, stats_reg):
    # note that commit spacing isnt exactly a tab, it is greater than that so need to have the multiple spaces
    #stats_reg = r'(\d{1,{}'.format(MAX_STATS_LEN)+'})(\s+)(\d{1,{}'.format(
    #    MAX_STATS_LEN)+ '(\s+)([a-zA-Z/]+)(\.)(\w{1,{}'.format(MAX_FILE_EXT_LEN)})'
    return is_match(stats_reg, line)


def make_stats(line, stats_reg):
    # NOTE THAT YOU CANNOT HAVE VARS IN REGEX STR
    # this needs to match regex
    g = re.match(stats_reg, line)
    return Statistic(*g.groups())


def make_diff(line):
    return line


def is_blank(line):
    return bool(line is None or line is '')


def is_index(line, index_reg, new_index_reg):

    m = is_match(index_reg, line)
    return is_match(new_index_reg, line)
def parse_filetype(line, index_reg):
    m = re.search(index_reg, line)
        return m.groups()[-1]
def check_start_diff(line, start_diff_reg):
    return is_match(start_diff_reg, line)
def parse_filename(line, start_diff_reg):
    m = re.search(start_diff_reg, line)
    names = list(filter(None, m.groups()))
def is_location_filename_info(line, location_reg):
    return is_match(location_reg, line)
def parse_location_filename_info(line, location_reg):
    m = re.search(location_reg, line)
def is_filenames_changed(line, filename_reg, devnull_file_reg):
    filenames = is_match(filename_reg, line)
    new = is_match(devnull_file_reg, line)
def get_filenames_changed(line, filename_reg, devnull_file_reg):
    new_file_reg, old_file_reg = devnull_file_reg.split('|')
    m = re.search(new_file_reg, line)
    if m is not None:
    m = re.search(old_file_reg, line)
    if m is not None:
        print(m.groups())
    m = re.search(filename_reg, line)
def is_raw_diff(line, diff_line_reg):
    return is_match(diff_line_reg, line)
def parse_diff_text(lst_diff_lines, regex_dict):
        start = check_start_diff(line, regex_dict['start_diff_reg'])
            curr_file = parse_filename(line, regex_dict['start_diff_reg'])
        elif is_index(line, regex_dict['index_reg'], regex_dict['new_index_reg']):
            change_dict['filetype'] = parse_filetype(line, regex_dict['index_reg'])
        elif is_filenames_changed(line, regex_dict['filename_reg'], regex_dict['devnull_file_reg']):
            l = get_filenames_changed(line, regex_dict['filename_reg'], regex_dict['devnull_file_reg'])
        elif is_location_filename_info(line, regex_dict['location_reg']):
            loc_info, funcname = parse_location_filename_info(line, regex_dict['location_reg'])
        elif is_raw_diff(line, regex_dict['diff_line_reg']):
def gen_parse_log(repo_path, regex_dict, **kwargs):
    # need the list to force execution
    cs = map(lambda x: process_lines(x, regex_dict), yield_gitlog_lines(repo_path, **kwargs))
        try:
            diff_objs = parse_diff_text(com.diffs_list, regex_dict)
            com.diff_objs_list = diff_objs
        except AttributeError as e:
            print(e)
            print(com.__dict__)
def gen_save_commitlog_jsipfs(repo_path, saving_to_fname, **kwargs):
    commits = gen_parse_log(repo_path, JS_IPFS_REGEX_DICT, **kwargs)
    for test_dict in [TEST_COM1000, TEST_COM10]:
        to_test = list(filter(lambda x: x.commit_info.sha1 == test_dict['sha1'], commits))[0]
        check_test_dict(to_test, test_dict)

    coms = list(map(serialize_to_dict, commits))

    print('Saving to ', os.path.join(DATA_DIR, saving_to_fname))
    with open(os.path.join(DATA_DIR, saving_to_fname), 'w') as f:
        json.dump(coms, f)


def gen_save_commitlog_goethereum(repo_path, saving_to_fname, **kwargs):
    commits = gen_parse_log(repo_path, GO_ETHEREUM_REGEX_DICT, **kwargs)
    errors = run_loc_test(commits)
    count_png_errors(errors)
    # select commit - want to make these tests go ethereum specific
    for test_dict in [TEST_GOETH_2017, TEST_GOETH_2018, TEST_GOETH_2016]:
        to_test = list(filter(lambda x: x.commit_info.sha1 == test_dict['sha1'], commits))[0]
        check_test_dict(to_test, test_dict)
        json.dump(coms, f)
    return commits, errors