from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message
from pydantic import BaseModel

class GreetingRequest(BaseModel):
    """A simple request model for greeting."""
    async def invoke(self) -> str:
        return "Hello! This is a greeting from the agent."
    
class GreetingAgentExecutor(AgentExecutor):
    """Agent executor for handling greeting requests."""

    def __init__(self):
        self.agent = GreetingRequest()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        """Execute the greeting request and send a message to the event queue."""
        greeting_message = await self.agent.invoke()
        event_queue.enqueue_event(new_agent_text_message(greeting_message))
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise NotImplementedError("Cancellation is not implemented for GreetingAgentExecutor.")