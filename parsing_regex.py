from analysis.dev import DELIM


# hash is 40 characters long, git hash is 9 characters and file extension limited to 4 characters
# index line as not delimited by tabs but by more than one space (tab plus some other spaces)

GO_ETHEREUM_REGEX_DICT = {
    # note these filename regex look for .file_ext so have problems with files like /.travis.yml
    'commit_reg': DELIM.join([r'([a-f0-9]{40})', '([a-f0-9]{9})', '([a-f0-9]{40})']),
    'stats_reg': r'(\d{1,10})\s+(\d{1,10})\s+([a-zA-Z/]+\.\w{1,4})',
    'index_reg': r'index ([a-f0-9]{7,9})(\.{2})([a-f0-9]{7,9})\s([0-9]{5,7})',
    'new_index_reg': r'index [a-f0-9]{7,9}\.{2}[a-f0-9]{7,9}',
    'start_diff_reg': r'diff --git a/([\w/]+\.\w{1,4})\s+b/([\w/]+\.\w{1,4})|diff --git a/\.([\w/]+\.\w{1,4})\s+b/\.([\w/]+\.\w{1,4})',
    'location_reg': r'@@ -([0-9]+),([0-9]+)\s\+([0-9]+),([0-9]+)\s@@\s*(.*)',
    'filename_reg': r'--- a/([\w/]+\.\w{1,4})|\+\+\+ b/([\w/]+\.\w{1,4})',
    'devnull_file_reg': r'--- /dev/null|\+\+\+ /dev/null',
    'diff_line_reg': r'- (.+)|\+ (.+)|(.+)'
}

# git sha1 hash is 32 characters, git hash is 7 characters long and file extensions can be 1-6 char long
JS_IPFS_REGEX_DICT = {
    'commit_reg': DELIM.join([r'([a-f0-9]{32})', '([a-f0-9]{7})', '([a-f0-9]{32})']),
    'stats_reg': r'(\d{1,10})\s+(\d{1,10})\s+([a-zA-Z/]+\.\w{1,6})',
    'index_reg': r'index ([a-f0-9]{7,9})(\.{2})([a-f0-9]{7,9})\s([0-9]{5,7})',
    'new_index_reg': r'index [a-f0-9]{7,9}\.{2}[a-f0-9]{7,9}',
    'start_diff_reg': r'diff --git a/(.+\.\w{1,6}})\b\s+\bb/(.+\.\w{1,6}})',
    'location_reg': r'@@ -([0-9]+),([0-9]+)\s\+([0-9]+),([0-9]+)\s@@\s*(.*)',
    'filename_reg': r'--- a/(.+\.\w{1,6}})|\+\+\+ b/(.+\.\w{1,6}})',
    'devnull_file_reg': r'--- /dev/null|\+\+\+ /dev/null',
    'diff_line_reg': r'- (.+)|\+ (.+)|(.+)'
}
