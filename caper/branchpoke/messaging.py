import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Set

from caper.branchpoke.config import Config
from caper.branchpoke.version_control import Project, Branch, User


class MessagingService(ABC):
    def __init__(self, config: Config):
        self.email_suffixes = [
            suffix.strip().lower()
            for suffix in config.email_suffixes
        ]

    def should_contact(self, email: str) -> bool:
        email = email.strip().lower()
        for suffix in self.email_suffixes:
            if email.endswith(suffix):
                return True
        return False

    @abstractmethod
    def notify_branch_stale(self, user: User, projects: Dict[Project, Set[Branch]]):
        ...

    @abstractmethod
    def notify_branch_already_merged(self, user: User, projects: Dict[Project, Set[Branch]]):
        ...


class MessagingServiceMultiplex(MessagingService):
    def __init__(self, config: Config, services: List[MessagingService]):
        super().__init__(config)
        self.messaging_services: List[MessagingService] = services

    def notify_branch_stale(self, user: User, projects: Dict[Project, Set[Branch]]):
        for service in self.messaging_services:
            service.notify_branch_stale(user, projects)

    def notify_branch_already_merged(self, user: User, projects: Dict[Project, Set[Branch]]):
        for service in self.messaging_services:
            service.notify_branch_already_merged(user, projects)


class LoggingMessagingService(MessagingService):
    def notify_branch_stale(self, user: User, projects: Dict[Project, Set[Branch]]):
        for project, branches in projects.items():
            for branch in branches:
                logging.warning(f"[BRANCH OLD   ]; project: {project.name}, branch: {branch.name}")

    def notify_branch_already_merged(self, user: User, projects: Dict[Project, Set[Branch]]):
        for project, branches in projects.items():
            for branch in branches:
                logging.warning(f"[BRANCH MERGED]; project: {project.name}, branch: {branch.name}")
