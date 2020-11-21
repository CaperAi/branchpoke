from collections import defaultdict
from datetime import timedelta, datetime, timezone
from typing import DefaultDict, Set

from caper.branchpoke.config import Config
from caper.branchpoke.messaging import MessagingService
from caper.branchpoke.version_control import Branch, VersionControlService, User, Project

GroupedIssues = DefaultDict[User, DefaultDict[Project, Set[Branch]]]


class Poker:
    def __init__(
            self,
            config: Config,
            version_control_service: VersionControlService,
            messaging_service: MessagingService,
    ):
        self.branch_age_max = timedelta(seconds=config.branch_age_max_seconds)
        self.version_control = version_control_service
        self.messaging = messaging_service

    def branch_is_old(self, branch: Branch):
        return (datetime.now(timezone.utc) - branch.created) > self.branch_age_max

    def branches(self):
        for project in self.version_control.projects():
            for branch in self.version_control.branches(project):
                yield project, branch

    def send_pokes(self):
        merged: GroupedIssues = defaultdict(lambda: defaultdict(set))
        stale: GroupedIssues = defaultdict(lambda: defaultdict(set))

        for project, branch in self.branches():
            author = branch.author

            # We're never going to message them, so ignore them.
            if not self.messaging.should_contact(author.email):
                continue

            if branch.protected:
                # This is a magic branch that we want to keep around. For example a "release-xxx" branch.
                continue

            if self.branch_is_old(branch):
                stale[author][project].add(branch)

            if branch.merged:
                merged[author][project].add(branch)

        for user, projects in merged.items():
            self.messaging.notify_branch_already_merged(user, projects)

        for user, projects in stale.items():
            self.messaging.notify_branch_stale(user, projects)
