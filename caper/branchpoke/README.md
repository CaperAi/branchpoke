# Branch Poke

Poke developers to remind them to clean up their open
branches. This tool sends a message to anyone who was
the last one to commit into a branch if the commit
was created a long time ago or if the branch has has
been "merged".

# Configuration

- `BRANCHPOKE_SLACK_TOKEN` or `--slack_token`: API token to connect to Slack App.
- `BRANCHPOKE_MESSAGING_EMAIL_SUFFIXES` or `--messaging_email_suffixes`: Suffixes of emails to allow. If set, will only send emails that end with one of the strings in this list. Comma separated list.
- `BRANCHPOKE_GITLAB_BASE_URL` or `--gitlab_base_url`: URL of your gitlab instance.
- `BRANCHPOKE_GITLAB_TOKEN` or `--gitlab_token`: API token for gitlab.
- `BRANCHPOKE_GITLAB_GROUP` or `--gitlab_group`: If set, only list projects from this group.
- `BRANCHPOKE_BRANCH_AGE_MAX_SECONDS` or `--branch_age_max_seconds`: Number of seconds after which a branch is considered "old".



