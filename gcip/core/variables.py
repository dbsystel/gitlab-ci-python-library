import os
from typing import Any, Optional


# In Python >= 3.9 it is also possible to use @classmethods and @property
# together, so that there are no parantheses necessarry.
# See https://stackoverflow.com/questions/128573/using-property-on-classmethods´
class EnvProxy():
    def __init__(self, key: str, always_available: bool = True) -> None:
        self.key = key
        self.always_available = always_available

    def __get__(self, obj: Any, objtype: Any = None) -> Optional[str]:
        if self.always_available:
            return os.environ[self.key]
        else:
            return os.getenv(self.key)


class PredefinedVariables():
    """
    Gitlab CI predefined variables.
    https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
    """

    CHAT_CHANNEL: str = EnvProxy("CHAT_CHANNEL")
    """
    Source chat channel which triggered the ChatOps command.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CHAT_INPUT: str = EnvProxy("CHAT_INPUT")
    """
    Additional arguments passed in the ChatOps command.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI: str = EnvProxy("CI")
    """
    Mark that job is executed in CI environment.

    Added in GitLab all
    Available in GitLab Runner 0.4

    Raises:
        KeyError: If environment variable not available.
    """

    CI_API_V4_URL: str = EnvProxy("CI_API_V4_URL")
    """
    The GitLab API v4 root URL.

    Added in GitLab 11.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_BUILDS_DIR: str = EnvProxy("CI_BUILDS_DIR")
    """
    Top-level directory where builds are executed.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_BEFORE_SHA: str = EnvProxy("CI_COMMIT_BEFORE_SHA")
    """
    The previous latest commit present on a branch. Is always
    0000000000000000000000000000000000000000 in pipelines for merge requests.

    Added in GitLab 11.2
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_DESCRIPTION: str = EnvProxy("CI_COMMIT_DESCRIPTION")
    """
    The description of the commit the message without first line,
    if the title is shorter than 100 characters; full message in other case.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    """

    CI_COMMIT_MESSAGE: str = EnvProxy("CI_COMMIT_MESSAGE")
    """
    The full commit message.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_NAME: str = EnvProxy("CI_COMMIT_REF_NAME")
    """
    The branch or tag name for which project is built.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_PROTECTED: str = EnvProxy("CI_COMMIT_REF_PROTECTED")
    """
    true if the job is running on a protected reference, false if not.

    Added in GitLab 11.11
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_SLUG: str = EnvProxy("CI_COMMIT_REF_SLUG")
    """
    $CI_COMMIT_REF_NAME in lowercase, shortened to 63 bytes,
    and with everything except 0-9 and a-z replaced with -.
    No leading / trailing -. Use in URLs, host names and domain names.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_SHA: str = EnvProxy("CI_COMMIT_SHA")
    """
    The commit revision for which project is built.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_SHORT_SHA: str = EnvProxy("CI_COMMIT_SHORT_SHA")
    """
    The first eight characters of CI_COMMIT_SHA.

    Added in GitLab 11.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_BRANCH: Optional[str] = EnvProxy("CI_COMMIT_BRANCH", always_available=False)
    """
    The commit branch name. Present in branch pipelines,
    including pipelines for the default branch.
    Not present in merge request pipelines or tag pipelines.

    Added in GitLab 12.6
    Available in GitLab Runner 0.5
    """

    CI_COMMIT_TAG: Optional[str] = EnvProxy("CI_COMMIT_TAG", always_available=False)
    """
    The commit tag name. Present only when building tags.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5
    """

    CI_COMMIT_TITLE: str = EnvProxy("CI_COMMIT_TITLE")
    """
    The title of the commit - the full first line of the message.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_TIMESTAMP: str = EnvProxy("CI_COMMIT_TIMESTAMP")
    """
    The timestamp of the commit in the ISO 8601 format.

    Added in GitLab 13.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONCURRENT_ID: str = EnvProxy("CI_CONCURRENT_ID")
    """
    Unique ID of build execution in a single executor.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONCURRENT_PROJECT_ID: str = EnvProxy("CI_CONCURRENT_PROJECT_ID")
    """
    Unique ID of build execution in a single executor and project.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONFIG_PATH: str = EnvProxy("CI_CONFIG_PATH")
    """
    The path to CI configuration file. Defaults to .gitlab-ci.yml.

    Added in GitLab 9.4
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEBUG_TRACE: str = EnvProxy("CI_DEBUG_TRACE")
    """
    Whether debug logging (tracing) is enabled.

    Added in GitLab all
    Available in GitLab Runner 1.7

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEFAULT_BRANCH: str = EnvProxy("CI_DEFAULT_BRANCH")
    """
    The name of the default branch for the project.

    Added in GitLab 12.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX: str = EnvProxy("CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX")
    """
    The image prefix for pulling images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_SERVER: str = EnvProxy("CI_DEPENDENCY_PROXY_SERVER")
    """
    The server for logging in to the Dependency Proxy. This is equivalent to $CI_SERVER_HOST:$CI_SERVER_PORT.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_PASSWORD: str = EnvProxy("CI_DEPENDENCY_PROXY_PASSWORD")
    """
    The password to use to pull images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_USER: str = EnvProxy("CI_DEPENDENCY_PROXY_USER")
    """
    The username to use to pull images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPLOY_FREEZE: Optional[str] = EnvProxy("CI_DEPLOY_FREEZE", always_available=False)
    """
    Included with the value true if the pipeline runs during a deploy freeze window.

    Added in GitLab 13.2
    Available in GitLab Runner all
    """

    CI_DEPLOY_PASSWORD: str = EnvProxy("CI_DEPLOY_PASSWORD")
    """
    Authentication password of the GitLab Deploy Token,
    only present if the Project has one related.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPLOY_USER: str = EnvProxy("CI_DEPLOY_USER")
    """
    Authentication username of the GitLab Deploy Token,
    only present if the Project has one related.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DISPOSABLE_ENVIRONMENT: Optional[str] = EnvProxy("CI_DISPOSABLE_ENVIRONMENT", always_available=False)
    """
    Marks that the job is executed in a disposable environment
    (something that is created only for this job and disposed of/destroyed
    after the execution - all executors except shell and ssh).
    If the environment is disposable, it is set to true,
    otherwise it is not defined at all.

    Added in GitLab all
    Available in GitLab Runner 10.1
    """

    CI_ENVIRONMENT_NAME: Optional[str] = EnvProxy("CI_ENVIRONMENT_NAME", always_available=False)
    """
    The name of the environment for this job.
    Only present if environment:name is set.

    Added in GitLab 8.15
    Available in GitLab Runner all
    """

    CI_ENVIRONMENT_SLUG: Optional[str] = EnvProxy("CI_ENVIRONMENT_SLUG", always_available=False)
    """
    A simplified version of the environment name,
    suitable for inclusion in DNS, URLs, Kubernetes labels, and so on.
    Only present if environment:name is set.

    Added in GitLab 8.15
    Available in GitLab Runner all
    """

    CI_ENVIRONMENT_URL: Optional[str] = EnvProxy("CI_ENVIRONMENT_URL", always_available=False)
    """
    The URL of the environment for this job.
    Only present if environment:url is set.

    Added in GitLab 9.3
    Available in GitLab Runner all
    """

    CI_EXTERNAL_PULL_REQUEST_IID: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_IID", always_available=False)
    """
    Pull Request ID from GitHub if the pipelines are for
    external pull requests.
    Available only if only [external_pull_requests] or
    rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY", always_available=False)  # noqa yapf: disable
    """
    The source repository name of the pull request if the pipelines are
    for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and
    the pull request is open.

    Added in GitLab 13.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY", always_available=False)  # noqa yapf: disable
    """
    The target repository name of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 13.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME", always_available=False)  # noqa yapf: disable
    """
    The source branch name of the pull request if the pipelines are for
    external pull requests. Available only if only [external_pull_requests]
    or rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA", always_available=False)  # noqa yapf: disable
    """
    The HEAD SHA of the source branch of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME", always_available=False)  # noqa yapf: disable
    """
    The target branch name of the pull request if the pipelines are for
    external pull requests. Available only if only [external_pull_requests]
    or rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA: Optional[str] = EnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA", always_available=False)  # noqa yapf: disable
    """
    The HEAD SHA of the target branch of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_HAS_OPEN_REQUIREMENTS: Optional[str] = EnvProxy("CI_HAS_OPEN_REQUIREMENTS", always_available=False)
    """
    Included with the value true only if the pipeline’s project has any
    open requirements. Not included if there are no open requirements for
    the pipeline’s project.

    Added in GitLab 13.1
    Available in GitLab Runner all
    """

    CI_OPEN_MERGE_REQUESTS: Optional[str] = EnvProxy("CI_OPEN_MERGE_REQUESTS", always_available=False)
    """
    Available in branch and merge request pipelines. Contains a
    comma-separated list of up to four merge requests that use the current
    branch and project as the merge request source.
    For example gitlab-org/gitlab!333,gitlab-org/gitlab-foss!11.

    Added in GitLab 13.8
    Available in GitLab Runner all
    """

    CI_JOB_ID: str = EnvProxy("CI_JOB_ID")
    """
    The unique ID of the current job that GitLab CI/CD uses internally.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_IMAGE: str = EnvProxy("CI_JOB_IMAGE")
    """
    The name of the image running the CI job.

    Added in GitLab 12.9
    Available in GitLab Runner 12.9

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_MANUAL: str = EnvProxy("CI_JOB_MANUAL")
    """
    The flag to indicate that job was manually started.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_NAME: str = EnvProxy("CI_JOB_NAME")
    """
    The name of the job as defined in .gitlab-ci.yml.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_STAGE: str = EnvProxy("CI_JOB_STAGE")
    """
    The name of the stage as defined in .gitlab-ci.yml.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_STATUS: str = EnvProxy("CI_JOB_STATUS")
    """
    The state of the job as each runner stage is executed.
    Use with after_script where CI_JOB_STATUS can be either success,
    failed or canceled.

    Added in GitLab all
    Available in GitLab Runner 13.5

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.

    """

    CI_JOB_TOKEN: str = EnvProxy("CI_JOB_TOKEN")
    """
    Token used for authenticating with a few API endpoints and downloading
    dependent repositories. The token is valid as long as the job is running.

    Added in GitLab 9.0
    Available in GitLab Runner 1.2

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_JWT: str = EnvProxy("CI_JOB_JWT")
    """
    RS256 JSON web token that can be used for authenticating with third
    party systems that support JWT authentication, for example HashiCorp’s Vault.

    Added in GitLab 12.10
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_URL: str = EnvProxy("CI_JOB_URL")
    """
    Job details URL.

    Added in GitLab 11.1
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_KUBERNETES_ACTIVE: Optional[str] = EnvProxy("CI_KUBERNETES_ACTIVE", always_available=False)
    """
    Included with the value true only if the pipeline has a Kubernetes
    cluster available for deployments. Not included if no cluster is available.
    Can be used as an alternative to only:kubernetes/except:kubernetes
    with rules:if.

    Added in GitLab 13.0
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_ASSIGNEES: Optional[str] = EnvProxy("CI_MERGE_REQUEST_ASSIGNEES", always_available=False)
    """
    Comma-separated list of username(s) of assignee(s) for the merge request
    if the pipelines are for merge requests.
    Available only if only [merge_requests] or rules syntax is used and the
    merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_ID: Optional[str] = EnvProxy("CI_MERGE_REQUEST_ID", always_available=False)
    """
    The instance-level ID of the merge request. Only available if the
    pipelines are for merge requests and the merge request is created.
    This is a unique ID across all projects on GitLab.

    Added in GitLab 11.6
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_IID: Optional[str] = EnvProxy("CI_MERGE_REQUEST_IID", always_available=False)
    """
    The project-level IID (internal ID) of the merge request.
    Only available If the pipelines are for merge requests and the merge
    request is created. This ID is unique for the current project.

    Added in GitLab 11.6
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_LABELS: Optional[str] = EnvProxy("CI_MERGE_REQUEST_LABELS", always_available=False)
    """
    Comma-separated label names of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_MILESTONE: Optional[str] = EnvProxy("CI_MERGE_REQUEST_MILESTONE", always_available=False)
    """
    The milestone title of the merge request if the pipelines are for merge
    requests. Available only if only [merge_requests] or rules syntax is
    used and the merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_ID: Optional[str] = EnvProxy("CI_MERGE_REQUEST_PROJECT_ID", always_available=False)
    """
    The ID of the project of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_PATH: Optional[str] = EnvProxy("CI_MERGE_REQUEST_PROJECT_PATH", always_available=False)
    """
    The path of the project of the merge request if the pipelines are for
    merge requests (for example namespace/awesome-project). Available only
    if only [merge_requests] or rules syntax is used and the merge request
    is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_URL: Optional[str] = EnvProxy("CI_MERGE_REQUEST_PROJECT_URL", always_available=False)
    """
    The URL of the project of the merge request if the pipelines are for
    merge requests (for example http://192.168.10.15:3000/namespace/awesome-project).
    Available only if only [merge_requests] or rules syntax is used and the merge
    request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_REF_PATH: Optional[str] = EnvProxy("CI_MERGE_REQUEST_REF_PATH", always_available=False)
    """
    The ref path of the merge request if the pipelines are for merge requests.
    (for example refs/merge-requests/1/head). Available only if only
    [merge_requests] or rules syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_BRANCH_NAME: Optional[str] = EnvProxy("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME", always_available=False)
    """
    The source branch name of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_BRANCH_SHA: Optional[str] = EnvProxy("CI_MERGE_REQUEST_SOURCE_BRANCH_SHA", always_available=False)
    """
    The HEAD SHA of the source branch of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or rules
    syntax is used, the merge request is created, and the pipeline is a
    merged result pipeline.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_ID: Optional[str] = EnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_ID", always_available=False)
    """
    The ID of the source project of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_PATH: Optional[str] = EnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_PATH", always_available=False)
    """
    The path of the source project of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or
    rules syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_URL: Optional[str] = EnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_URL", always_available=False)
    """
    The URL of the source project of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TARGET_BRANCH_NAME: Optional[str] = EnvProxy("CI_MERGE_REQUEST_TARGET_BRANCH_NAME", always_available=False)
    """
    The target branch name of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TARGET_BRANCH_SHA: Optional[str] = EnvProxy("CI_MERGE_REQUEST_TARGET_BRANCH_SHA", always_available=False)
    """
    The HEAD SHA of the target branch of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or rules
    syntax is used, the merge request is created, and the pipeline is a merged
    result pipeline.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TITLE: Optional[str] = EnvProxy("CI_MERGE_REQUEST_TITLE", always_available=False)
    """
    The title of the merge request if the pipelines are for merge requests.
    Available only if only [merge_requests] or rules syntax is used and the
    merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_EVENT_TYPE: Optional[str] = EnvProxy("CI_MERGE_REQUEST_EVENT_TYPE", always_available=False)
    """
    The event type of the merge request, if the pipelines are for merge requests.
    Can be detached, merged_result or merge_train.

    Added in GitLab 12.3
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_DIFF_ID: Optional[str] = EnvProxy("CI_MERGE_REQUEST_DIFF_ID", always_available=False)
    """
    The version of the merge request diff, if the pipelines are for merge requests.

    Added in GitLab 13.7
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_DIFF_BASE_SHA: Optional[str] = EnvProxy("CI_MERGE_REQUEST_DIFF_BASE_SHA", always_available=False)
    """
    The base SHA of the merge request diff, if the pipelines are for merge requests.

    Added in GitLab 13.7
    Available in GitLab Runner all
    """

    CI_NODE_INDEX: Optional[str] = EnvProxy("CI_NODE_INDEX", always_available=False)
    """
    Index of the job in the job set. If the job is not parallelized, this variable is not set.

    Added in GitLab 11.5
    Available in GitLab Runner all
    """

    CI_NODE_TOTAL: str = EnvProxy("CI_NODE_TOTAL")
    """
    Total number of instances of this job running in parallel. If the job is not parallelized, this variable is set to 1.

    Added in GitLab 11.5
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PAGES_DOMAIN: str = EnvProxy("CI_PAGES_DOMAIN")
    """
    The configured domain that hosts GitLab Pages.

    Added in GitLab 11.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PAGES_URL: str = EnvProxy("CI_PAGES_URL")
    """
    URL to GitLab Pages-built pages. Always belongs to a subdomain of CI_PAGES_DOMAIN.

    Added in GitLab 11.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_ID: str = EnvProxy("CI_PIPELINE_ID")
    """
    The instance-level ID of the current pipeline. This is a unique ID
    across all projects on GitLab.

    Added in GitLab 8.10
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_IID: str = EnvProxy("CI_PIPELINE_IID")
    """
    The project-level IID (internal ID) of the current pipeline.
    This ID is unique for the current project.

    Added in GitLab 11.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_SOURCE: str = EnvProxy("CI_PIPELINE_SOURCE")
    """
    Indicates how the pipeline was triggered.
    Possible options are push, web, schedule, api, external, chat, webide,
    merge_request_event, external_pull_request_event, parent_pipeline,
    trigger, or pipeline.
    For pipelines created before GitLab 9.5, this is displayed as unknown.

    Added in GitLab 10.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_TRIGGERED: str = EnvProxy("CI_PIPELINE_TRIGGERED")
    """
    The flag to indicate that job was triggered.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_URL: str = EnvProxy("CI_PIPELINE_URL")
    """
    Pipeline details URL.

    Added in GitLab 11.1
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_CONFIG_PATH: str = EnvProxy("CI_PROJECT_CONFIG_PATH")
    """
    The CI configuration path for the project.

    Added in GitLab 13.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_DIR: str = EnvProxy("CI_PROJECT_DIR")
    """
    The full path where the repository is cloned and where the job is run.
    If the GitLab Runner builds_dir parameter is set, this variable is set
    relative to the value of builds_dir. For more information, see Advanced
    configuration for GitLab Runner.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_ID: str = EnvProxy("CI_PROJECT_ID")
    """
    The unique ID of the current project that GitLab CI/CD uses internally.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_NAME: str = EnvProxy("CI_PROJECT_NAME")
    """
    The name of the directory for the project that is being built.
    For example, if the project URL is gitlab.example.com/group-name/project-1,
    the CI_PROJECT_NAME would be project-1.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_NAMESPACE: str = EnvProxy("CI_PROJECT_NAMESPACE")
    """
    The project namespace (username or group name) that is being built.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_ROOT_NAMESPACE: str = EnvProxy("CI_PROJECT_ROOT_NAMESPACE")
    """
    The root project namespace (username or group name) that is being built.
    For example, if CI_PROJECT_NAMESPACE is root-group/child-group/grandchild-group,
    CI_PROJECT_ROOT_NAMESPACE would be root-group.

    Added in GitLab 13.2
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_PATH: str = EnvProxy("CI_PROJECT_PATH")
    """
    The namespace with project name.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_PATH_SLUG: str = EnvProxy("CI_PROJECT_PATH_SLUG")
    """
    $CI_PROJECT_PATH in lowercase and with everything except 0-9 and a-z replaced with -. Use in URLs and domain names.

    Added in GitLab 9.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_REPOSITORY_LANGUAGES: str = EnvProxy("CI_PROJECT_REPOSITORY_LANGUAGES")
    """
    Comma-separated, lowercase list of the languages used in the repository (for example ruby,javascript,html,css).

    Added in GitLab 12.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_TITLE: str = EnvProxy("CI_PROJECT_TITLE")
    """
    The human-readable project name as displayed in the GitLab web interface.

    Added in GitLab 12.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_URL: str = EnvProxy("CI_PROJECT_URL")
    """
    The HTTP(S) address to access project.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_VISIBILITY: str = EnvProxy("CI_PROJECT_VISIBILITY")
    """
    The project visibility (internal, private, public).

    Added in GitLab 10.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_REGISTRY: Optional[str] = EnvProxy("CI_REGISTRY", always_available=False)
    """
    GitLab Container Registry. This variable includes a :port value if one
    has been specified in the registry configuration.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5
    """

    CI_REGISTRY_IMAGE: Optional[str] = EnvProxy("CI_REGISTRY_IMAGE", always_available=False)
    """
    the address of the registry tied to the specific project.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_REGISTRY_PASSWORD: Optional[str] = EnvProxy("CI_REGISTRY_PASSWORD", always_available=False)
    """
    The password to use to push containers to the GitLab Container Registry, for the current project.

    Added in GitLab 9.0
    Available in GitLab Runner all
    """

    CI_REGISTRY_USER: Optional[str] = EnvProxy("CI_REGISTRY_USER", always_available=False)
    """
    The username to use to push containers to the GitLab Container Registry, for the current project.

    Added in GitLab 9.0
    Available in GitLab Runner all
    """

    CI_REPOSITORY_URL: str = EnvProxy("CI_REPOSITORY_URL")
    """
    The URL to clone the Git repository.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_DESCRIPTION: str = EnvProxy("CI_RUNNER_DESCRIPTION")
    """
    The description of the runner as saved in GitLab.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_EXECUTABLE_ARCH: str = EnvProxy("CI_RUNNER_EXECUTABLE_ARCH")
    """
    The OS/architecture of the GitLab Runner executable (note that this is not necessarily the same as the environment of the executor).

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_ID: str = EnvProxy("CI_RUNNER_ID")
    """
    The unique ID of runner being used.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_REVISION: str = EnvProxy("CI_RUNNER_REVISION")
    """
    GitLab Runner revision that is executing the current job.

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_SHORT_TOKEN: str = EnvProxy("CI_RUNNER_SHORT_TOKEN")
    """
    First eight characters of the runner’s token used to authenticate new job requests. Used as the runner’s unique ID.

    Added in GitLab all
    Available in GitLab Runner 12.3

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_TAGS: str = EnvProxy("CI_RUNNER_TAGS")
    """
    The defined runner tags.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_VERSION: str = EnvProxy("CI_RUNNER_VERSION")
    """
    GitLab Runner version that is executing the current job.

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER: str = EnvProxy("CI_SERVER")
    """
    Mark that job is executed in CI environment.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_URL: str = EnvProxy("CI_SERVER_URL")
    """
    The base URL of the GitLab instance, including protocol and port (like https://gitlab.example.com:8080).

    Added in GitLab 12.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_HOST: str = EnvProxy("CI_SERVER_HOST")
    """
    Host component of the GitLab instance URL, without protocol and port (like gitlab.example.com).

    Added in GitLab 12.1
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_PORT: str = EnvProxy("CI_SERVER_PORT")
    """
    Port component of the GitLab instance URL, without host and protocol (like 3000).

    Added in GitLab 12.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_PROTOCOL: str = EnvProxy("CI_SERVER_PROTOCOL")
    """
    Protocol component of the GitLab instance URL, without host and port (like https).

    Added in GitLab 12.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_NAME: str = EnvProxy("CI_SERVER_NAME")
    """
    The name of CI server that is used to coordinate jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_REVISION: str = EnvProxy("CI_SERVER_REVISION")
    """
    GitLab revision that is used to schedule jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION: str = EnvProxy("CI_SERVER_VERSION")
    """
    GitLab version that is used to schedule jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_MAJOR: str = EnvProxy("CI_SERVER_VERSION_MAJOR")
    """
    GitLab version major component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_MINOR: str = EnvProxy("CI_SERVER_VERSION_MINOR")
    """
    GitLab version minor component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_PATCH: str = EnvProxy("CI_SERVER_VERSION_PATCH")
    """
    GitLab version patch component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SHARED_ENVIRONMENT: Optional[str] = EnvProxy("CI_SHARED_ENVIRONMENT", always_available=False)
    """
    Marks that the job is executed in a shared environment (something that
    is persisted across CI invocations like shell or ssh executor).
    If the environment is shared, it is set to true, otherwise it is not
    defined at all.

    Added in GitLab all
    Available in GitLab Runner 10.1
    """

    GITLAB_CI: str = EnvProxy("GITLAB_CI")
    """
    Mark that job is executed in GitLab CI/CD environment.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_FEATURES: str = EnvProxy("GITLAB_FEATURES")
    """
    The comma separated list of licensed features available for your instance and plan.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_EMAIL: str = EnvProxy("GITLAB_USER_EMAIL")
    """
    The email of the user who started the job.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_ID: str = EnvProxy("GITLAB_USER_ID")
    """
    The ID of the user who started the job.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_LOGIN: str = EnvProxy("GITLAB_USER_LOGIN")
    """
    The login username of the user who started the job.

    Added in GitLab 10.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_NAME: str = EnvProxy("GITLAB_USER_NAME")
    """
    The real name of the user who started the job.

    Added in GitLab 10.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    TRIGGER_PAYLOAD: Optional[str] = EnvProxy("TRIGGER_PAYLOAD", always_available=False)
    """
    This variable is available when a pipeline is triggered with a webhook

    Added in GitLab 13.9
    Available in GitLab Runner all
    """
