import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import GreetingAgentExecutor


def main():
    #Will define the skills of the agent
    skills = AgentSkill(
        id="greeting_skill",
        name="Greeting Skill",
        description="A skill that allows the agent to greet users.",
        tags=["greeting", "communication"],
        examples=["Hello!", "Hi there!", "Greetings!"]
    )

    # will make the card for the agent
    card = AgentCard(
        id="greeting_agent",
        name="Greeting Agent",
        description="An agent that can greet users.",
        url="http://localhost:9999/",
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[skills],
        version="1.0.0",
        capabilities=AgentCapabilities()  
    )

    #define the request handler for the agent
    req_handler = DefaultRequestHandler(
        GreetingAgentExecutor(), 
        InMemoryTaskStore()
        )

    # Wil create the server
    server = A2AStarletteApplication(
        agent_card=card,
        http_handler=req_handler
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=9999)

if __name__ == "__main__":    
    main()
