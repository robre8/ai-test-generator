from fastapi import APIRouter
from ..schemas.test_schema import CodeRequest, TestResponse, CodeValidationResponse
from ..services.test_generation_service import process_code
from ..services.code_validator import get_safe_code_info

router = APIRouter()

@router.post("/generate-tests", response_model=TestResponse)
def generate_tests(request: CodeRequest):
    """Generate and execute tests for provided code"""
    result = process_code(request.code)
    return result

@router.post("/validate-code", response_model=CodeValidationResponse)
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
