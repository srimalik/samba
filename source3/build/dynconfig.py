import string, Utils

# list of directory options to offer in configure
dir_options = {
    'with-piddir'                         : [ '${PREFIX}/var/locks', 'where to put pid files' ],
    'with-privatedir'                     : [ '${PREFIX}/private', 'Where to put sam.ldb and other private files' ],
    'with-winbindd-socket-dir'            : [ '${PREFIX}/var/lib/winbindd', 'winbind socket directory' ],
    'with-winbindd-privileged-socket-dir' : [ '${PREFIX}/var/lib/winbindd_privileged', 'winbind privileged socket directory'],
    'with-ntp-signd-socket-dir'           : [ '${PREFIX}/var/run/ntp_signd', 'NTP signed directory'],
    'with-lockdir'                        : [ '${PREFIX}/var/locks', 'where to put lock files' ],
    'with-codepagedir'                    : [ '${PREFIX}/lib/samba', 'where to put codepages' ],
    'with-privatedir'                     : [ '${PREFIX}/private', 'where to put smbpasswd' ],
    'with-cachedir'                       : [ '${PREFIX}/var/locks', 'where to put temporary cache files' ],
    'with-logfilebase'                    : [ '${PREFIX}/var/log/samba', 'Where to put log files' ],
    'with-configdir'                      : [ '${PREFIX}/etc/samba', 'Where to put configuration files' ],
    'with-swatdir'                        : [ '${PREFIX}/swat', 'Where to put SWAT files' ],
    'with-statedir'                       : [ '${PREFIX}/var/locks', 'where to put persistent state files' ],
    'with-cachedir'                       : [ '${PREFIX}/var/locks', 'where to put temporary cache files' ],
    'with-ncalrpcdir'                     : [ '${PREFIX}/var/ncalrpc', 'where to put ncalrpc sockets' ],
    'with-pammodulesdir'                  : [ '', 'Which directory to use for PAM modules' ],
    'with-codepagedir'                    : [ '${PREFIX}/lib/samba', 'Where to put codepages' ],
    'with-selftest-prefix'                : [ '', 'The prefix where make test will be run' ],
    'with-selftest-shrdir'                : [ '', 'The share directory that make test will be run against' ]
    }

# list of cflags to use for dynconfig.c
dyn_cflags = {
    'CONFIGFILE'                     : '${SYSCONFDIR}/smb.conf',
    'BINDIR'                         : '${BINDIR}',
    'SBINDIR'                        : '${SBINDIR}',
    'LIBDIR'                         : '${LIBDIR}',
    'STATEDIR'                       : '${LOCALSTATEDIR}',
    'LMHOSTSFILE'                    : '${SYSCONFDIR}/lmhosts',
    'LOCKDIR'                        : '${LOCALSTATEDIR}/locks',
    'PIDDIR'                         : '${LOCALSTATEDIR}/run',
    'DATADIR'                        : '${DATADIR}',
    'LOGFILEBASE'                    : '${LOCALSTATEDIR}',
    'CONFIGDIR'                      : '${SYSCONFDIR}',
    'NCALRPCDIR'                     : '${LOCALSTATEDIR}/ncalrpc',
    'SWATDIR'                        : '${PREFIX}/swat',
    'PRIVATE_DIR'                    : '${PRIVATEDIR}',
    'MODULESDIR'                     : '${PREFIX}/modules',
    'SETUPDIR'                       : '${DATADIR}/setup',
    'WINBINDD_PRIVILEGED_SOCKET_DIR' : '${WINBINDD_PRIVILEGED_SOCKET_DIR}',
    'WINBINDD_SOCKET_DIR'            : '${WINBINDD_SOCKET_DIR}',
    'NTP_SIGND_SOCKET_DIR'           : '${NTP_SIGND_SOCKET_DIR}',
    'CODEPAGEDIR'                    : '${CODEPAGEDIR}',
    'CACHEDIR'                       : '${CACHEDIR}',
    'SMB_PASSWD_FILE'                : '${PRIVATEDIR}/smbpasswd',
    }

def get_varname(v):
    '''work out a variable name from a configure option name'''
    if v.startswith('with-'):
        v = v[5:]
    v = v.upper()
    v = string.replace(v, '-', '_')
    return v


def dynconfig_cflags(bld):
    '''work out the extra CFLAGS for dynconfig.c'''
    cflags = []
    for f in dyn_cflags.keys():
        # substitute twice, as we could have substitutions containing variables
        v = Utils.subst_vars(dyn_cflags[f], bld.env)
        v = Utils.subst_vars(v, bld.env)
        bld.ASSERT(v != '', "Empty dynconfig value for %s" % f)
        bld.ASSERT(v.find('${') == -1, "Unsubstituted variable in %s : %s : %s" % (f, dyn_cflags[f], v))
        cflags.append('-D%s="%s"' % (f, v))
    return cflags