import httpx
from pydantic import BaseModel

class MessageRequest(BaseModel):
    content: str
    customer_id: str

class MessageResponse(BaseModel):
    content: str

class AgentClientError(Exception):
    pass

class AgentClient:
    """Client for interacting with the agent API."""
    
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        
    async def ainvoke(
        self, 
        content: str, 
        customer_id: str
    ) -> MessageResponse:
        """
        Invoke the agent asynchronously.
        
        Args:
            content (str): The message content to send
            customer_id (str): The customer identifier for memory/thread tracking
            
        Returns:
            MessageResponse: The response from the agent containing the message content
            
        Raises:
            AgentClientError: If there is an error communicating with the API
        """
        request = MessageRequest(
            content=content,
            customer_id=customer_id
        )
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/sales/chat",
                    json=request.model_dump(),
                    timeout=30
                )
                response.raise_for_status()
                return MessageResponse(**response.json())
                
            except httpx.HTTPError as e:
                raise AgentClientError(f"Error communicating with agent API: {e}")

#test
# Example usage:
# async def main():
#     client = AgentClient("http://127.0.0.1:8000")
#     response = await client.ainvoke(
#         content="what is my name",
#         customer_id="holaAmisdfgo"
#     )
#     print("look", response.content)  # Access the response content


# import asyncio

# asyncio.run(main())