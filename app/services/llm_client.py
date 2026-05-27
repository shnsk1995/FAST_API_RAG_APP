"""Thin Anthropic wrapper.

Responsibilities:
- Hold the single anthropic.AsyncAnthropic instance (constructed once per
  Lambda container, key loaded from Secrets Manager at cold start).
- Centralise retries + circuit breaker (tenacity): retry on 429/5xx with
  exponential backoff + jitter; surface UpstreamLLMError after exhaustion.
- Translate Anthropic responses into our domain types.
- Record token usage including prompt-cache hit/miss fields.
"""

# class LLMClient:
#     def __init__(self, anthropic_client, settings): ...
#
#     async def complete(self, request: AnthropicMessagesRequest) -> LLMResponse:
#         """Single shot. Returns text + usage + stop_reason.
#         - Pass system blocks with cache_control through verbatim.
#         - Read response.usage.cache_read_input_tokens for observability.
#         """
#         ...
#
#     async def stream(self, request: AnthropicMessagesRequest) -> AsyncIterator[LLMStreamEvent]:
#         """Yield text deltas + final usage.
#         - Use client.messages.stream context manager.
#         - Re-raise transient errors as UpstreamLLMError after retries.
#         """
#         ...
#
# class LLMResponse(BaseModel):
#     text: str
#     usage: TokenUsage
#     stop_reason: str
#     model: str
