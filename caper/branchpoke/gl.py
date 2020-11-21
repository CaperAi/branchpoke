from datetime import datetime
from typing import Generator

from gitlab import Gitlab
from gitlab.v4.objects import ProjectBranch as GitlabBranch

from caper.branchpoke.config import Config
from caper.branchpoke.version_control import VersionControlService, Project, Branch, User


class GitlabVersionControlService(VersionControlService):
    def __init__(self, config: Config):
        self.client = Gitlab(url=config.gitlab_base_url, private_token=config.gitlab_token)
        self.group = config.gitlab_group

    def projects(self) -> Generator[Project, None, None]:
        if self.group:
            base = self.client.groups.get(self.group)
        else:
            base = self.client

        for gitlab_project in base.projects.list(as_list=False):
            yield Project(
                id=str(gitlab_project.get_id()),
                name=gitlab_project.path_with_namespace,
                url=gitlab_project.web_url
            )

    def branchpoke_branch(self, gitlab_branch: GitlabBranch) -> Branch:
        head = gitlab_branch.commit

        author = User(
            id=head['committer_email'],
            email=head['committer_email'],
        )

        return Branch(
            id=gitlab_branch.get_id(),
            name=gitlab_branch.name,
            url=gitlab_branch.web_url,
            author=author,
            protected=gitlab_branch.protected,
            merged=gitlab_branch.merged,
            created=datetime.fromisoformat(head['committed_date'])
        )

    def branches(self, project: Project) -> Generator[Branch, None, None]:
        gitlab_project = self.client.projects.get(project.id)
        for gitlab_branch in gitlab_project.branches.list(as_list=False):
            yield self.branchpoke_branch(gitlab_branch)
