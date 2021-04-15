import pytest

from gcip import (
    Job,
    Rule,
    Cache,
    WhenStatement,
    PredefinedVariables,
)


@pytest.fixture(scope="module")
def rule():
    rule = Rule(
        if_statement=f"{PredefinedVariables.CI_COMMIT_REF_NAME} == main",
        when=WhenStatement.ALWAYS,
        allow_failure=True,
    )
    return rule


@pytest.fixture
def job(rule):
    job = Job(script="date", namespace="fixture_stage", name="job_name")
    job.append_scripts(f'echo "You are running on branch: ${PredefinedVariables.CI_COMMIT_REF_NAME}"')
    job.set_image("busybox")
    job.set_cache(Cache(paths=["path/to/cache/"]))
    job.append_rules(rule)
    job.prepend_rules(Rule(if_statement='echo "I am prepended" || true'))
    job.add_artifacts_paths("custom/path/to/artifact.txt")
    job.add_tags("custom", "docker")
    job.add_variables(
        ENV_VAR="Hello",
        CUSTOM="World",
    )
    job.add_needs(Job(script=f"echo I am needed by {job.name}", namespace="needs", name="needs_job"))
    return job


def test_job_properties(job):
    assert job.name == "fixture-stage-job-name"
    assert job.stage == "fixture_stage"
    assert job.image.name == "busybox"
    assert job.variables == {"ENV_VAR": "Hello", "CUSTOM": "World"}
    assert job.tags == {"custom": None, "docker": None}
    assert job.rules[0].render() == {"allow_failure": False, "if": 'echo "I am prepended" || true', "when": "on_success"}
    assert job.needs[0].name == "needs-needs-job"
    assert job.scripts[0] == "date"
    assert job.artifacts_paths["custom/path/to/artifact.txt"] is None
    assert job.cache.paths[0] == "./path/to/cache/"


def test_job_exceptions():
    with pytest.raises(ValueError):
        Job(script="Neither name nor namespace")
    with pytest.raises(AttributeError):
        Job(script={"Wrong": "Attribute, Type"}, name="test_script_attribute_exception")  # type: ignore
