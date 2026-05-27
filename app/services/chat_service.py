"""Chat orchestration — the heart of the RAG pipeline.

This class composes the building blocks. Routers should NEVER call retriever /
LLM / cache directly; they call ChatService.complete or .stream and let this
module enforce the pipeline order.
"""

# class ChatService:
#     def __init__(
#         self,
#         retriever: Retriever,
#         prompt_builder: PromptBuilder,
#         llm_client: LLMClient,
#         semantic_cache: SemanticCache,
#         guardrails: Guardrails,
#         conversation_store: ConversationStore,
#         settings: Settings,
#     ): ...
#
#     async def complete(
#         self,
#         request: ChatCompletionRequest,
#         user: AuthenticatedUser,
#         request_id: str,
#     ) -> ChatCompletionResponse:
#         """Non-streaming pipeline:
#
#             1. Resolve / create conversation_id; load short-term history.
#             2. guardrails.check_input(latest_user_message, user)
#                  -> if blocked: raise GuardrailViolation.
#                  -> if redacted: use redacted text downstream.
#             3. cache_key = semantic_cache.build_key(
#                   user.tenant_id, request.filters, redacted_question)
#                hit = await semantic_cache.get(cache_key, embedding=...)
#                if hit and hit.similarity >= threshold:
#                    return hit.response  # mark CacheStatus.SEMANTIC_HIT
#             4. docs = await retriever.search(
#                   query=redacted_question,
#                   user=user,
#                   top_k=request.top_k,
#                   filters=request.filters,
#                   conversation_history=history,    # optional query rewrite
#                )
#             5. prompt = prompt_builder.build(
#                   system_prompt=SYSTEM_PROMPT,
#                   documents=docs,
#                   history=history,
#                   question=redacted_question,
#                )
#                # PromptBuilder marks the system + docs blocks with
#                # cache_control={"type": "ephemeral"} so Anthropic prompt
#                # caching kicks in for repeat queries on the same corpus.
#             6. llm_response = await llm_client.complete(prompt, request)
#             7. guardrails.check_output(llm_response.text, docs_ids)
#                  -> if blocked: raise GuardrailViolation (or redact).
#             8. await semantic_cache.set(cache_key, response, ttl=...)
#             9. await conversation_store.append(conversation_id, ...)
#            10. Return ChatCompletionResponse w/ citations + usage + latency.
#         """
#         ...
#
#     async def stream(
#         self, request, user, request_id,
#     ) -> AsyncIterator[StreamEvent]:
#         """Same pipeline but yields:
#             - event: token   (text deltas)
#             - event: citations
#             - event: done
#         Output guardrails: buffer full text, run check on the final string
#         before the `done` event; or run streaming-safe checks on a sliding
#         window. If a guardrail fires mid-stream, send `event: error` and
#         truncate.
#         """
#         ...
#
#     async def get_conversation(self, conversation_id, user): ...
#     async def delete_conversation(self, conversation_id, user): ...
