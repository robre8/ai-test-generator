from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class CodeRequest(BaseModel):
    code: str

class StatusEnum(str, Enum):
    """Response status types"""
    success = "success"
    failed = "failed"
    validation_error = "validation_error"
    execution_error = "execution_error"
    timeout = "timeout"

class ErrorTypeEnum(str, Enum):
    """Error type classification"""
    test_failure = "TestFailure"
    code_invalid = "CodeInvalid"
    timeout = "Timeout"
    security_violation = "SecurityViolation"
    docker_error = "DockerError"
    unknown = "Unknown"

class TestResponse(BaseModel):
    status: StatusEnum  # success, failed, validation_error, execution_error, timeout
    generated_tests: str
    execution_output: str
    passed: bool
    execution_time: float  # Time in seconds
    error: Optional[str] = None
    error_type: Optional[ErrorTypeEnum] = None

class CodeValidationResponse(BaseModel):
    is_safe: bool
    error_message: Optional[str] = None
    dangerous_items: List[str] = []
    functions: List[str] = []
    classes: List[str] = []
    code_length: int

