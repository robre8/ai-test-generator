from fastapi import APIRouter
from ..schemas.test_schema import CodeRequest, TestResponse, CodeValidationResponse
from ..services.test_generation_service import process_code
from ..services.code_validator import get_safe_code_info

router = APIRouter()

@router.post(
    "/generate-tests",
    response_model=TestResponse,
    summary="Generate and execute tests",
    description="Generate pytest tests from the provided code and execute them in the sandbox.",
    tags=["tests"],
)
def generate_tests(request: CodeRequest):
    """Generate and execute tests for provided code"""
    result = process_code(request.code)
    return result

@router.post(
    "/validate-code",
    response_model=CodeValidationResponse,
    summary="Validate code safety",
    description="Analyze code for unsafe operations without executing tests.",
    tags=["validation"],
)
def validate_code(request: CodeRequest):
    """Check if code is safe to execute (without running tests)"""
    info = get_safe_code_info(request.code)
    return CodeValidationResponse(
        is_safe=info["is_safe"],
        error_message=info["error_message"],
        dangerous_items=info["dangerous_items"],
        functions=info["functions"],
        classes=info["classes"],
        code_length=info["code_length"]
    )
