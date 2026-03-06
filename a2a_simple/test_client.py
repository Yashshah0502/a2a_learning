import uuid
import asyncio
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    TextPart,
)

PUBLIC_AGENT_CARD_PATH = "/.well-known/agent.json"
BASE_URL = "http://localhost:9999"

async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            base_url=BASE_URL,
            httpx_client=httpx_client
        )

        final_agent_card_to_use = None
        try:
            print(f"Resolving agent card from {BASE_URL}{PUBLIC_AGENT_CARD_PATH}...")
            final_card = await resolver.get_agent_card()
            print("fetched the card")
            final_agent_card_to_use = final_card
        except Exception as e:
            print(f"Failed to resolve agent card: {e}")
            raise RuntimeError("Failed to fetch public agent card")

        client = A2AClient(agent_card=final_agent_card_to_use,
                           httpx_client=httpx_client)
        print("Client initilized!!")

        message_payload = Message(
            role=Role.user,
            messageId=str(uuid.uuid4()),
            parts=[Part(root=TextPart(text="Hello, how are you?"))],
        )
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message=message_payload,
            ),
        )
        print("Sending message")

        response = await client.send_message(request)
        print("Response:")
        print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
