TEST_COM10 = {
    'sha1': 'a1b9b93c8eb9f0b4820dc6b19358668501110eb9',
    'author_email': 'jonathankrone@gmail.com',
    'subject': 'revert: internalKey recording',
    'commit_body': '',
    # check length of diffs_list = diff_objs_list = 3
    'diffs': [{
        'filename_old': 'src/core/components/pin-set.js',
        'filename_new': 'src/core/components/pin-set.js',
        'filetype': '100644',
        'locations_changed': [('95', '26', '95', '23'), ('186', '7', '183', '6'),
         ('202', '26', '198', '25'), ('237', '7', '232', '6'), ('245', '7', '239', '7')],
        'functions_changed': ['exports = module.exports = function (dag) {',
             'exports = module.exports = function (dag) {',
             'exports = module.exports = function (dag) {',
             'exports = module.exports = function (dag) {',
             'exports = module.exports = function (dag) {'],
        'num_changes': 5,
        'is_rename': False,
        'is_new': False,
        'is_deletion': False
        },
    ]
}



TEST_COM1000 = {
    'sha1': '28b7215adb4ab40ba40f2f88fe65f9297e3fcb16',
    'author_email': 'daviddias.p@gmail.com',
    'subject': 'make jsipfs id to print out valid json',
    'commit_body': '',
    # check length of diffs_list = diff_objs_list = 3
    'diffs': [{
        'filename_old': 'src/cli/commands/id.js',
        'filename_new': 'src/cli/commands/id.js',
        'filetype': '100644',
        'locations_changed': [('26', '7', '26', '7')],
        'functions_changed': ['module.exports = Command.extend({'],
        'num_changes': 1,
        'is_rename': False,
        'is_new': False,
        'is_deletion': False
        },
        {
        'filename_old': 'test/cli/test-id.js',
        'filename_new': 'test/cli/test-id.js',
        'filetype': '100644',
        'locations_changed': [('18', '12', '18', '16'), ('54', '14', '58', '21')],
        'functions_changed': ["describe('id', () => {", "describe('id', () => {"],
        'num_changes': 2,
        'is_rename': False,
        'is_new': False,
        'is_deletion': False
        },
    ]
}