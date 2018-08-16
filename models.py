from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DATE, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import UniqueConstraint

from sqlalchemy import MetaData

from sqlalchemy.dialects.postgresql import JSON

from analysis.helpers import connect_to_db
# from helpers import connect_to_db
from analysis.dev import LOCAL_DB, LOCAL_DB_GOETH
# from dev import LOCAL_DB_GOETH

# note when running this to create the database, can't run from top level directory
# instead, need to run python models.py in the analysis/ directory and also need to change the paths from analysis.dev to dev


Base = declarative_base()


class Repo(Base):
    __tablename__ = 'repos'

    id = Column(Integer, primary_key=True)
    # this should be the github fullname
    full_name = Column(String)
    github_repo_id = Column(Integer)
    owner = Column(String)
    github_owner_id = Column(Integer)

    UniqueConstraint('github_repo_id')

    def __repr__(self):
        return "<Repo(repo name='{fname}', gh_id={gh_id})>".format(fname=self.full_name, gh_id=self.github_repo_id)


class Commit(Base):
    __tablename__ = 'commits'

    id = Column(Integer, primary_key=True, unique=True)
    sha1 = Column(String, nullable=True, unique=True)
    git_hash = Column(String)
    repo_id = Column(Integer, ForeignKey('repos.id'))

    subject = Column(Text)
    timestamp = Column(TIMESTAMP)
    date_time = Column(DATE)

    commit_body = Column(Text)
    raw_text = Column(Text)

    author_id = Column(Integer, ForeignKey('developers.id'), nullable=True)
    commiter_id = Column(Integer, ForeignKey('developers.id'), nullable=True)

    repo = relationship('Repo', backref='commits')

    def __repr__(self):
        return '<Commit({h}: {subject})>'.format(h=self.git_hash, subject=self.subject)

    @hybrid_property
    def additions(self):
        return sum(d.additions for d in self.diffs)

    @hybrid_property
    def deletions(self):
        return sum(d.deletions for d in self.diffs)

    @hybrid_property
    def files_changed(self):
        return list(d.filename_new for d in self.diffs)


class Developer(Base):
    __tablename__ = 'developers'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    username = Column(String, nullable=True)
    affiliation = Column(Text, nullable=True)
    UniqueConstraint('email', 'name')

    authored_commits = relationship('Commit', backref='author', foreign_keys='Commit.author_id')
    commiter_commits = relationship('Commit', backref='commiter', foreign_keys='Commit.commiter_id')

    def __repr__(self):
        return "<Developer({name}-{email})>".format(name=self.name, email=self.email)


class Diff(Base):
    __tablename__ = 'diffs'

    id = Column(Integer, primary_key=True, unique=True)
    filename_old = Column(Text)
    filename_new = Column(Text)
    filetype = Column(String)

    is_rename = Column(Boolean)
    is_new = Column(Boolean)
    is_deletion = Column(Boolean)
    raw_diff = Column(Text, nullable=True)
    additions = Column(Integer)
    deletions = Column(Integer)

    commit_id = Column(Integer, ForeignKey('commits.id'))
    commit = relationship('Commit', backref='diffs')

    def __repr__(self):
        return '<Diff({fname})>'.format(fname=self.filename_new)


class Change(Base):
    __tablename__ = 'changes'

    id = Column(Integer, primary_key=True, unique=True)
    function_changed = Column(Text)
    location_changed = Column(JSON)

    raw_changes = Column(Text)

    additions = Column(Integer)
    deletions = Column(Integer)

    diff_id = Column(Integer, ForeignKey('diffs.id'))
    diff = relationship('Diff', backref='changes')

    def __repr__(self):
        return '<Change({fname})>'.format(fname=self.function_changed)


# create database and turn on logging
if __name__ == '__main__':

    session, engine = connect_to_db(LOCAL_DB_GOETH)
    meta = MetaData()
    # drop all tables from database - note this is not something to run if not creating
    meta.drop_all(engine)

    # create database schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)