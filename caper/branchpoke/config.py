from argparse import Namespace
from functools import partial
from os import environ
from typing import Optional


def setting(name: str, cast=None, default=None, args: Optional[Namespace] = None):
    key = 'BRANCHPOKE_' + name.strip().upper()
    if args is not None and name in args and args.__getattribute__(name) is not None:
        value = args.__getattribute__(name)
    elif key in environ:
        value = environ[key]
    elif default is not None:
        value = default
    else:
        raise Exception("Setting not found")

    if cast is list:
        return value.split(',')

    return value if cast is None else cast(value)


class Config:
    gitlab_base_url: str
    gitlab_token: str
    gitlab_group: str

    branch_age_max_seconds: int

    def __init__(self, args: Namespace):
        s = partial(setting, args=args)

        # TODO: self.messaging_backend = s('messaging_backend', default='print')
        self.email_suffixes = s('messaging_email_suffixes', cast=list, default='')

        self.slack_token = s('slack_token', default='')

        # TODO: self.vcs_backend = s('vcs_backend', default='gitlab')

        self.gitlab_base_url = s('gitlab_base_url', default='https://gitlab.com/api/v4')
        self.gitlab_token = s('gitlab_token')
        self.gitlab_group = s('gitlab_group', default='')

        self.branch_age_max_seconds = s('branch_age_max_seconds', cast=int, default=(86400 * 100))
