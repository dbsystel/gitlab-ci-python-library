import yaml
import copy


class Job():
    def __init__(
        self,
        *args,
        name: str,
        script: [str],
        variables: dict = {},
        namespace: str = None,
    ):
        self._name = name
        self._namespace = namespace
        self._variables = variables

        if type(script) == str:
            self._script = [script]
        elif type(script) == list:
            self._script = script
        else:
            raise AttributeError(
                "script parameter must be of type string or list of strings")

    @property
    def fqdn(self):
        return self._name + (f"_{self._namespace}"
                             if self._namespace is not None else "")

    def prepend_script(self, script: str):
        self._script.insert(0, script)

    def append_script(self, script: str):
        self._script.append(script)

    def add_variables(self, variables: dict):
        self._variables = {**self._variables, **variables}

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += namespace

    def copy(self, namespace: str = None):
        if self._namespace is None and namespace is None:
            target_namespace = None
        elif self._namespace is None:
            target_namespace = namespace
        elif namespace is None:
            target_namespace = self._namespace
        else:
            target_namespace = f"{self._namespace}_{namespace}"

        return Job(
            name=self._name,
            script=copy.deepcopy(self._script),
            variables=copy.deepcopy(self._variables),
            namespace=target_namespace,
        )

    def render(self):
        return {
            "script": self._script,
            "variables": self._variables,
        }


class JobSequence():
    def __init__(self, *args, namespace: str = None):
        self._jobs = []
        self._namespace = namespace
        self._prepend_scripts = []
        self._append_scripts = []

    def add_job(self, job: Job, *args, namespace: str = None):
        job.add_namespace(namespace)
        self._jobs.append(job)

    def add_sequence(self, job_sequence, *args, namespace: str = None):
        job_sequence.add_namespace(namespace)
        self._jobs.append(job_sequence)

    def prepend_script(self, script: str):
        self._prepend_scripts.append(script)

    def append_script(self, script: str):
        self._append_scripts.append(script)

    def add_namespace(self, namespace: str):
        if namespace is None:
            return
        if self._namespace is None:
            self._namespace = namespace
        else:
            self._namespace += namespace

    @property
    def populated_jobs(self) -> list:
        all_jobs = []
        for job in self._jobs:
            if type(job) == JobSequence:
                all_jobs += job.populated_jobs
            elif type(job) == Job:
                all_jobs.append(job.copy(self._namespace))

        for job in all_jobs:
            for script in self._prepend_scripts:
                job.prepend_script(script)
            for script in self._append_scripts:
                job.append_script(script)

        return all_jobs

    @property
    def jobs(self) -> list:
        return self._jobs


class Pipeline(JobSequence):
    def __init__(
        self,
        *args,
        variables: dict = None,
        before_script: list = None,
        namespace: str = None,
    ):
        super().__init__(namespace)

        self._pipeline = {}
        if variables is not None:
            self._pipeline["variables"] = variables
        if before_script is not None:
            self._pipeline["before_script"] = before_script

    def render(self):
        stages = {}
        job_copies = self.populated_jobs
        for job in job_copies:
            # use the keys of dictionary as ordered set
            stages[job.fqdn] = None
        pipe_copy = copy.deepcopy(self._pipeline)
        pipe_copy["stages"] = list(stages.keys())
        for job in job_copies:
            rendered_job = job.render()
            rendered_job["stage"] = job.fqdn
            pipe_copy[job.fqdn] = rendered_job
        return pipe_copy

    def print_yaml(self):
        print(
            yaml.dump(self.render(), default_flow_style=False,
                      sort_keys=False))
