import time
from utils.better_logging import logger

from agent.workload import Workload
from agent.job_source import JobSource
from api.models import to_telemetry_attributes


class JobRunner:
    def __init__(self, source: JobSource, workload: Workload):
        self.source = source
        self.workload = workload

    async def run(self):
        while True:
            try:
                job = await self.source.get_next_job()
                if job:
                    result = None
                    try:
                        result = await self.workload.execute(job)
                        await self.source.handle_result(job, result)
                    except Exception as ex:
                        logger.error(f"Error processing job {job.job_id}", exc_info=ex)
                        await self.source.handle_job_failure(job, result, ex)

                else:
                    logger.info("No more jobs to process.")
                    break
            except Exception as ex:
                time.sleep(5)
                logger.warning("Failed to retrieve a job for processing, trying again...", exc_info=ex)
