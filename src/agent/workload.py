from abc import ABC, abstractmethod
from api.models import JobMessage, JobResult


class Workload(ABC):
    def __init__(self, kind: str):
        self.kind = kind

    @abstractmethod
    async def execute(self, job: JobMessage) -> JobResult:
        pass
