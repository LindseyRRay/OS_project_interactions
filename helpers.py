from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from objects import Commit_info, Statistic, FileChange, Commit


def serialize_from_dict(commit_dict):
    comm_info = Commit_info(**commit_dict['commit_info'])
    stats = list(Statistic(**stat_dict) for stat_dict in commit_dict['statistics_list'])
    'diff_objs_list'
    diff_obj_list = list(FileChange(**fchange_dict) for fchange_dict in commit_dict['diff_objs_list'])
    c = Commit(commit_info=comm_info)
    c.statistics_list = stats
    c.diff_objs_list = diff_obj_list
    c.diffs_list = commit_dict['diffs_list']
    return c


def serialize_to_dict(commit_obj):
    ## turn into a dict so you can dump it to json
    d = dict()
    d['commit_info'] = commit_obj.commit_info._asdict()
    d['diffs_list'] = commit_obj.diffs_list
    # also need to serialize the Statistics objects and filechange objects
    d['statistics_list'] = [x._asdict() for x in commit_obj.statistics_list]
    d['diff_objs_list'] = [x._asdict() for x in commit_obj.diff_objs_list]
    return d


def connect_to_db(db_str):
    engine = create_engine(db_str)
    Session = sessionmaker(bind=engine)
    return Session(), engine
