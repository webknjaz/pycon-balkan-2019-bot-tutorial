import logging

from octomachinery.app.server.runner import run as run_app
from octomachinery.app.routing import process_event_actions
from octomachinery.app.routing.decorators import process_webhook_payload
from octomachinery.app.runtime.context import RUNTIME_CONTEXT


logger = logging.getLogger(__name__)


@process_event_actions('pull_request', {'closed'})
@process_webhook_payload
async def on_issue_opened(
        *,
        action, number, pull_request,
        repository, organization,
        sender, installation,
):
    """Whenever an issue is opened, greet the author and say thanks."""
    github_api = RUNTIME_CONTEXT.app_installation_client

    if not pull_request['merged']:
        # interrupt early
        logger.info(f'PR #{number} just got closed but not merged')
        return

    logger.info(f'PR #{number} just got merged')

    comments_api_url = pull_request["comments_url"]
    author = pull_request["user"]["login"]
    message = (
        f"Thanks for the PR @{author}! "
    )
    await github_api.post(
        comments_api_url, data={
            "body": message,
        }
    )


@process_event_actions('issues', {'opened'})
@process_webhook_payload
async def on_issue_opened(
        *,
        action, issue, repository, sender, installation,
        assignee=None, changes=None,
):
    """Whenever an issue is opened, greet the author and say thanks."""
    github_api = RUNTIME_CONTEXT.app_installation_client
    comments_api_url = issue["comments_url"]
    author = issue["user"]["login"]
    message = (
        f"Thanks for the report @{author}! "
        "I will look into it ASAP! (I'm a bot 🤖)."
    )
    await github_api.post(
        comments_api_url, data={
            "body": message,
        }
    )


if __name__ == "__main__":
    run_app(
        name='PyCon-Bot-by-webknjaz',
        version='1.0.0',
        url='https://github.com/apps/pyyyyyycoooon-booooot111',
    )
