import os
from typing import Any, Optional


# In Python >= 3.9 it is also possible to use @classmethods and @property
# together, so that there are no parantheses necessarry.
# See https://stackoverflow.com/questions/128573/using-property-on-classmethods´
class EnvProxy:
    """This proxy delays the operating system query for environment variables until the value is requested.

    This proxy is designed for requesting predefined environment variables that must
    exist within a Gitlab CI pipeline execution. Create an object from this proxy
    with the name of the Gitlab `CI_*` variable you want to query:

    ```
    CI_COMMIT_REF_SLUG = EnvProxy("CI_COMMIT_REF_SLUG")  # os.environ is not (!) called here
    ...
    ```

    When using an object of this proxy in a statement it returns the value of the `CI_*`
    variable requested or raises a `KeyError` if against our expectations the variable
    is not available.

    ```
    ...
    if CI_COMMIT_REF_SLUG == "foobar":  # <- os.environ is called here
        ...
    ```

    The proxy has a different behavior when not being called within a Gitlab CI pipeline
    execution. This is, when the environment variable `CI` is unset (from the official
    Gitlab CI docs). Then the proxy does not raise a KeyError for `CI_*` variables, because
    they naturally does not exist (or at least their existence is not guaranteed).
    So if we are not running within a Gitlab CI pipeline, the proxy insteads returns the
    dummy string `notRunningInAPipeline` for all `CI_*` variables. Except for the `CI`
    variable itself, where an empty string is returned, indicating we are not running
    within a pipeline

    Args:
        key (str): The name of the environment variable that should be queried on request.
    """

    def __init__(self, key: str) -> None:
        self._key = key

    def __get__(self, obj: Any, objtype: Any = None) -> str:
        if os.getenv("CI"):  # when running within a gitlab ci pipeline
            return os.environ[self._key]

        # indicate that we are not running within a pipeline by
        # returning an empty string
        if self._key == "CI":
            return ""

        # in the case we are not running within a pipeline ($CI is empty)
        # for all other variables we return a dummy value which
        # explicitly describe this state
        return "notRunningInAPipeline"


class OptionalEnvProxy:
    """This class represents an optional environment variable.

    It returns `os.getenv(<key>)` on the key given in the `__init__()` method.

    The class can be used in every expression where the `Optional[str]` of `os.getenv()` is expected:

    ```
    myvar = OptionalEnvProxy("MY_ENVIRONMENT_VARIABLE")
    ```

    The purpose of this class is to delay the execution of `os.getenv()`. In the upper example `myvar` is
    only set to this `OptionalEnvProxy` object. The value itself is retrieved with `os.getenv()` in the moment
    when `myvar` is used.
    """

    def __init__(self, key: str) -> None:
        self._key = key

    def __get__(self, obj: Any, objtype: Any = None) -> Optional[str]:
        return os.getenv(self._key)


class PredefinedVariables:
    """
    Gitlab CI predefined variables.
    https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
    """

    CHAT_CHANNEL: EnvProxy = EnvProxy("CHAT_CHANNEL")
    """
    Source chat channel which triggered the ChatOps command.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CHAT_INPUT: EnvProxy = EnvProxy("CHAT_INPUT")
    """
    Additional arguments passed in the ChatOps command.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI: EnvProxy = EnvProxy("CI")
    """
    Mark that job is executed in CI environment.

    Added in GitLab all
    Available in GitLab Runner 0.4

    Raises:
        KeyError: If environment variable not available.
    """

    CI_API_V4_URL: EnvProxy = EnvProxy("CI_API_V4_URL")
    """
    The GitLab API v4 root URL.

    Added in GitLab 11.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_BUILDS_DIR: EnvProxy = EnvProxy("CI_BUILDS_DIR")
    """
    Top-level directory where builds are executed.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_BEFORE_SHA: EnvProxy = EnvProxy("CI_COMMIT_BEFORE_SHA")
    """
    The previous latest commit present on a branch. Is always
    0000000000000000000000000000000000000000 in pipelines for merge requests.

    Added in GitLab 11.2
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_DESCRIPTION: EnvProxy = EnvProxy("CI_COMMIT_DESCRIPTION")
    """
    The description of the commit the message without first line,
    if the title is shorter than 100 characters; full message in other case.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    """

    CI_COMMIT_MESSAGE: EnvProxy = EnvProxy("CI_COMMIT_MESSAGE")
    """
    The full commit message.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_NAME: EnvProxy = EnvProxy("CI_COMMIT_REF_NAME")
    """
    The branch or tag name for which project is built.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_PROTECTED: EnvProxy = EnvProxy("CI_COMMIT_REF_PROTECTED")
    """
    true if the job is running on a protected reference, false if not.

    Added in GitLab 11.11
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_REF_SLUG: EnvProxy = EnvProxy("CI_COMMIT_REF_SLUG")
    """
    $CI_COMMIT_REF_NAME in lowercase, shortened to 63 bytes,
    and with everything except 0-9 and a-z replaced with -.
    No leading / trailing -. Use in URLs, host names and domain names.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_SHA: EnvProxy = EnvProxy("CI_COMMIT_SHA")
    """
    The commit revision for which project is built.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_SHORT_SHA: EnvProxy = EnvProxy("CI_COMMIT_SHORT_SHA")
    """
    The first eight characters of CI_COMMIT_SHA.

    Added in GitLab 11.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_BRANCH: OptionalEnvProxy = OptionalEnvProxy("CI_COMMIT_BRANCH")
    """
    The commit branch name. Present in branch pipelines,
    including pipelines for the default branch.
    Not present in merge request pipelines or tag pipelines.

    Added in GitLab 12.6
    Available in GitLab Runner 0.5
    """

    CI_COMMIT_TAG: OptionalEnvProxy = OptionalEnvProxy("CI_COMMIT_TAG")
    """
    The commit tag name. Present only when building tags.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5
    """

    CI_COMMIT_TITLE: EnvProxy = EnvProxy("CI_COMMIT_TITLE")
    """
    The title of the commit - the full first line of the message.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_COMMIT_TIMESTAMP: EnvProxy = EnvProxy("CI_COMMIT_TIMESTAMP")
    """
    The timestamp of the commit in the ISO 8601 format.

    Added in GitLab 13.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONCURRENT_ID: EnvProxy = EnvProxy("CI_CONCURRENT_ID")
    """
    Unique ID of build execution in a single executor.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONCURRENT_PROJECT_ID: EnvProxy = EnvProxy("CI_CONCURRENT_PROJECT_ID")
    """
    Unique ID of build execution in a single executor and project.

    Added in GitLab all
    Available in GitLab Runner 11.10

    Raises:
        KeyError: If environment variable not available.
    """

    CI_CONFIG_PATH: EnvProxy = EnvProxy("CI_CONFIG_PATH")
    """
    The path to CI configuration file. Defaults to .gitlab-ci.yml.

    Added in GitLab 9.4
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEBUG_TRACE: EnvProxy = EnvProxy("CI_DEBUG_TRACE")
    """
    Whether debug logging (tracing) is enabled.

    Added in GitLab all
    Available in GitLab Runner 1.7

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEFAULT_BRANCH: EnvProxy = EnvProxy("CI_DEFAULT_BRANCH")
    """
    The name of the default branch for the project.

    Added in GitLab 12.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX: EnvProxy = EnvProxy("CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX")
    """
    The image prefix for pulling images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_SERVER: EnvProxy = EnvProxy("CI_DEPENDENCY_PROXY_SERVER")
    """
    The server for logging in to the Dependency Proxy. This is equivalent to $CI_SERVER_HOST:$CI_SERVER_PORT.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_PASSWORD: EnvProxy = EnvProxy("CI_DEPENDENCY_PROXY_PASSWORD")
    """
    The password to use to pull images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPENDENCY_PROXY_USER: EnvProxy = EnvProxy("CI_DEPENDENCY_PROXY_USER")
    """
    The username to use to pull images through the Dependency Proxy.

    Added in GitLab 13.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPLOY_FREEZE: OptionalEnvProxy = OptionalEnvProxy("CI_DEPLOY_FREEZE")
    """
    Included with the value true if the pipeline runs during a deploy freeze window.

    Added in GitLab 13.2
    Available in GitLab Runner all
    """

    CI_DEPLOY_PASSWORD: EnvProxy = EnvProxy("CI_DEPLOY_PASSWORD")
    """
    Authentication password of the GitLab Deploy Token,
    only present if the Project has one related.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DEPLOY_USER: EnvProxy = EnvProxy("CI_DEPLOY_USER")
    """
    Authentication username of the GitLab Deploy Token,
    only present if the Project has one related.

    Added in GitLab 10.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_DISPOSABLE_ENVIRONMENT: OptionalEnvProxy = OptionalEnvProxy("CI_DISPOSABLE_ENVIRONMENT")
    """
    Marks that the job is executed in a disposable environment
    (something that is created only for this job and disposed of/destroyed
    after the execution - all executors except shell and ssh).
    If the environment is disposable, it is set to true,
    otherwise it is not defined at all.

    Added in GitLab all
    Available in GitLab Runner 10.1
    """

    CI_ENVIRONMENT_NAME: OptionalEnvProxy = OptionalEnvProxy("CI_ENVIRONMENT_NAME")
    """
    The name of the environment for this job.
    Only present if environment:name is set.

    Added in GitLab 8.15
    Available in GitLab Runner all
    """

    CI_ENVIRONMENT_SLUG: OptionalEnvProxy = OptionalEnvProxy("CI_ENVIRONMENT_SLUG")
    """
    A simplified version of the environment name,
    suitable for inclusion in DNS, URLs, Kubernetes labels, and so on.
    Only present if environment:name is set.

    Added in GitLab 8.15
    Available in GitLab Runner all
    """

    CI_ENVIRONMENT_URL: OptionalEnvProxy = OptionalEnvProxy("CI_ENVIRONMENT_URL")
    """
    The URL of the environment for this job.
    Only present if environment:url is set.

    Added in GitLab 9.3
    Available in GitLab Runner all
    """

    CI_EXTERNAL_PULL_REQUEST_IID: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_IID")
    """
    Pull Request ID from GitHub if the pipelines are for
    external pull requests.
    Available only if only [external_pull_requests] or
    rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY")
    """
    The source repository name of the pull request if the pipelines are
    for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and
    the pull request is open.

    Added in GitLab 13.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY")
    """
    The target repository name of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 13.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME")
    """
    The source branch name of the pull request if the pipelines are for
    external pull requests. Available only if only [external_pull_requests]
    or rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA")
    """
    The HEAD SHA of the source branch of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME")
    """
    The target branch name of the pull request if the pipelines are for
    external pull requests. Available only if only [external_pull_requests]
    or rules syntax is used and the pull request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA: OptionalEnvProxy = OptionalEnvProxy("CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA")
    """
    The HEAD SHA of the target branch of the pull request if the pipelines
    are for external pull requests. Available only if only
    [external_pull_requests] or rules syntax is used and the pull
    request is open.

    Added in GitLab 12.3
    Available in GitLab Runner all

    """

    CI_HAS_OPEN_REQUIREMENTS: OptionalEnvProxy = OptionalEnvProxy("CI_HAS_OPEN_REQUIREMENTS")
    """
    Included with the value true only if the pipeline’s project has any
    open requirements. Not included if there are no open requirements for
    the pipeline’s project.

    Added in GitLab 13.1
    Available in GitLab Runner all
    """

    CI_OPEN_MERGE_REQUESTS: OptionalEnvProxy = OptionalEnvProxy("CI_OPEN_MERGE_REQUESTS")
    """
    Available in branch and merge request pipelines. Contains a
    comma-separated list of up to four merge requests that use the current
    branch and project as the merge request source.
    For example gitlab-org/gitlab!333,gitlab-org/gitlab-foss!11.

    Added in GitLab 13.8
    Available in GitLab Runner all
    """

    CI_JOB_ID: EnvProxy = EnvProxy("CI_JOB_ID")
    """
    The unique ID of the current job that GitLab CI/CD uses internally.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_IMAGE: EnvProxy = EnvProxy("CI_JOB_IMAGE")
    """
    The name of the image running the CI job.

    Added in GitLab 12.9
    Available in GitLab Runner 12.9

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_MANUAL: EnvProxy = EnvProxy("CI_JOB_MANUAL")
    """
    The flag to indicate that job was manually started.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_NAME: EnvProxy = EnvProxy("CI_JOB_NAME")
    """
    The name of the job as defined in .gitlab-ci.yml.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_STAGE: EnvProxy = EnvProxy("CI_JOB_STAGE")
    """
    The name of the stage as defined in .gitlab-ci.yml.

    Added in GitLab 9.0
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.

    Raises:
        KeyError: If environment variable not available.
    """

    CI_JOB_STATUS: EnvProxy = EnvProxy("CI_JOB_STATUS")
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

    CI_JOB_TOKEN: EnvProxy = EnvProxy("CI_JOB_TOKEN")
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

    CI_JOB_JWT: EnvProxy = EnvProxy("CI_JOB_JWT")
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

    CI_JOB_URL: EnvProxy = EnvProxy("CI_JOB_URL")
    """
    Job details URL.

    Added in GitLab 11.1
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_KUBERNETES_ACTIVE: OptionalEnvProxy = OptionalEnvProxy("CI_KUBERNETES_ACTIVE")
    """
    Included with the value true only if the pipeline has a Kubernetes
    cluster available for deployments. Not included if no cluster is available.
    Can be used as an alternative to only:kubernetes/except:kubernetes
    with rules:if.

    Added in GitLab 13.0
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_ASSIGNEES: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_ASSIGNEES")
    """
    Comma-separated list of username(s) of assignee(s) for the merge request
    if the pipelines are for merge requests.
    Available only if only [merge_requests] or rules syntax is used and the
    merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_ID: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_ID")
    """
    The instance-level ID of the merge request. Only available if the
    pipelines are for merge requests and the merge request is created.
    This is a unique ID across all projects on GitLab.

    Added in GitLab 11.6
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_IID: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_IID")
    """
    The project-level IID (internal ID) of the merge request.
    Only available If the pipelines are for merge requests and the merge
    request is created. This ID is unique for the current project.

    Added in GitLab 11.6
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_LABELS: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_LABELS")
    """
    Comma-separated label names of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_MILESTONE: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_MILESTONE")
    """
    The milestone title of the merge request if the pipelines are for merge
    requests. Available only if only [merge_requests] or rules syntax is
    used and the merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_ID: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_PROJECT_ID")
    """
    The ID of the project of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_PATH: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_PROJECT_PATH")
    """
    The path of the project of the merge request if the pipelines are for
    merge requests (for example namespace/awesome-project). Available only
    if only [merge_requests] or rules syntax is used and the merge request
    is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_PROJECT_URL: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_PROJECT_URL")
    """
    The URL of the project of the merge request if the pipelines are for
    merge requests (for example http://192.168.10.15:3000/namespace/awesome-project).
    Available only if only [merge_requests] or rules syntax is used and the merge
    request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_REF_PATH: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_REF_PATH")
    """
    The ref path of the merge request if the pipelines are for merge requests.
    (for example refs/merge-requests/1/head). Available only if only
    [merge_requests] or rules syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_BRANCH_NAME: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_SOURCE_BRANCH_NAME")
    """
    The source branch name of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_BRANCH_SHA: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_SOURCE_BRANCH_SHA")
    """
    The HEAD SHA of the source branch of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or rules
    syntax is used, the merge request is created, and the pipeline is a
    merged result pipeline.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_ID: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_ID")
    """
    The ID of the source project of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_PATH: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_PATH")
    """
    The path of the source project of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or
    rules syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_SOURCE_PROJECT_URL: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_SOURCE_PROJECT_URL")
    """
    The URL of the source project of the merge request if the pipelines are
    for merge requests. Available only if only [merge_requests] or rules
    syntax is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TARGET_BRANCH_NAME: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
    """
    The target branch name of the merge request if the pipelines are for
    merge requests. Available only if only [merge_requests] or rules syntax
    is used and the merge request is created.

    Added in GitLab 11.6
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TARGET_BRANCH_SHA: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_TARGET_BRANCH_SHA")
    """
    The HEAD SHA of the target branch of the merge request if the pipelines
    are for merge requests. Available only if only [merge_requests] or rules
    syntax is used, the merge request is created, and the pipeline is a merged
    result pipeline.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_TITLE: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_TITLE")
    """
    The title of the merge request if the pipelines are for merge requests.
    Available only if only [merge_requests] or rules syntax is used and the
    merge request is created.

    Added in GitLab 11.9
    Available in GitLab Runner all

    """

    CI_MERGE_REQUEST_EVENT_TYPE: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_EVENT_TYPE")
    """
    The event type of the merge request, if the pipelines are for merge requests.
    Can be detached, merged_result or merge_train.

    Added in GitLab 12.3
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_DIFF_ID: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_DIFF_ID")
    """
    The version of the merge request diff, if the pipelines are for merge requests.

    Added in GitLab 13.7
    Available in GitLab Runner all
    """

    CI_MERGE_REQUEST_DIFF_BASE_SHA: OptionalEnvProxy = OptionalEnvProxy("CI_MERGE_REQUEST_DIFF_BASE_SHA")
    """
    The base SHA of the merge request diff, if the pipelines are for merge requests.

    Added in GitLab 13.7
    Available in GitLab Runner all
    """

    CI_NODE_INDEX: OptionalEnvProxy = OptionalEnvProxy("CI_NODE_INDEX")
    """
    Index of the job in the job set. If the job is not parallelized, this variable is not set.

    Added in GitLab 11.5
    Available in GitLab Runner all
    """

    CI_NODE_TOTAL: EnvProxy = EnvProxy("CI_NODE_TOTAL")
    """
    Total number of instances of this job running in parallel. If the job is not parallelized, this variable is set to 1.

    Added in GitLab 11.5
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PAGES_DOMAIN: EnvProxy = EnvProxy("CI_PAGES_DOMAIN")
    """
    The configured domain that hosts GitLab Pages.

    Added in GitLab 11.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PAGES_URL: EnvProxy = EnvProxy("CI_PAGES_URL")
    """
    URL to GitLab Pages-built pages. Always belongs to a subdomain of CI_PAGES_DOMAIN.

    Added in GitLab 11.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_ID: EnvProxy = EnvProxy("CI_PIPELINE_ID")
    """
    The instance-level ID of the current pipeline. This is a unique ID
    across all projects on GitLab.

    Added in GitLab 8.10
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_IID: EnvProxy = EnvProxy("CI_PIPELINE_IID")
    """
    The project-level IID (internal ID) of the current pipeline.
    This ID is unique for the current project.

    Added in GitLab 11.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_SOURCE: EnvProxy = EnvProxy("CI_PIPELINE_SOURCE")
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

    CI_PIPELINE_TRIGGERED: EnvProxy = EnvProxy("CI_PIPELINE_TRIGGERED")
    """
    The flag to indicate that job was triggered.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PIPELINE_URL: EnvProxy = EnvProxy("CI_PIPELINE_URL")
    """
    Pipeline details URL.

    Added in GitLab 11.1
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_CONFIG_PATH: EnvProxy = EnvProxy("CI_PROJECT_CONFIG_PATH")
    """
    The CI configuration path for the project.

    Added in GitLab 13.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_DIR: EnvProxy = EnvProxy("CI_PROJECT_DIR")
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

    CI_PROJECT_ID: EnvProxy = EnvProxy("CI_PROJECT_ID")
    """
    The unique ID of the current project that GitLab CI/CD uses internally.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_NAME: EnvProxy = EnvProxy("CI_PROJECT_NAME")
    """
    The name of the directory for the project that is being built.
    For example, if the project URL is gitlab.example.com/group-name/project-1,
    the CI_PROJECT_NAME would be project-1.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_NAMESPACE: EnvProxy = EnvProxy("CI_PROJECT_NAMESPACE")
    """
    The project namespace (username or group name) that is being built.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_ROOT_NAMESPACE: EnvProxy = EnvProxy("CI_PROJECT_ROOT_NAMESPACE")
    """
    The root project namespace (username or group name) that is being built.
    For example, if CI_PROJECT_NAMESPACE is root-group/child-group/grandchild-group,
    CI_PROJECT_ROOT_NAMESPACE would be root-group.

    Added in GitLab 13.2
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_PATH: EnvProxy = EnvProxy("CI_PROJECT_PATH")
    """
    The namespace with project name.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_PATH_SLUG: EnvProxy = EnvProxy("CI_PROJECT_PATH_SLUG")
    """
    $CI_PROJECT_PATH in lowercase and with everything except 0-9 and a-z replaced with -. Use in URLs and domain names.

    Added in GitLab 9.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_REPOSITORY_LANGUAGES: EnvProxy = EnvProxy("CI_PROJECT_REPOSITORY_LANGUAGES")
    """
    Comma-separated, lowercase list of the languages used in the repository (for example ruby,javascript,html,css).

    Added in GitLab 12.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_TITLE: EnvProxy = EnvProxy("CI_PROJECT_TITLE")
    """
    The human-readable project name as displayed in the GitLab web interface.

    Added in GitLab 12.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_URL: EnvProxy = EnvProxy("CI_PROJECT_URL")
    """
    The HTTP(S) address to access project.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_PROJECT_VISIBILITY: EnvProxy = EnvProxy("CI_PROJECT_VISIBILITY")
    """
    The project visibility (internal, private, public).

    Added in GitLab 10.3
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_REGISTRY: OptionalEnvProxy = OptionalEnvProxy("CI_REGISTRY")
    """
    GitLab Container Registry. This variable includes a :port value if one
    has been specified in the registry configuration.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5
    """

    CI_REGISTRY_IMAGE: OptionalEnvProxy = OptionalEnvProxy("CI_REGISTRY_IMAGE")
    """
    the address of the registry tied to the specific project.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_REGISTRY_PASSWORD: OptionalEnvProxy = OptionalEnvProxy("CI_REGISTRY_PASSWORD")
    """
    The password to use to push containers to the GitLab Container Registry, for the current project.

    Added in GitLab 9.0
    Available in GitLab Runner all
    """

    CI_REGISTRY_USER: OptionalEnvProxy = OptionalEnvProxy("CI_REGISTRY_USER")
    """
    The username to use to push containers to the GitLab Container Registry, for the current project.

    Added in GitLab 9.0
    Available in GitLab Runner all
    """

    CI_REPOSITORY_URL: EnvProxy = EnvProxy("CI_REPOSITORY_URL")
    """
    The URL to clone the Git repository.

    Added in GitLab 9.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_DESCRIPTION: EnvProxy = EnvProxy("CI_RUNNER_DESCRIPTION")
    """
    The description of the runner as saved in GitLab.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_EXECUTABLE_ARCH: EnvProxy = EnvProxy("CI_RUNNER_EXECUTABLE_ARCH")
    """
    The OS/architecture of the GitLab Runner executable (note that this is not necessarily the same as the environment of the executor).

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_ID: EnvProxy = EnvProxy("CI_RUNNER_ID")
    """
    The unique ID of runner being used.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_REVISION: EnvProxy = EnvProxy("CI_RUNNER_REVISION")
    """
    GitLab Runner revision that is executing the current job.

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_SHORT_TOKEN: EnvProxy = EnvProxy("CI_RUNNER_SHORT_TOKEN")
    """
    First eight characters of the runner’s token used to authenticate new job requests. Used as the runner’s unique ID.

    Added in GitLab all
    Available in GitLab Runner 12.3

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_TAGS: EnvProxy = EnvProxy("CI_RUNNER_TAGS")
    """
    The defined runner tags.

    Added in GitLab 8.10
    Available in GitLab Runner 0.5

    Raises:
        KeyError: If environment variable not available.
    """

    CI_RUNNER_VERSION: EnvProxy = EnvProxy("CI_RUNNER_VERSION")
    """
    GitLab Runner version that is executing the current job.

    Added in GitLab all
    Available in GitLab Runner 10.6

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER: EnvProxy = EnvProxy("CI_SERVER")
    """
    Mark that job is executed in CI environment.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_URL: EnvProxy = EnvProxy("CI_SERVER_URL")
    """
    The base URL of the GitLab instance, including protocol and port (like https://gitlab.example.com:8080).

    Added in GitLab 12.7
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_HOST: EnvProxy = EnvProxy("CI_SERVER_HOST")
    """
    Host component of the GitLab instance URL, without protocol and port (like gitlab.example.com).

    Added in GitLab 12.1
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_PORT: EnvProxy = EnvProxy("CI_SERVER_PORT")
    """
    Port component of the GitLab instance URL, without host and protocol (like 3000).

    Added in GitLab 12.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_PROTOCOL: EnvProxy = EnvProxy("CI_SERVER_PROTOCOL")
    """
    Protocol component of the GitLab instance URL, without host and port (like https).

    Added in GitLab 12.8
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_NAME: EnvProxy = EnvProxy("CI_SERVER_NAME")
    """
    The name of CI server that is used to coordinate jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_REVISION: EnvProxy = EnvProxy("CI_SERVER_REVISION")
    """
    GitLab revision that is used to schedule jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION: EnvProxy = EnvProxy("CI_SERVER_VERSION")
    """
    GitLab version that is used to schedule jobs.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_MAJOR: EnvProxy = EnvProxy("CI_SERVER_VERSION_MAJOR")
    """
    GitLab version major component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_MINOR: EnvProxy = EnvProxy("CI_SERVER_VERSION_MINOR")
    """
    GitLab version minor component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SERVER_VERSION_PATCH: EnvProxy = EnvProxy("CI_SERVER_VERSION_PATCH")
    """
    GitLab version patch component.

    Added in GitLab 11.4
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    CI_SHARED_ENVIRONMENT: OptionalEnvProxy = OptionalEnvProxy("CI_SHARED_ENVIRONMENT")
    """
    Marks that the job is executed in a shared environment (something that
    is persisted across CI invocations like shell or ssh executor).
    If the environment is shared, it is set to true, otherwise it is not
    defined at all.

    Added in GitLab all
    Available in GitLab Runner 10.1
    """

    GITLAB_CI: EnvProxy = EnvProxy("GITLAB_CI")
    """
    Mark that job is executed in GitLab CI/CD environment.

    Added in GitLab all
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_FEATURES: EnvProxy = EnvProxy("GITLAB_FEATURES")
    """
    The comma separated list of licensed features available for your instance and plan.

    Added in GitLab 10.6
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_EMAIL: EnvProxy = EnvProxy("GITLAB_USER_EMAIL")
    """
    The email of the user who started the job.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_ID: EnvProxy = EnvProxy("GITLAB_USER_ID")
    """
    The ID of the user who started the job.

    Added in GitLab 8.12
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_LOGIN: EnvProxy = EnvProxy("GITLAB_USER_LOGIN")
    """
    The login username of the user who started the job.

    Added in GitLab 10.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    GITLAB_USER_NAME: EnvProxy = EnvProxy("GITLAB_USER_NAME")
    """
    The real name of the user who started the job.

    Added in GitLab 10.0
    Available in GitLab Runner all

    Raises:
        KeyError: If environment variable not available.
    """

    TRIGGER_PAYLOAD: OptionalEnvProxy = OptionalEnvProxy("TRIGGER_PAYLOAD")
    """
    This variable is available when a pipeline is triggered with a webhook

    Added in GitLab 13.9
    Available in GitLab Runner all
    """
