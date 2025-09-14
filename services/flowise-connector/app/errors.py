from dataclasses import dataclass


@dataclass
class AgentUpstreamError(Exception):
    status: int
    detail: str
    upstream: str


@dataclass
class WorkflowTriggerError(Exception):
    status: int
    detail: str
    upstream: str
