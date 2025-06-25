import argparse
import asyncio
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)))

from agent.job_sources.local import LocalJobSource
from agent.runner import JobRunner
from agent.workload import Workload
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Run the challenge agent")
    parser.add_argument(
        "--enable-task-tracker",
        action="store_true",
        default=False,
        help="Enable TaskTracker",
    )
    parser.add_argument(
        "--no-op-workload",
        action="store_true",
        default=False,
        help="Use a no-op workload which simply echoes the job message.",
    )
    parser.add_argument(
        "--phase",
        choices=["phase1", "phase2"],
        required=False,
        default="phase1",
        help="Competition phase to control which defenses to use.",
    )
    return parser.parse_known_args()


async def main(enable_task_tracker: bool, no_op_workload: bool, unknown_args: list[str]):
    job_source = LocalJobSource(unknown_args)

    workload: Workload | None = None
    if no_op_workload:
        from agent.workloads.example import ExampleWorkload

        workload = ExampleWorkload(unknown_args)
    else:
        from agent.workloads.scenarios import GeneralWorkload

        workload = GeneralWorkload(task_tracker=enable_task_tracker)

    runner = JobRunner(job_source, workload)

    await runner.run()


if __name__ == "__main__":
    """
    Run the agent in local mode.

    For task-tracker agents, we will generally need to configure the dispatch queue name:

    > python ./src/agent --enable-task-tracker --phase phase1
    """
    args, unknown_args = parse_args()
    os.environ["COMPETITION_PHASE"] = args.phase

    # Run the agent
    asyncio.run(main(args.enable_task_tracker, args.no_op_workload, unknown_args))
