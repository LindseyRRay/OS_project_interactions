import argparse
import datetime


from gitlog_parser import gen_save_commitlog
from fill_db import fill_db


# sample command for jsipfs python analysis/log_fill_db.py '/Users/Lraymond/Python/gitkit_research/js-ipfs'

if __name__ == '__main__':
    str_date = datetime.datetime.now().strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser(description='generate git log for repo and fill database')
    parser.add_argument('repo_path', type=str,
                        help='repo path for the repo')
    parser.add_argument('--fname', type=str, help='file name to save commits')
    parser.add_argument('--start', default='2013-01-01',
                        help='start of analysis period')
    parser.add_argument('--end', default=str_date, help='end date')

    args = parser.parse_args()

    print('args ', args)
    if args.fname is None:
        fname = '{}_parsed_commits.json'.format(args.repo_path.split('/')[-1])
    else:
        fname = args.fname


    print('Generating and saving commit log to ', fname)
    gen_save_commitlog(args.repo_path, fname, start=args.start, end=args.end)
    print('Filling Database')
    fill_db(fname)



