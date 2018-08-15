import os
import json

from analysis.dev import DATA_DIR, LOCAL_DB, LOCAL_DB_GOETH
from analysis.helpers import serialize_from_dict, connect_to_db

from analysis.create_database import create_repo, insert_commit


def create_jsipfs_repo(session):
    jsipfs_repo = {
        'full_name': 'ipfs/js-ipfs',
        'github_repo_id': 20312497,
        'owner': 'ipfs',
        'github_owner_id': 10536621}

    return create_repo(session, jsipfs_repo)


def create_goether_repo(session):
    goeth_repo = {
        'full_name': "ethereum/go-ethereum",
        'github_repo_id': 15452919,
        'owner': 'ethereum',
        'github_owner_id': 6250754}
    return create_repo(session, goeth_repo)


def fill_jsipfs_db(saving_to_fname):
    with open(os.path.join(DATA_DIR, saving_to_fname), 'r') as f:
        c2 = json.load(f)

    session, engine = connect_to_db(LOCAL_DB)
    commit_vals = list(map(serialize_from_dict, c2))
    repo = create_jsipfs_repo(session)
    return list(map(lambda x: insert_commit(session, x, repo), commit_vals))


def fill_goether_db(saving_to_fname):
    with open(os.path.join(DATA_DIR, saving_to_fname), 'r') as f:
        c2 = json.load(f)

    session, engine = connect_to_db(LOCAL_DB_GOETH)
    commit_vals = list(map(serialize_from_dict, c2))
    repo = create_goether_repo(session)
    return list(map(lambda x: insert_commit(session, x, repo), commit_vals))