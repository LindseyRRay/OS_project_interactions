from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import funcy
from datetime import datetime

from analysis.dev import DELIM, RAW_DIFF_DELIM

from analysis.models import Repo, Commit, Diff, Developer, Change


def get_one_or_create(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound as e:
        return model(**kwargs), False
    except MultipleResultsFound as e:
        print('Error Multiple Results Found ', kwargs)
        return session.query(model).filter_by(**kwargs).first(), False


def create_commit(session, commit_info_dict):
    keys = ('sha1', 'git_hash', 'subject', 'timestamp', 'date_time', 'commit_body', 'raw_text')
    comm_dict = funcy.select_keys(lambda x: x in keys, commit_info_dict)
    comm_dict['date_time'] = datetime.strptime(comm_dict['date_time'], '%Y-%m-%d %H:%M:%S %z')
    comm_dict['timestamp'] = datetime.fromtimestamp(int(comm_dict['timestamp']))
    # check if a commit already exists with same hash
    c, exists = get_one_or_create(session, Commit, git_hash=comm_dict['git_hash'])
    if exists:
        print('Commit obj already exists', comm_dict['git_hash'])
    else:
        c, created = get_one_or_create(session, Commit, **comm_dict)
    return c


def create_repo(session, repo_info_dict):
    keys = ('full_name', 'github_repo_id', 'owner')
    r_dict = funcy.select_keys(lambda x: x in keys, repo_info_dict)
    c, exists = get_one_or_create(session, Repo, github_repo_id=r_dict['github_repo_id'])
    if exists:
        print('Repo already exists', r_dict['github_repo_id'])
    else:
        c, created = get_one_or_create(session, Repo, **r_dict)
    return c


def create_developer(session, develop_dict):
    keys = ('name','email', 'username', 'affiliation')
    r_dict = funcy.select_keys(lambda x: x in keys, develop_dict)
    c, exists = get_one_or_create(session, Developer, email=develop_dict['email'])
    if exists:
        print('Developer already exists ', develop_dict['email'])
    else:
        c, created = get_one_or_create(session, Developer, **develop_dict)
    return c


def create_diff(session, d_dict):
    keys = (
        'filename_old','filename_new', 'filetype', 'is_rename', 'is_new', 'is_deletion',
    'raw_diff', 'additions', 'deletions')
    r_dict = funcy.select_keys(lambda x: x in keys, d_dict)
    c, exists = get_one_or_create(session, Diff, **r_dict)
    if exists:
        print('Diff already exists', r_dict)
    return c


def create_change(session, c_dict):
    keys = (
        'function_changed','location_changed', 'raw_changes', 'additions', 'deletions')
    r_dict = funcy.select_keys(lambda x: x in keys, c_dict)
    c, exists = get_one_or_create(session, Change , raw_changes=r_dict['raw_changes'])
    if exists:
        print('Change already exists', r_dict)
    else:
        # if call get or create, json will error
        c = Change(**r_dict)
    return c


def try_exc_wrapper(value, delim=DELIM):
    try:
        #if iterable, turn it into a string, if not, just return
        return delim.join(value)
    except TypeError:
        str(value)


def location_to_dict(location_tup):
    return {'old_start': location_tup[0],
            'old_end': location_tup[1],
            'new_start': location_tup[2],
            'new_end': location_tup[3]}


def insert_commit(session, commit_obj, repo_obj):
    '''
    Process for inserting information into the database is as follows:
    create if necessary repo
    create commit
    assign repo to commit
    create/fetch author developer and commit developer - commit between these two to avoid dups
    assign author commiter relations to commit - session.commit()
    for each diff associated with a commit, create/fetch the diff, add statistics to it, session commit
    for each change assocaited with a diff, create it and assign to the diff
    then session.commit
    repeat process for all changes associated with a diff and all diffs associated with a commit
    '''
    comm = create_commit(session, commit_obj.commit_info._asdict())
    session.add(comm)
    session.commit()
    d_dict = {'name': commit_obj.commit_info.author_name,
              'email': commit_obj.commit_info.author_email}
    author = create_developer(session, d_dict)
    session.add(author)
    session.commit()
    c_dict = {'name': commit_obj.commit_info.commiter_name,
              'email': commit_obj.commit_info.commiter_email}
    commiter = create_developer(session, c_dict)
    session.add(commiter)
    session.commit()
    comm.author = author
    comm.commiter = commiter
    comm.repo = repo_obj
    session.commit()

    # add the diffs
    statistics = commit_obj.statistics_list

    for diff_obj in commit_obj.diff_objs_list:
        diff_dict = diff_obj._asdict()
        stat = funcy.first(filter(lambda x: x.filename == diff_obj.filename_new, statistics))
        if stat:
            diff_dict['additions'] = stat.additions
            diff_dict['deletions'] = stat.deletions
        diff_dict['raw_diff'] = try_exc_wrapper(
            diff_dict['raw_diff'], delim=RAW_DIFF_DELIM)
        d = create_diff(session, diff_dict)
        session.add(d)
        session.commit()
        d.commit = comm
        for i in range(diff_obj.num_changes):
            c_dict = {'function_changed': diff_obj.functions_changed[i],
                      'location_changed': location_to_dict(diff_obj.locations_changed[i]),
                      'raw_changes': try_exc_wrapper(
                          diff_obj.list_changes[i], delim=RAW_DIFF_DELIM)
                      }
            change = create_change(session, c_dict)
            session.add(change)
            session.commit()
            change.diff = d
    session.commit()
    return comm
