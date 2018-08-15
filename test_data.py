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

TEST_GOETH_2018 = {
    'sha1': '6d1e292eefa70b5cb76cd03ff61fc6c4550d7c36',
    'author_email': 'janos@users.noreply.github.com',
    'subject': 'Manifest cli fix and upload defaultpath only once (#17375)',
    'commit_body': '* cmd/swarm: fix manifest subcommands and add tests',
    # check length of diffs_list = diff_objs_list = 10
    'diffs': [{
        'filename_old': 'cmd/swarm/main.go',
        'filename_new': 'cmd/swarm/main.go',
        'filetype': '100644',
        'locations_changed':  [('322', '23', '322', '23')],
        'functions_changed':['Downloads a swarm bzz uri to the given dir. When no dir is provided, working dir'],
        'num_changes': 1,
        'is_rename': False,
        'is_new': False,
        'is_deletion': False
        },
            {
                'filename_old': 'swarm/api/manifest.go',
                'filename_new': 'swarm/api/manifest.go',
                'filetype': '100644',
                'locations_changed':  [('106', '13', '106', '18')],
                'functions_changed':  [
                    'func (a *API) NewManifestWriter(ctx context.Context, addr storage.Address, quitC'],
                'num_changes': 1,
                'is_rename': False,
                'is_new': False,
                'is_deletion': False
        },
        {
            'filename_old': 'swarm/api/api.go',
            'filename_new': 'swarm/api/api.go',
            'filetype': '100644',
            'locations_changed': [('704', '11', '704', '12'), ('737', '6', '738', '25')],
            'functions_changed': [
                'func (a *API) AddFile(ctx context.Context, mhash, path, fname string, content []',
                'func (a *API) UploadTar(ctx context.Context, bodyReader io.ReadCloser, manifestP'
            ],
            'num_changes': 2,
            'is_rename': False,
            'is_new': False,
            'is_deletion': False
        },
    ]
}

TEST_GOETH_2017 = {
    'sha1': '8f35e3086cbea24839c5435b1cebe85a438b42d3',
    'author_email': 'mmeister@suse.de',
    'subject': 'cmd/geth: fix geth attach --datadir=... (#15517)',
    'commit_body': '',
    # check length of diffs_list = diff_objs_list = 1
    'diffs': [{
        'filename_old': 'cmd/geth/consolecmd.go',
        'filename_new': 'cmd/geth/consolecmd.go',
        'filetype': '100644',
        'locations_changed':  [('17', '6', '17', '7'), ('112', '7', '113', '11')],
        'functions_changed': [None, 'func localConsole(ctx *cli.Context) error {'],
        'num_changes': 2,
        'is_rename': False,
        'is_new': False,
        'is_deletion': False
        }]
}

TEST_GOETH_2016 = {
    'sha1': '64af2aafdaf16d0bab4c2b89573324b076602bab',
    'author_email': 'geffobscura@gmail.com',
    'subject': 'core, core/vm: added gas price variance table',
    'commit_body': 'This implements 1b & 1c of EIP150 by adding a new GasTable which must be',
    # check length of diffs_list = diff_objs_list = 19
    'diffs': [{
        'filename_old': '/dev/null',
        'filename_new': 'params/gas_table.go',
        'filetype': '',
        'locations_changed':  [('0', '0', '1', '65')],
        'functions_changed': [None],
        'num_changes': 1,
        'is_rename': False,
        'is_new': True,
        'is_deletion': False
        }]
}
