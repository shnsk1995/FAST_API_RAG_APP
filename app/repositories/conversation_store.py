"""Conversation history store (DynamoDB).

Table layout (`conversations`):
    PK: conversation_id
    SK: ts#<ulid>                     # one item per message
    Attrs: role, content, citations, usage, model, user_id, tenant_id

Sort key prefix lets us page through history in time order. Add a TTL
attribute for automatic purging based on retention policy.
"""

# class ConversationStore(Protocol):
#     async def create(self, user: AuthenticatedUser) -> str: ...   # returns conversation_id
#
#     async def append(
#         self, conversation_id: str, message: ChatMessage,
#         citations: list[Citation] | None = None,
#         usage: TokenUsage | None = None,
#     ) -> None: ...
#
#     async def get_recent(
#         self, conversation_id: str, max_messages: int = 20,
#     ) -> list[ChatMessage]: ...
#
#     async def delete(self, conversation_id: str, user: AuthenticatedUser) -> None: ...
#
#     async def assert_owner(self, conversation_id: str, user: AuthenticatedUser) -> None:
#         """Raise AuthorizationError unless user owns this conversation."""
#         ...
