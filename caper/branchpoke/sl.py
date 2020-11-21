import logging
from functools import lru_cache
from typing import Optional, Dict, Set

from slack import WebClient
from slack.errors import SlackApiError

from caper.branchpoke.config import Config
from caper.branchpoke.messaging import MessagingService
from caper.branchpoke.version_control import Project, Branch, User


class SlackMessagingService(MessagingService):
    def __init__(self, config: Config):
        super().__init__(config)
        self.client = WebClient(token=config.slack_token)

    @lru_cache(maxsize=512, typed=True)
    def slack_user(self, user: User) -> Optional[str]:
        try:
            response = self.client.users_lookupByEmail(email=user.email)
        except SlackApiError as e:
            logging.error(f"Failed to lookup email '{user.email}' because: {e.response['error']}")
            return None
        return response['user']['id']

    def send(self, user: User, message: str):

        if not self.should_contact(user.email):
            return

        slack_user_id = self.slack_user(user)

        if slack_user_id is None:
            logging.warning("Lookup of user failed, ignoring.")
            return

        logging.info(f"Sending message to {user.email} (slack={slack_user_id})")
        self.client.chat_postMessage(
            channel=slack_user_id,
            # text='',
            as_user=True,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        )

    @staticmethod
    def link(thing):
        return f'<{thing.url}|{thing.name}>'

    @staticmethod
    def __is_too_long(message: str) -> bool:
        """
        Slack only lets you send messages 3001 characters long.
        :param message: A message we want to send via slack.
        :return: True if the message is too long to be sent over slack.
        """
        return len(message) > 2000

    def notify_branch_stale(self, user: User, projects: Dict[Project, Set[Branch]]):
        message = f"You have some open branches that are becoming stale:\n\n"
        for project, branches in projects.items():
            message += f'• {self.link(project)}\n'
            for branch in branches:
                if self.__is_too_long(message):
                    break
                message += f'    - {self.link(branch)}: {branch.age.days}d\n'
        self.send(user, message)

    def notify_branch_already_merged(self, user: User, projects: Dict[Project, Set[Branch]]):
        message = f"You have some open branches that have already been merged:\n\n"
        for project, branches in projects.items():
            message += f'- {self.link(project)}\n'
            for branch in branches:
                if self.__is_too_long(message):
                    break
                message += f'    • {self.link(branch)}\n'
        self.send(user, message)
