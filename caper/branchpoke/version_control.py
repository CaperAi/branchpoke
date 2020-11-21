from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import NamedTuple, Generator


class User(NamedTuple):
    id: str
    email: str


class Project(NamedTuple):
    id: str
    name: str
    url: str


class Branch(NamedTuple):
    id: str
    name: str
    url: str
    author: User
    protected: bool
    merged: bool
    created: datetime

    @property
    def age(self):
        return datetime.now(timezone.utc) - self.created


class VersionControlService(ABC):
    @abstractmethod
    def projects(self) -> Generator[Project, None, None]:
        ...

    @abstractmethod
    def branches(self, project: Project) -> Generator[Branch, None, None]:
        ...
