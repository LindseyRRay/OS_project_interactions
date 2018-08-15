import funcy
import re


def test_len_changes_matches(comm_obj):
    # for each FileChange object assert the number of location changes matches number of changes per file
    error_dict = {
        'mismatched_location': [],
        'count_mismatch': []
    }
    errors = False
    for fchange in comm_obj.diff_objs_list:
        if len(fchange.locations_changed) != len(fchange.list_changes):
            print(fchange.list_changes)
            print(fchange.locations_changed)
            errors = True
            error_dict['mismatched_location'].append(fchange)
        if len(fchange.locations_changed) != fchange.num_changes or len(fchange.list_changes) != fchange.num_changes:
            print('NUM CHANGES ERROR')
            print(fchange.num_changes)
            print(fchange.locations_changed)
            print(len(fchange.locations_changed))
            print(fchange.list_changes)
            print(len(fchange.list_changes))
            errors = True
            error_dict['count_mismatch'].append(fchange)
    return errors, error_dict


def run_loc_test(list_commits):
    res = map(test_len_changes_matches, list_commits)
    errors = list(filter(lambda x: x[0] is True, res))
    print('Number of errors: ', len(errors))
    return list(map(funcy.second, errors))


def count_png_errors(errors):
    count_errors = 0
    for e in errors:
        for diff in e['mismatched_location']:
            # if first line of raw diff contains a png file, continue
            if re.match(r'diff --git a/[\w/]  +\.png', diff.raw_diff[0]):
                continue
            else:
                print('NOT PNG FILE ', diff.raw_diff[0]),
                count_errors += 1
    return count_errors


def check_test_dict(commit_obj, test_dict):
    diff_checks = (
    'filetype', 'locations_changed', 'functions_changed', 'num_changes', 'is_rename', 'is_new', 'is_deletion')
    for k, v in test_dict.items():
        if k != 'diffs':
            print('testing ', k, ': ', v, ' value is ', getattr(commit_obj.commit_info, k))
            assert getattr(commit_obj.commit_info, k) == v
    # now check the diffs info
    commit_diffs = commit_obj.diff_objs_list
    match_filenames = lambda x: x.filename_old == test_diff['filename_old'] and x.filename_new == test_diff[
        'filename_new']

    for test_diff in test_dict['diffs']:
        # select diff
        print(test_diff)
        print(commit_diffs)
        c_diff = list(filter(match_filenames, commit_diffs))
        print(c_diff)
        assert len(c_diff) == 1
        # check values in test diff
        to_test = c_diff[0]
        for v in diff_checks:
            test_val = getattr(to_test, v)
            check_val = test_diff[v]
            print('Checking Diff ', v, ' check ', check_val, ' test val ', test_val)
            assert test_val == check_val

