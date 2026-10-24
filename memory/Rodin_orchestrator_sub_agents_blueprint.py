# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Loop agent implementation."""

from __future__ import annotations

import logging
from typing import AsyncGenerator
from typing import ClassVar
from typing import Optional
import warnings

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any
from typing_extensions import deprecated
from typing_extensions import override

try:
  from google.adk.events.event import Event  # type: ignore
  from google.adk.features import experimental, FeatureName  # type: ignore
  from google.adk.utils.context_utils import Aclosing  # type: ignore
  from google.adk.agents.base_agent import BaseAgent, BaseAgentState  # type: ignore
  from google.adk.agents.base_agent_config import BaseAgentConfig  # type: ignore
  from google.adk.agents.invocation_context import InvocationContext  # type: ignore
  from google.adk.agents.loop_agent_config import LoopAgentConfig  # type: ignore
except ImportError:
  class FeatureName:
    AGENT_STATE = "AGENT_STATE"

  def experimental(_feature: Any):
    def _decorator(cls_or_fn: Any) -> Any:
      return cls_or_fn
    return _decorator

  @dataclass
  class _EventActions:
    escalate: bool = False

  @dataclass
  class Event:
    author: str = "rodin_loop_agent"
    actions: _EventActions = field(default_factory=_EventActions)
    payload: dict[str, Any] = field(default_factory=dict)

  @asynccontextmanager
  async def Aclosing(agen: Any):
    try:
      yield agen
    finally:
      if hasattr(agen, "aclose"):
        await agen.aclose()

  class BaseAgentState:
    def __init__(self, **kwargs: Any) -> None:
      for k, v in kwargs.items():
        setattr(self, k, v)

  class BaseAgentConfig:
    pass

  class LoopAgentConfig(BaseAgentConfig):
    pass

  @dataclass
  class InvocationContext:
    is_resumable: bool = False
    agent_states: dict[str, Any] = field(default_factory=dict)

    def set_agent_state(self, name: str, agent_state: Any = None, end_of_agent: bool = False) -> None:
      self.agent_states[name] = {"state": agent_state, "end_of_agent": end_of_agent}

    def should_pause_invocation(self, _event: Event) -> bool:
      return False

    def reset_sub_agent_states(self, _name: str) -> None:
      pass

  class BaseAgent:
    def __init__(self, name: str = "rodin_loop_agent", sub_agents: Optional[list[Any]] = None, max_iterations: Optional[int] = 3):
      self.name = name
      self.sub_agents = sub_agents or []
      self.max_iterations = max_iterations

    def _load_agent_state(self, ctx: InvocationContext, _cls: Any) -> Any:
      entry = ctx.agent_states.get(self.name)
      return entry.get("state") if isinstance(entry, dict) else None

    def _create_agent_state_event(self, _ctx: InvocationContext) -> Event:
      return Event(author=self.name)

logger = logging.getLogger('google_adk.' + __name__)


@experimental(FeatureName.AGENT_STATE)
class LoopAgentState(BaseAgentState):
  """State for LoopAgent."""

  current_sub_agent: str = ''
  """The name of the current sub-agent to run in the loop."""

  times_looped: int = 0
  """The number of times the loop agent has looped."""


@deprecated(
    'LoopAgent is deprecated in favor of Workflow and will be removed in a'
    ' future version. Workflow cannot yet be used as an LlmAgent sub-agent.'
)
class LoopAgent(BaseAgent):
  """A shell agent that run its sub-agents in a loop.

  When sub-agent generates an event with escalate or max_iterations are
  reached, the loop agent will stop.

  .. deprecated::
    LoopAgent is deprecated in favor of Workflow and will be removed in a
    future version. Workflow cannot yet be used as an LlmAgent sub-agent.
  """

  config_type: ClassVar[type[BaseAgentConfig]] = LoopAgentConfig
  """The config type for this agent.

  DEPRECATED: This attribute is deprecated and will be removed in a future
  version, along with the AgentConfig YAML loader.
  """

  max_iterations: Optional[int] = None
  """The maximum number of iterations to run the loop agent.

  If not set, the loop agent will run indefinitely until a sub-agent
  escalates. A value of zero or less runs the sub-agents no times at all.
  """

  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    if not self.sub_agents:
      return

    agent_state = self._load_agent_state(ctx, LoopAgentState)
    is_resuming_at_current_agent = agent_state is not None
    times_looped, start_index = self._get_start_state(agent_state)

    should_exit = False
    pause_invocation = False
    while (
        self.max_iterations is None or times_looped < self.max_iterations
    ) and not (should_exit or pause_invocation):
      for i in range(start_index, len(self.sub_agents)):
        sub_agent = self.sub_agents[i]

        if ctx.is_resumable and not is_resuming_at_current_agent:
          # If we are resuming from the current event, it means the same event
          # has already been logged, so we should avoid yielding it again.
          agent_state = LoopAgentState(
              current_sub_agent=sub_agent.name,
              times_looped=times_looped,
          )
          ctx.set_agent_state(self.name, agent_state=agent_state)
          yield self._create_agent_state_event(ctx)

        is_resuming_at_current_agent = False

        async with Aclosing(sub_agent.run_async(ctx)) as agen:
          async for event in agen:
            yield event
            if event.actions.escalate:
              should_exit = True
            if ctx.should_pause_invocation(event):
              pause_invocation = True

        if should_exit or pause_invocation:
          break  # break inner for loop

      if not pause_invocation:
        # Restart from the beginning of the loop.
        start_index = 0
        times_looped += 1
        # Reset the state of all sub-agents in the loop.
        ctx.reset_sub_agent_states(self.name)

    # If the invocation is paused, we should not yield the end of agent event.
    if pause_invocation:
      return

    if ctx.is_resumable:
      ctx.set_agent_state(self.name, end_of_agent=True)
      yield self._create_agent_state_event(ctx)

  def _get_start_state(
      self,
      agent_state: Optional[LoopAgentState],
  ) -> tuple[int, int]:
    """Computes the start state of the loop agent from the agent state."""
    if not agent_state:
      return 0, 0

    times_looped = agent_state.times_looped
    start_index = 0
    if agent_state.current_sub_agent:
      try:
        sub_agent_names = [sub_agent.name for sub_agent in self.sub_agents]
        start_index = sub_agent_names.index(agent_state.current_sub_agent)
      except ValueError:
        # A sub-agent was removed so the agent name is not found.
        # For now, we restart from the beginning.
        logger.warning(
            'Sub-agent %s was not found. Restarting from the beginning.',
            agent_state.current_sub_agent,
        )
    return times_looped, start_index

  @override
  async def _run_live_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    raise NotImplementedError('This is not supported yet for LoopAgent.')
    yield  # AsyncGenerator requires having at least one yield statement