from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError

from WeatherAgent import WeatherAgent

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WeatherAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue=event_queue, task_id=task.id, context_id=task.contextId)
        
        try:
            # async for item in self.agent.stream(query, task.contextId):
            #     is_task_complete = item['is_task_complete']
            #     require_user_input = item['require_user_input']

            async with WeatherAgent() as weather_agent:

                logger.info("calling weather_agent.invoke")
                result = await weather_agent.invoke(query=query, context_id=task.contextId)
                logger.info(f"weather_agent returned: {result}")
                is_task_complete = result['is_task_complete']
                require_user_input = result['require_user_input']

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            result['content'],
                            task.contextId,
                            task.id,
                        ),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            result['content'],
                            task.contextId,
                            task.id,
                        ),
                        final=True,
                    )
                else:
                    await updater.add_artifact(
                        [Part(root=TextPart(text=result['content']))],
                        name='conversion_result',
                    )
                    await updater.complete()

        except Exception as e:
            logger.error(f'An error occurred while streaming the response: {e}')
            raise ServerError(error=InternalError()) from e

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("Cancel not supported")
    