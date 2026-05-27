"""Domain exceptions and FastAPI exception handlers.

Goals:
- Map every internal exception to a consistent JSON error envelope
  { "error": { "code": "...", "message": "...", "request_id": "..." } }.
- Never leak stack traces or internal identifiers to clients.
- Emit structured logs + metrics for every error.
"""

# Define exception classes (raise these from services / routers):
#
# class AppError(Exception):                      # base
#     status_code: int = 500
#     code: str = "internal_error"
#
# class AuthenticationError(AppError): 401 / "unauthenticated"
# class AuthorizationError(AppError):  403 / "forbidden"
# class ValidationAppError(AppError):  422 / "invalid_request"
# class GuardrailViolation(AppError):  400 / "guardrail_blocked"
#     # carries `category` (pii | injection | toxicity | policy)
# class RateLimitExceeded(AppError):   429 / "rate_limited"
# class UpstreamLLMError(AppError):    502 / "llm_unavailable"
# class VectorStoreError(AppError):    503 / "retrieval_failed"
# class IngestionError(AppError):      500 / "ingestion_failed"
# class NotFoundError(AppError):       404 / "not_found"


def register_exception_handlers(app):
    """Attach handlers for AppError, RequestValidationError, HTTPException, Exception.

    Each handler should:
    - Build the standard error envelope.
    - Pull request_id from contextvars (set by RequestContextMiddleware).
    - Log with structlog including user_id, tenant_id, route, exc_info for 5xx.
    - Emit a CloudWatch metric (errors_total{code=...}).
    """
    ...
