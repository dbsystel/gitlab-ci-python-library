import os


class GitlabCiEnv():
    """
    Gitlab CI Environment variables.
    """
    @staticmethod
    def CHAT_CHANNEL() -> str:
        return os.environ["CHAT_CHANNEL"]

    @staticmethod
    def CHAT_INPUT() -> str:
        return os.environ["CHAT_INPUT"]

    @staticmethod
    def CI() -> str:
        return os.environ["CI"]

    @staticmethod
    def CI_API_V4_URL() -> str:
        return os.environ["CI_API_V4_URL"]

    @staticmethod
    def CI_BUILDS_DIR() -> str:
        return os.environ["CI_BUILDS_DIR"]

    @staticmethod
    def CI_COMMIT_BEFORE_SHA() -> str:
        return os.environ["CI_COMMIT_BEFORE_SHA"]

    @staticmethod
    def CI_COMMIT_DESCRIPTION() -> str:
        return os.environ["CI_COMMIT_DESCRIPTION"]

    @staticmethod
    def CI_COMMIT_MESSAGE() -> str:
        return os.environ["CI_COMMIT_MESSAGE"]

    @staticmethod
    def CI_COMMIT_REF_NAME() -> str:
        return os.environ["CI_COMMIT_REF_NAME"]

    @staticmethod
    def CI_COMMIT_REF_PROTECTED() -> str:
        return os.environ["CI_COMMIT_REF_PROTECTED"]

    @staticmethod
    def CI_COMMIT_REF_SLUG() -> str:
        return os.environ["CI_COMMIT_REF_SLUG"]

    @staticmethod
    def CI_COMMIT_SHA() -> str:
        return os.environ["CI_COMMIT_SHA"]

    @staticmethod
    def CI_COMMIT_SHORT_SHA() -> str:
        return os.environ["CI_COMMIT_SHORT_SHA"]

    @staticmethod
    def CI_COMMIT_BRANCH() -> str:
        return os.environ["CI_COMMIT_BRANCH"]

    @staticmethod
    def CI_COMMIT_TAG() -> str:
        return os.environ["CI_COMMIT_TAG"]

    @staticmethod
    def CI_COMMIT_TITLE() -> str:
        return os.environ["CI_COMMIT_TITLE"]

    @staticmethod
    def CI_COMMIT_TIMESTAMP() -> str:
        return os.environ["CI_COMMIT_TIMESTAMP"]

    @staticmethod
    def CI_CONCURRENT_ID() -> str:
        return os.environ["CI_CONCURRENT_ID"]

    @staticmethod
    def CI_CONCURRENT_PROJECT_ID() -> str:
        return os.environ["CI_CONCURRENT_PROJECT_ID"]

    @staticmethod
    def CI_CONFIG_PATH() -> str:
        return os.environ["CI_CONFIG_PATH"]

    @staticmethod
    def CI_DEBUG_TRACE() -> str:
        return os.environ["CI_DEBUG_TRACE"]

    @staticmethod
    def CI_DEFAULT_BRANCH() -> str:
        return os.environ["CI_DEFAULT_BRANCH"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX() -> str:
        return os.environ["CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_SERVER() -> str:
        return os.environ["CI_DEPENDENCY_PROXY_SERVER"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_PASSWORD() -> str:
        return os.environ["CI_DEPENDENCY_PROXY_PASSWORD"]

    @staticmethod
    def CI_DEPENDENCY_PROXY_USER() -> str:
        return os.environ["CI_DEPENDENCY_PROXY_USER"]

    @staticmethod
    def CI_DEPLOY_FREEZE() -> str:
        return os.environ["CI_DEPLOY_FREEZE"]

    @staticmethod
    def CI_DEPLOY_PASSWORD() -> str:
        return os.environ["CI_DEPLOY_PASSWORD"]

    @staticmethod
    def CI_DEPLOY_USER() -> str:
        return os.environ["CI_DEPLOY_USER"]

    @staticmethod
    def CI_DISPOSABLE_ENVIRONMENT() -> str:
        return os.environ["CI_DISPOSABLE_ENVIRONMENT"]

    @staticmethod
    def CI_ENVIRONMENT_NAME() -> str:
        return os.environ["CI_ENVIRONMENT_NAME"]

    @staticmethod
    def CI_ENVIRONMENT_SLUG() -> str:
        return os.environ["CI_ENVIRONMENT_SLUG"]

    @staticmethod
    def CI_ENVIRONMENT_URL() -> str:
        return os.environ["CI_ENVIRONMENT_URL"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_IID() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_IID"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME"]

    @staticmethod
    def CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA() -> str:
        return os.environ["CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA"]

    @staticmethod
    def CI_HAS_OPEN_REQUIREMENTS() -> str:
        return os.environ["CI_HAS_OPEN_REQUIREMENTS"]

    @staticmethod
    def CI_OPEN_MERGE_REQUESTS() -> str:
        return os.environ["CI_OPEN_MERGE_REQUESTS"]

    @staticmethod
    def CI_JOB_ID() -> str:
        return os.environ["CI_JOB_ID"]

    @staticmethod
    def CI_JOB_IMAGE() -> str:
        return os.environ["CI_JOB_IMAGE"]

    @staticmethod
    def CI_JOB_MANUAL() -> str:
        return os.environ["CI_JOB_MANUAL"]

    @staticmethod
    def CI_JOB_NAME() -> str:
        return os.environ["CI_JOB_NAME"]

    @staticmethod
    def CI_JOB_STAGE() -> str:
        return os.environ["CI_JOB_STAGE"]

    @staticmethod
    def CI_JOB_STATUS() -> str:
        return os.environ["CI_JOB_STATUS"]

    @staticmethod
    def CI_JOB_TOKEN() -> str:
        return os.environ["CI_JOB_TOKEN"]

    @staticmethod
    def CI_JOB_JWT() -> str:
        return os.environ["CI_JOB_JWT"]

    @staticmethod
    def CI_JOB_URL() -> str:
        return os.environ["CI_JOB_URL"]

    @staticmethod
    def CI_KUBERNETES_ACTIVE() -> str:
        return os.environ["CI_KUBERNETES_ACTIVE"]

    @staticmethod
    def CI_MERGE_REQUEST_ASSIGNEES() -> str:
        return os.environ["CI_MERGE_REQUEST_ASSIGNEES"]

    @staticmethod
    def CI_MERGE_REQUEST_ID() -> str:
        return os.environ["CI_MERGE_REQUEST_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_IID() -> str:
        return os.environ["CI_MERGE_REQUEST_IID"]

    @staticmethod
    def CI_MERGE_REQUEST_LABELS() -> str:
        return os.environ["CI_MERGE_REQUEST_LABELS"]

    @staticmethod
    def CI_MERGE_REQUEST_MILESTONE() -> str:
        return os.environ["CI_MERGE_REQUEST_MILESTONE"]

    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_ID() -> str:
        return os.environ["CI_MERGE_REQUEST_PROJECT_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_PATH() -> str:
        return os.environ["CI_MERGE_REQUEST_PROJECT_PATH"]

    @staticmethod
    def CI_MERGE_REQUEST_PROJECT_URL() -> str:
        return os.environ["CI_MERGE_REQUEST_PROJECT_URL"]

    @staticmethod
    def CI_MERGE_REQUEST_REF_PATH() -> str:
        return os.environ["CI_MERGE_REQUEST_REF_PATH"]

    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_BRANCH_NAME() -> str:
        return os.environ["CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"]

    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_BRANCH_SHA() -> str:
        return os.environ["CI_MERGE_REQUEST_SOURCE_BRANCH_SHA"]

    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_ID() -> str:
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_PATH() -> str:
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_PATH"]

    @staticmethod
    def CI_MERGE_REQUEST_SOURCE_PROJECT_URL() -> str:
        return os.environ["CI_MERGE_REQUEST_SOURCE_PROJECT_URL"]

    @staticmethod
    def CI_MERGE_REQUEST_TARGET_BRANCH_NAME() -> str:
        return os.environ["CI_MERGE_REQUEST_TARGET_BRANCH_NAME"]

    @staticmethod
    def CI_MERGE_REQUEST_TARGET_BRANCH_SHA() -> str:
        return os.environ["CI_MERGE_REQUEST_TARGET_BRANCH_SHA"]

    @staticmethod
    def CI_MERGE_REQUEST_TITLE() -> str:
        return os.environ["CI_MERGE_REQUEST_TITLE"]

    @staticmethod
    def CI_MERGE_REQUEST_EVENT_TYPE() -> str:
        return os.environ["CI_MERGE_REQUEST_EVENT_TYPE"]

    @staticmethod
    def CI_MERGE_REQUEST_DIFF_ID() -> str:
        return os.environ["CI_MERGE_REQUEST_DIFF_ID"]

    @staticmethod
    def CI_MERGE_REQUEST_DIFF_BASE_SHA() -> str:
        return os.environ["CI_MERGE_REQUEST_DIFF_BASE_SHA"]

    @staticmethod
    def CI_NODE_INDEX() -> str:
        return os.environ["CI_NODE_INDEX"]

    @staticmethod
    def CI_NODE_TOTAL() -> str:
        return os.environ["CI_NODE_TOTAL"]

    @staticmethod
    def CI_PAGES_DOMAIN() -> str:
        return os.environ["CI_PAGES_DOMAIN"]

    @staticmethod
    def CI_PAGES_URL() -> str:
        return os.environ["CI_PAGES_URL"]

    @staticmethod
    def CI_PIPELINE_ID() -> str:
        return os.environ["CI_PIPELINE_ID"]

    @staticmethod
    def CI_PIPELINE_IID() -> str:
        return os.environ["CI_PIPELINE_IID"]

    @staticmethod
    def CI_PIPELINE_SOURCE() -> str:
        return os.environ["CI_PIPELINE_SOURCE"]

    @staticmethod
    def CI_PIPELINE_TRIGGERED() -> str:
        return os.environ["CI_PIPELINE_TRIGGERED"]

    @staticmethod
    def CI_PIPELINE_URL() -> str:
        return os.environ["CI_PIPELINE_URL"]

    @staticmethod
    def CI_PROJECT_CONFIG_PATH() -> str:
        return os.environ["CI_PROJECT_CONFIG_PATH"]

    @staticmethod
    def CI_PROJECT_DIR() -> str:
        return os.environ["CI_PROJECT_DIR"]

    @staticmethod
    def CI_PROJECT_ID() -> str:
        return os.environ["CI_PROJECT_ID"]

    @staticmethod
    def CI_PROJECT_NAME() -> str:
        return os.environ["CI_PROJECT_NAME"]

    @staticmethod
    def CI_PROJECT_NAMESPACE() -> str:
        return os.environ["CI_PROJECT_NAMESPACE"]

    @staticmethod
    def CI_PROJECT_ROOT_NAMESPACE() -> str:
        return os.environ["CI_PROJECT_ROOT_NAMESPACE"]

    @staticmethod
    def CI_PROJECT_PATH() -> str:
        return os.environ["CI_PROJECT_PATH"]

    @staticmethod
    def CI_PROJECT_PATH_SLUG() -> str:
        return os.environ["CI_PROJECT_PATH_SLUG"]

    @staticmethod
    def CI_PROJECT_REPOSITORY_LANGUAGES() -> str:
        return os.environ["CI_PROJECT_REPOSITORY_LANGUAGES"]

    @staticmethod
    def CI_PROJECT_TITLE() -> str:
        return os.environ["CI_PROJECT_TITLE"]

    @staticmethod
    def CI_PROJECT_URL() -> str:
        return os.environ["CI_PROJECT_URL"]

    @staticmethod
    def CI_PROJECT_VISIBILITY() -> str:
        return os.environ["CI_PROJECT_VISIBILITY"]

    @staticmethod
    def CI_REGISTRY() -> str:
        return os.environ["CI_REGISTRY"]

    @staticmethod
    def CI_REGISTRY_IMAGE() -> str:
        return os.environ["CI_REGISTRY_IMAGE"]

    @staticmethod
    def CI_REGISTRY_PASSWORD() -> str:
        return os.environ["CI_REGISTRY_PASSWORD"]

    @staticmethod
    def CI_REGISTRY_USER() -> str:
        return os.environ["CI_REGISTRY_USER"]

    @staticmethod
    def CI_REPOSITORY_URL() -> str:
        return os.environ["CI_REPOSITORY_URL"]

    @staticmethod
    def CI_RUNNER_DESCRIPTION() -> str:
        return os.environ["CI_RUNNER_DESCRIPTION"]

    @staticmethod
    def CI_RUNNER_EXECUTABLE_ARCH() -> str:
        return os.environ["CI_RUNNER_EXECUTABLE_ARCH"]

    @staticmethod
    def CI_RUNNER_ID() -> str:
        return os.environ["CI_RUNNER_ID"]

    @staticmethod
    def CI_RUNNER_REVISION() -> str:
        return os.environ["CI_RUNNER_REVISION"]

    @staticmethod
    def CI_RUNNER_SHORT_TOKEN() -> str:
        return os.environ["CI_RUNNER_SHORT_TOKEN"]

    @staticmethod
    def CI_RUNNER_TAGS() -> str:
        return os.environ["CI_RUNNER_TAGS"]

    @staticmethod
    def CI_RUNNER_VERSION() -> str:
        return os.environ["CI_RUNNER_VERSION"]

    @staticmethod
    def CI_SERVER() -> str:
        return os.environ["CI_SERVER"]

    @staticmethod
    def CI_SERVER_URL() -> str:
        return os.environ["CI_SERVER_URL"]

    @staticmethod
    def CI_SERVER_HOST() -> str:
        return os.environ["CI_SERVER_HOST"]

    @staticmethod
    def CI_SERVER_PORT() -> str:
        return os.environ["CI_SERVER_PORT"]

    @staticmethod
    def CI_SERVER_PROTOCOL() -> str:
        return os.environ["CI_SERVER_PROTOCOL"]

    @staticmethod
    def CI_SERVER_NAME() -> str:
        return os.environ["CI_SERVER_NAME"]

    @staticmethod
    def CI_SERVER_REVISION() -> str:
        return os.environ["CI_SERVER_REVISION"]

    @staticmethod
    def CI_SERVER_VERSION() -> str:
        return os.environ["CI_SERVER_VERSION"]

    @staticmethod
    def CI_SERVER_VERSION_MAJOR() -> str:
        return os.environ["CI_SERVER_VERSION_MAJOR"]

    @staticmethod
    def CI_SERVER_VERSION_MINOR() -> str:
        return os.environ["CI_SERVER_VERSION_MINOR"]

    @staticmethod
    def CI_SERVER_VERSION_PATCH() -> str:
        return os.environ["CI_SERVER_VERSION_PATCH"]

    @staticmethod
    def CI_SHARED_ENVIRONMENT() -> str:
        return os.environ["CI_SHARED_ENVIRONMENT"]

    @staticmethod
    def GITLAB_CI() -> str:
        return os.environ["GITLAB_CI"]

    @staticmethod
    def GITLAB_FEATURES() -> str:
        return os.environ["GITLAB_FEATURES"]

    @staticmethod
    def GITLAB_USER_EMAIL() -> str:
        return os.environ["GITLAB_USER_EMAIL"]

    @staticmethod
    def GITLAB_USER_ID() -> str:
        return os.environ["GITLAB_USER_ID"]

    @staticmethod
    def GITLAB_USER_LOGIN() -> str:
        return os.environ["GITLAB_USER_LOGIN"]

    @staticmethod
    def GITLAB_USER_NAME() -> str:
        return os.environ["GITLAB_USER_NAME"]

    @staticmethod
    def TRIGGER_PAYLOAD() -> str:
        return os.environ["TRIGGER_PAYLOAD"]
