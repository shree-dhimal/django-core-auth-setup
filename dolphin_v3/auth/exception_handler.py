from rest_framework.views import exception_handler
from rest_framework import status

def api_exception_handler(exc, context):
    """
    Custom exception handler for DRF to return uniform responses.
    """
    response = exception_handler(exc, context)

    # If DRF handled it, format response
    if response is not None:
        data = {
            "success": False,
            "status_code": response.status_code,
            "errors": response.data,
        }
        response.data = data
        return response

    # If DRF did not handle it (unexpected errors)
    from rest_framework.response import Response
    return Response(
        {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "errors": str(exc)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )