from argparse import ArgumentParser

from caper.branchpoke.config import Config
from caper.branchpoke.gl import GitlabVersionControlService
from caper.branchpoke.messaging import MessagingServiceMultiplex
from caper.branchpoke.poke import Poker
from caper.branchpoke.sl import SlackMessagingService

parser = ArgumentParser()
parser.add_argument('--messaging_email_suffixes')
parser.add_argument('--slack_token')
parser.add_argument('--gitlab_base_url')
parser.add_argument('--gitlab_group')
parser.add_argument('--gitlab_token')
parser.add_argument('--branch_age_max_seconds')
args = parser.parse_args()

config = Config(args)
poker = Poker(
    config,
    version_control_service=GitlabVersionControlService(config),
    messaging_service=MessagingServiceMultiplex(
        config,
        [
            SlackMessagingService(config)
        ]
    )
)
poker.send_pokes()
