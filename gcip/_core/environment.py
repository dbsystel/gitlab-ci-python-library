import os


class GitLabCiEnv():
    """
    Gitlab CI Environment variables.
    """

    @staticmethod
    def CHAT_CHANNEL() -> str:
        """
        Source chat channel which triggered the ChatOps command.

        Added in GitLab 10.6
        Available in GitLab Runner all
        """
        return os.environ["CHAT_CHANNEL"]

    @staticmethod
    def CHAT_INPUT() -> str:
        """
        Additional arguments passed in the ChatOps command.

        Added in GitLab 10.6
        Available in GitLab Runner all
        """
        return os.environ["CHAT_INPUT"]

    @staticmethod
    def CI() -> str:
        """
        Mark that job is executed in CI environment.

        Added in GitLab all
        Available in GitLab Runner 0.4
        """
        return os.environ["CI"]

    @staticmethod
    def CI_API_V4_URL() -> str:
        """
        The GitLab API v4 root URL.

        Added in GitLab 11.7
        Available in GitLab Runner all
        """
        return os.environ["CI_API_V4_URL"]

    @staticmethod
    def CI_BUILDS_DIR() -> str:
        """
        Top-level directory where builds are executed.

        Added in GitLab all
        Available in GitLab Runner 11.10
        """
        return os.environ["CI_BUILDS_DIR"]

    @staticmethod
    def CI_COMMIT_BEFORE_SHA() -> str:
        """
        The previous latest commit present on a branch. Is always
        0000000000000000000000000000000000000000 in pipelines for merge requests.

        Added in GitLab 11.2
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_BEFORE_SHA"]

    @staticmethod
    def CI_COMMIT_DESCRIPTION() -> str:
        """
        The description of the commit the message without first line,
        if the title is shorter than 100 characters; full message in other case.

        Added in GitLab 10.8
        Available in GitLab Runner all
        return os.environ["CI_COMMIT_DESCRIPTION"]

        """
    @staticmethod
    def CI_COMMIT_MESSAGE() -> str:
        """
        The full commit message.

        Added in GitLab 10.8
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_MESSAGE"]

    @staticmethod
    def CI_COMMIT_REF_NAME() -> str:
        """
        The branch or tag name for which project is built.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_REF_NAME"]

    @staticmethod
    def CI_COMMIT_REF_PROTECTED() -> str:
        """
        true if the job is running on a protected reference, false if not.

        Added in GitLab 11.11
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_REF_PROTECTED"]

    @staticmethod
    def CI_COMMIT_REF_SLUG() -> str:
        """
        $CI_COMMIT_REF_NAME in lowercase, shortened to 63 bytes,
        and with everything except 0-9 and a-z replaced with -.
        No leading / trailing -. Use in URLs, host names and domain names.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_REF_SLUG"]

    @staticmethod
    def CI_COMMIT_SHA() -> str:
        """
        The commit revision for which project is built.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_SHA"]

    @staticmethod
    def CI_COMMIT_SHORT_SHA() -> str:
        """
        The first eight characters of CI_COMMIT_SHA.

        Added in GitLab 11.7
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_SHORT_SHA"]

    @staticmethod
    def CI_COMMIT_BRANCH() -> str:
        """
        The commit branch name. Present in branch pipelines,
        including pipelines for the default branch.
        Not present in merge request pipelines or tag pipelines.

        Added in GitLab 12.6
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_COMMIT_BRANCH"]

    @staticmethod
    def CI_COMMIT_TAG() -> str:
        """
        The commit tag name. Present only when building tags.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_COMMIT_TAG"]

    @staticmethod
    def CI_COMMIT_TITLE() -> str:
        """
        The title of the commit - the full first line of the message.

        Added in GitLab 10.8
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_TITLE"]

    @staticmethod
    def CI_COMMIT_TIMESTAMP() -> str:
        """
        The timestamp of the commit in the ISO 8601 format.

        Added in GitLab 13.4
        Available in GitLab Runner all
        """
        return os.environ["CI_COMMIT_TIMESTAMP"]

    @staticmethod
    def CI_CONCURRENT_ID() -> str:
        """
        Unique ID of build execution in a single executor.

        Added in GitLab all
        Available in GitLab Runner 11.10
        """
        return os.environ["CI_CONCURRENT_ID"]

    @staticmethod
    def CI_CONCURRENT_PROJECT_ID() -> str:
        """
        Unique ID of build execution in a single executor and project.

        Added in GitLab all
        Available in GitLab Runner 11.10
        """
        return os.environ["CI_CONCURRENT_PROJECT_ID"]

    @staticmethod
    def CI_CONFIG_PATH() -> str:
        """
        The path to CI configuration file. Defaults to .gitlab-ci.yml.

        Added in GitLab 9.4
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_CONFIG_PATH"]

    @staticmethod
    def CI_DEBUG_TRACE() -> str:
        """
        Whether debug logging (tracing) is enabled.

        Added in GitLab all
        Available in GitLab Runner 1.7
        """
        return os.environ["CI_DEBUG_TRACE"]

    @staticmethod
    def CI_DEFAULT_BRANCH() -> str:
        """
        The name of the default branch for the project.

        Added in GitLab 12.4
        Available in GitLab Runner all
        """
        return os.environ["CI_DEFAULT_BRANCH"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX() -> str:
        """
        The image prefix for pulling images through the Dependency Proxy.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_SERVER() -> str:
        """
        The server for logging in to the Dependency Proxy. This is equivalent to $CI_SERVER_HOST:$CI_SERVER_PORT.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPENDENCY_PROXY_SERVER"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_PASSWORD() -> str:
        """
        The password to use to pull images through the Dependency Proxy.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPENDENCY_PROXY_PASSWORD"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_USER() -> str:
        """
        The username to use to pull images through the Dependency Proxy.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPENDENCY_PROXY_USER"]

    @staticmethod
    def CI_DEPLOY_FREEZE() -> str:
        """
        Included with the value true if the pipeline runs during a deploy freeze window.

        Added in GitLab 13.2
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPLOY_FREEZE"]

    @staticmethod
    def CI_DEPLOY_PASSWORD() -> str:
        """
        Authentication password of the GitLab Deploy Token,
        only present if the Project has one related.

        Added in GitLab 10.8
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPLOY_PASSWORD"]

    @staticmethod
    def CI_DEPLOY_USER() -> str:
        """
        Authentication username of the GitLab Deploy Token,
        only present if the Project has one related.

        Added in GitLab 10.8
        Available in GitLab Runner all
        """
        return os.environ["CI_DEPLOY_USER"]

    @staticmethod
    def CI_DISPOSABLE_ENVIRONMENT() -> str:
        """
        Marks that the job is executed in a disposable environment
        (something that is created only for this job and disposed of/destroyed
        after the execution - all executors except shell and ssh).
        If the environment is disposable, it is set to true,
        otherwise it is not defined at all.

        Added in GitLab all
        Available in GitLab Runner 10.1
        """
        return os.environ["CI_DISPOSABLE_ENVIRONMENT"]

    @staticmethod
    def CI_ENVIRONMENT_NAME() -> str:
        """
        The name of the environment for this job.
        Only present if environment:name is set.

        Added in GitLab 8.15
        Available in GitLab Runner all
        """
        return os.environ["CI_ENVIRONMENT_NAME"]

    @staticmethod
    def CI_ENVIRONMENT_SLUG() -> str:
        """
        A simplified version of the environment name,
        suitable for inclusion in DNS, URLs, Kubernetes labels, and so on.
        Only present if environment:name is set.

        Added in GitLab 8.15
        Available in GitLab Runner all
        """
        return os.environ["CI_ENVIRONMENT_SLUG"]

    @staticmethod
    def CI_ENVIRONMENT_URL() -> str:
        """
        The URL of the environment for this job.
        Only present if environment:url is set.

        Added in GitLab 9.3
        Available in GitLab Runner all
        """
        return os.environ["CI_ENVIRONMENT_URL"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_IID() -> str:
        """
        Pull Request ID from GitHub if the pipelines are for
        external pull requests.
        Available only if only [external_pull_requests] or
        rules syntax is used and the pull request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_IID"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY() -> str:
        """
        The source repository name of the pull request if the pipelines are
        for external pull requests. Available only if only
        [external_pull_requests] or rules syntax is used and
        the pull request is open.

        Added in GitLab 13.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY() -> str:
        """
        The target repository name of the pull request if the pipelines
        are for external pull requests. Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 13.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME() -> str:
        """
        The source branch name of the pull request if the pipelines are for
        external pull requests. Available only if only [external_pull_requests]
        or rules syntax is used and the pull request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA() -> str:
        """
        The HEAD SHA of the source branch of the pull request if the pipelines
        are for external pull requests. Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME() -> str:
        """
        The target branch name of the pull request if the pipelines are for
        external pull requests. Available only if only [external_pull_requests]
        or rules syntax is used and the pull request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME"]

        """
    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA() -> str:
        """
        The HEAD SHA of the target branch of the pull request if the pipelines
        are for external pull requests. Available only if only
        [external_pull_requests] or rules syntax is used and the pull
        request is open.

        Added in GitLab 12.3
        Available in GitLab Runner all
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA"]

        """
    @staticmethod
    def CI_HAS_OPEN_REQUIREMENTS() -> str:
        """
        Included with the value true only if the pipeline’s project has any
        open requirements. Not included if there are no open requirements for
        the pipeline’s project.

        Added in GitLab 13.1
        Available in GitLab Runner all
        """
        return os.environ["CI_HAS_OPEN_REQUIREMENTS"]

    @staticmethod
    def CI_OPEN_MERGE_REQUESTS() -> str:
        """
        Available in branch and merge request pipelines. Contains a
        comma-separated list of up to four merge requests that use the current
        branch and project as the merge request source.
        For example gitlab-org/gitlab!333,gitlab-org/gitlab-foss!11.

        Added in GitLab 13.8
        Available in GitLab Runner all
        """
        return os.environ["CI_OPEN_MERGE_REQUESTS"]

    @staticmethod
    def CI_JOB_ID() -> str:
        """
        The unique ID of the current job that GitLab CI/CD uses internally.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_JOB_ID"]

    @staticmethod
    def CI_JOB_IMAGE() -> str:
        """
        The name of the image running the CI job.

        Added in GitLab 12.9
        Available in GitLab Runner 12.9
        """
        return os.environ["CI_JOB_IMAGE"]

    @staticmethod
    def CI_JOB_MANUAL() -> str:
        """
        The flag to indicate that job was manually started.

        Added in GitLab 8.12
        Available in GitLab Runner all
        """
        return os.environ["CI_JOB_MANUAL"]

    @staticmethod
    def CI_JOB_NAME() -> str:
        """
        The name of the job as defined in .gitlab-ci.yml.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_JOB_NAME"]

    @staticmethod
    def CI_JOB_STAGE() -> str:
        """
        The name of the stage as defined in .gitlab-ci.yml.

        Added in GitLab 9.0
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_JOB_STAGE"]

    @staticmethod
    def CI_JOB_STATUS() -> str:
        """
        The state of the job as each runner stage is executed.
        Use with after_script where CI_JOB_STATUS can be either success,
        failed or canceled.

        Added in GitLab all
        Available in GitLab Runner 13.5
        return os.environ["CI_JOB_STATUS"]

        """
    @staticmethod
    def CI_JOB_TOKEN() -> str:
        """
        Token used for authenticating with a few API endpoints and downloading
        dependent repositories. The token is valid as long as the job is running.

        Added in GitLab 9.0
        Available in GitLab Runner 1.2
        """
        return os.environ["CI_JOB_TOKEN"]

    @staticmethod
    def CI_JOB_JWT() -> str:
        """
        RS256 JSON web token that can be used for authenticating with third
        party systems that support JWT authentication, for example HashiCorp’s Vault.

        Added in GitLab 12.10
        Available in GitLab Runner all
        """
        return os.environ["CI_JOB_JWT"]

    @staticmethod
    def CI_JOB_URL() -> str:
        """
        Job details URL.

        Added in GitLab 11.1
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_JOB_URL"]

    @staticmethod
    def CI_KUBERNETES_ACTIVE() -> str:
        """
        Included with the value true only if the pipeline has a Kubernetes
        cluster available for deployments. Not included if no cluster is available.
        Can be used as an alternative to only:kubernetes/except:kubernetes
        with rules:if.

        Added in GitLab 13.0
        Available in GitLab Runner all
        """
        return os.environ["CI_KUBERNETES_ACTIVE"]

    @staticmethod
    def CI_MERGE_REQUEST_ASSIGNEES() -> str:
        """
        Comma-separated list of username(s) of assignee(s) for the merge request
        if the pipelines are for merge requests.
        Available only if only [merge_requests] or rules syntax is used and the
        merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_ASSIGNEES"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_ID() -> str:
        """
        The instance-level ID of the merge request. Only available if the
        pipelines are for merge requests and the merge request is created.
        This is a unique ID across all projects on GitLab.

        Added in GitLab 11.6
        Available in GitLab Runner all
        """
        return os.environ["CI_MERGE_REQUEST_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_IID() -> str:
        """
        The project-level IID (internal ID) of the merge request.
        Only available If the pipelines are for merge requests and the merge
        request is created. This ID is unique for the current project.

        Added in GitLab 11.6
        Available in GitLab Runner all
        """
        return os.environ["CI_MERGE_REQUEST_IID"]

    @staticmethod
    def CI_MERGE_REQUEST_LABELS() -> str:
        """
        Comma-separated label names of the merge request if the pipelines are
        for merge requests. Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_LABELS"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_MILESTONE() -> str:
        """
        The milestone title of the merge request if the pipelines are for merge
        requests. Available only if only [merge_requests] or rules syntax is
        used and the merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_MILESTONE"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_ID() -> str:
        """
        The ID of the project of the merge request if the pipelines are for
        merge requests. Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_PROJECT_ID"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_PATH() -> str:
        """
        The path of the project of the merge request if the pipelines are for
        merge requests (for example namespace/awesome-project). Available only
        if only [merge_requests] or rules syntax is used and the merge request
        is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_PROJECT_PATH"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_URL() -> str:
        """
        The URL of the project of the merge request if the pipelines are for
        merge requests (for example http://192.168.10.15:3000/namespace/awesome-project).
        Available only if only [merge_requests] or rules syntax is used and the merge
        request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_PROJECT_URL"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_REF_PATH() -> str:
        """
        The ref path of the merge request if the pipelines are for merge requests.
        (for example refs/merge-requests/1/head). Available only if only
        [merge_requests] or rules syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_REF_PATH"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_BRANCH_NAME() -> str:
        """
        The source branch name of the merge request if the pipelines are for
        merge requests. Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_BRANCH_SHA() -> str:
        """
        The HEAD SHA of the source branch of the merge request if the pipelines
        are for merge requests. Available only if only [merge_requests] or rules
        syntax is used, the merge request is created, and the pipeline is a
        merged result pipeline.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_SOURCE_BRANCH_SHA"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_ID() -> str:
        """
        The ID of the source project of the merge request if the pipelines are
        for merge requests. Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_ID"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_PATH() -> str:
        """
        The path of the source project of the merge request if the pipelines
        are for merge requests. Available only if only [merge_requests] or
        rules syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_PATH"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_URL() -> str:
        """
        The URL of the source project of the merge request if the pipelines are
        for merge requests. Available only if only [merge_requests] or rules
        syntax is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_URL"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_TARGET_BRANCH_NAME() -> str:
        """
        The target branch name of the merge request if the pipelines are for
        merge requests. Available only if only [merge_requests] or rules syntax
        is used and the merge request is created.

        Added in GitLab 11.6
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_TARGET_BRANCH_NAME"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_TARGET_BRANCH_SHA() -> str:
        """
        The HEAD SHA of the target branch of the merge request if the pipelines
        are for merge requests. Available only if only [merge_requests] or rules
        syntax is used, the merge request is created, and the pipeline is a merged
        result pipeline.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_TARGET_BRANCH_SHA"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_TITLE() -> str:
        """
        The title of the merge request if the pipelines are for merge requests.
        Available only if only [merge_requests] or rules syntax is used and the
        merge request is created.

        Added in GitLab 11.9
        Available in GitLab Runner all
        return os.environ["CI_MERGE_REQUEST_TITLE"]

        """
    @staticmethod
    def CI_MERGE_REQUEST_EVENT_TYPE() -> str:
        """
        The event type of the merge request, if the pipelines are for merge requests.
        Can be detached, merged_result or merge_train.

        Added in GitLab 12.3
        Available in GitLab Runner all
        """
        return os.environ["CI_MERGE_REQUEST_EVENT_TYPE"]

    @staticmethod
    def CI_MERGE_REQUEST_DIFF_ID() -> str:
        """
        The version of the merge request diff, if the pipelines are for merge requests.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_MERGE_REQUEST_DIFF_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_DIFF_BASE_SHA() -> str:
        """
        The base SHA of the merge request diff, if the pipelines are for merge requests.

        Added in GitLab 13.7
        Available in GitLab Runner all
        """
        return os.environ["CI_MERGE_REQUEST_DIFF_BASE_SHA"]

    @staticmethod
    def CI_NODE_INDEX() -> str:
        """
        Index of the job in the job set. If the job is not parallelized, this variable is not set.

        Added in GitLab 11.5
        Available in GitLab Runner all
        """
        return os.environ["CI_NODE_INDEX"]

    @staticmethod
    def CI_NODE_TOTAL() -> str:
        """
        Total number of instances of this job running in parallel. If the job is not parallelized, this variable is set to 1.

        Added in GitLab 11.5
        Available in GitLab Runner all
        """
        return os.environ["CI_NODE_TOTAL"]

    @staticmethod
    def CI_PAGES_DOMAIN() -> str:
        """
        The configured domain that hosts GitLab Pages.

        Added in GitLab 11.8
        Available in GitLab Runner all
        """
        return os.environ["CI_PAGES_DOMAIN"]

    @staticmethod
    def CI_PAGES_URL() -> str:
        """
        URL to GitLab Pages-built pages. Always belongs to a subdomain of CI_PAGES_DOMAIN.

        Added in GitLab 11.8
        Available in GitLab Runner all
        """
        return os.environ["CI_PAGES_URL"]

    @staticmethod
    def CI_PIPELINE_ID() -> str:
        """
        The instance-level ID of the current pipeline. This is a unique ID
        across all projects on GitLab.

        Added in GitLab 8.10
        Available in GitLab Runner all
        """
        return os.environ["CI_PIPELINE_ID"]

    @staticmethod
    def CI_PIPELINE_IID() -> str:
        """
        The project-level IID (internal ID) of the current pipeline.
        This ID is unique for the current project.

        Added in GitLab 11.0
        Available in GitLab Runner all
        """
        return os.environ["CI_PIPELINE_IID"]

    @staticmethod
    def CI_PIPELINE_SOURCE() -> str:
        """
        Indicates how the pipeline was triggered.
        Possible options are push, web, schedule, api, external, chat, webide,
        merge_request_event, external_pull_request_event, parent_pipeline,
        trigger, or pipeline.
        For pipelines created before GitLab 9.5, this is displayed as unknown.

        Added in GitLab 10.0
        Available in GitLab Runner all
        return os.environ["CI_PIPELINE_SOURCE"]

        """
    @staticmethod
    def CI_PIPELINE_TRIGGERED() -> str:
        """
        The flag to indicate that job was triggered.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_PIPELINE_TRIGGERED"]

    @staticmethod
    def CI_PIPELINE_URL() -> str:
        """
        Pipeline details URL.

        Added in GitLab 11.1
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PIPELINE_URL"]

    @staticmethod
    def CI_PROJECT_CONFIG_PATH() -> str:
        """
        The CI configuration path for the project.

        Added in GitLab 13.8
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_CONFIG_PATH"]

    @staticmethod
    def CI_PROJECT_DIR() -> str:
        """
        The full path where the repository is cloned and where the job is run.
        If the GitLab Runner builds_dir parameter is set, this variable is set
        relative to the value of builds_dir. For more information, see Advanced
        configuration for GitLab Runner.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_DIR"]

    @staticmethod
    def CI_PROJECT_ID() -> str:
        """
        The unique ID of the current project that GitLab CI/CD uses internally.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_ID"]

    @staticmethod
    def CI_PROJECT_NAME() -> str:
        """
        The name of the directory for the project that is being built.
        For example, if the project URL is gitlab.example.com/group-name/project-1,
        the CI_PROJECT_NAME would be project-1.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PROJECT_NAME"]

    @staticmethod
    def CI_PROJECT_NAMESPACE() -> str:
        """
        The project namespace (username or group name) that is being built.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PROJECT_NAMESPACE"]

    @staticmethod
    def CI_PROJECT_ROOT_NAMESPACE() -> str:
        """
        The root project namespace (username or group name) that is being built.
        For example, if CI_PROJECT_NAMESPACE is root-group/child-group/grandchild-group,
        CI_PROJECT_ROOT_NAMESPACE would be root-group.

        Added in GitLab 13.2
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PROJECT_ROOT_NAMESPACE"]

    @staticmethod
    def CI_PROJECT_PATH() -> str:
        """
        The namespace with project name.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PROJECT_PATH"]

    @staticmethod
    def CI_PROJECT_PATH_SLUG() -> str:
        """
        $CI_PROJECT_PATH in lowercase and with everything except 0-9 and a-z replaced with -. Use in URLs and domain names.

        Added in GitLab 9.3
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_PATH_SLUG"]

    @staticmethod
    def CI_PROJECT_REPOSITORY_LANGUAGES() -> str:
        """
        Comma-separated, lowercase list of the languages used in the repository (for example ruby,javascript,html,css).

        Added in GitLab 12.3
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_REPOSITORY_LANGUAGES"]

    @staticmethod
    def CI_PROJECT_TITLE() -> str:
        """
        The human-readable project name as displayed in the GitLab web interface.

        Added in GitLab 12.4
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_TITLE"]

    @staticmethod
    def CI_PROJECT_URL() -> str:
        """
        The HTTP(S) address to access project.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_PROJECT_URL"]

    @staticmethod
    def CI_PROJECT_VISIBILITY() -> str:
        """
        The project visibility (internal, private, public).

        Added in GitLab 10.3
        Available in GitLab Runner all
        """
        return os.environ["CI_PROJECT_VISIBILITY"]

    @staticmethod
    def CI_REGISTRY() -> str:
        """
        If the Container Registry is enabled it returns the address of the
        GitLab Container Registry. This variable includes a :port value if one
        has been specified in the registry configuration.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_REGISTRY"]

    @staticmethod
    def CI_REGISTRY_IMAGE() -> str:
        """
        If the Container Registry is enabled for the project it returns
        the address of the registry tied to the specific project.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_REGISTRY_IMAGE"]

    @staticmethod
    def CI_REGISTRY_PASSWORD() -> str:
        """
        The password to use to push containers to the GitLab Container Registry, for the current project.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_REGISTRY_PASSWORD"]

    @staticmethod
    def CI_REGISTRY_USER() -> str:
        """
        The username to use to push containers to the GitLab Container Registry, for the current project.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_REGISTRY_USER"]

    @staticmethod
    def CI_REPOSITORY_URL() -> str:
        """
        The URL to clone the Git repository.

        Added in GitLab 9.0
        Available in GitLab Runner all
        """
        return os.environ["CI_REPOSITORY_URL"]

    @staticmethod
    def CI_RUNNER_DESCRIPTION() -> str:
        """
        The description of the runner as saved in GitLab.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_RUNNER_DESCRIPTION"]

    @staticmethod
    def CI_RUNNER_EXECUTABLE_ARCH() -> str:
        """
        The OS/architecture of the GitLab Runner executable (note that this is not necessarily the same as the environment of the executor).

        Added in GitLab all
        Available in GitLab Runner 10.6
        """
        return os.environ["CI_RUNNER_EXECUTABLE_ARCH"]

    @staticmethod
    def CI_RUNNER_ID() -> str:
        """
        The unique ID of runner being used.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_RUNNER_ID"]

    @staticmethod
    def CI_RUNNER_REVISION() -> str:
        """
        GitLab Runner revision that is executing the current job.

        Added in GitLab all
        Available in GitLab Runner 10.6
        """
        return os.environ["CI_RUNNER_REVISION"]

    @staticmethod
    def CI_RUNNER_SHORT_TOKEN() -> str:
        """
        First eight characters of the runner’s token used to authenticate new job requests. Used as the runner’s unique ID.

        Added in GitLab all
        Available in GitLab Runner 12.3
        """
        return os.environ["CI_RUNNER_SHORT_TOKEN"]

    @staticmethod
    def CI_RUNNER_TAGS() -> str:
        """
        The defined runner tags.

        Added in GitLab 8.10
        Available in GitLab Runner 0.5
        """
        return os.environ["CI_RUNNER_TAGS"]

    @staticmethod
    def CI_RUNNER_VERSION() -> str:
        """
        GitLab Runner version that is executing the current job.

        Added in GitLab all
        Available in GitLab Runner 10.6
        """
        return os.environ["CI_RUNNER_VERSION"]

    @staticmethod
    def CI_SERVER() -> str:
        """
        Mark that job is executed in CI environment.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER"]

    @staticmethod
    def CI_SERVER_URL() -> str:
        """
        The base URL of the GitLab instance, including protocol and port (like https://gitlab.example.com:8080).

        Added in GitLab 12.7
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_URL"]

    @staticmethod
    def CI_SERVER_HOST() -> str:
        """
        Host component of the GitLab instance URL, without protocol and port (like gitlab.example.com).

        Added in GitLab 12.1
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_HOST"]

    @staticmethod
    def CI_SERVER_PORT() -> str:
        """
        Port component of the GitLab instance URL, without host and protocol (like 3000).

        Added in GitLab 12.8
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_PORT"]

    @staticmethod
    def CI_SERVER_PROTOCOL() -> str:
        """
        Protocol component of the GitLab instance URL, without host and port (like https).

        Added in GitLab 12.8
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_PROTOCOL"]

    @staticmethod
    def CI_SERVER_NAME() -> str:
        """
        The name of CI server that is used to coordinate jobs.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_NAME"]

    @staticmethod
    def CI_SERVER_REVISION() -> str:
        """
        GitLab revision that is used to schedule jobs.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_REVISION"]

    @staticmethod
    def CI_SERVER_VERSION() -> str:
        """
        GitLab version that is used to schedule jobs.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_VERSION"]

    @staticmethod
    def CI_SERVER_VERSION_MAJOR() -> str:
        """
        GitLab version major component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_VERSION_MAJOR"]

    @staticmethod
    def CI_SERVER_VERSION_MINOR() -> str:
        """
        GitLab version minor component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_VERSION_MINOR"]

    @staticmethod
    def CI_SERVER_VERSION_PATCH() -> str:
        """
        GitLab version patch component.

        Added in GitLab 11.4
        Available in GitLab Runner all
        """
        return os.environ["CI_SERVER_VERSION_PATCH"]

    @staticmethod
    def CI_SHARED_ENVIRONMENT() -> str:
        """
        Marks that the job is executed in a shared environment (something that
        is persisted across CI invocations like shell or ssh executor).
        If the environment is shared, it is set to true, otherwise it is not
        defined at all.

        Added in GitLab all
        Available in GitLab Runner 10.1
        """
        return os.environ["CI_SHARED_ENVIRONMENT"]

    @staticmethod
    def GITLAB_CI() -> str:
        """
        Mark that job is executed in GitLab CI/CD environment.

        Added in GitLab all
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_CI"]

    @staticmethod
    def GITLAB_FEATURES() -> str:
        """
        The comma separated list of licensed features available for your instance and plan.

        Added in GitLab 10.6
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_FEATURES"]

    @staticmethod
    def GITLAB_USER_EMAIL() -> str:
        """
        The email of the user who started the job.

        Added in GitLab 8.12
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_USER_EMAIL"]

    @staticmethod
    def GITLAB_USER_ID() -> str:
        """
        The ID of the user who started the job.

        Added in GitLab 8.12
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_USER_ID"]

    @staticmethod
    def GITLAB_USER_LOGIN() -> str:
        """
        The login username of the user who started the job.

        Added in GitLab 10.0
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_USER_LOGIN"]

    @staticmethod
    def GITLAB_USER_NAME() -> str:
        """
        The real name of the user who started the job.

        Added in GitLab 10.0
        Available in GitLab Runner all
        """
        return os.environ["GITLAB_USER_NAME"]

    @staticmethod
    def TRIGGER_PAYLOAD() -> str:
        """
        This variable is available when a pipeline is triggered with a webhook

        Added in GitLab 13.9
        Available in GitLab Runner all
        """
        return os.environ["TRIGGER_PAYLOAD"]
