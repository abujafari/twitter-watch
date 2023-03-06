from rest_framework.response import Response


def make_response(message, status):
    return Response({
        "message": message
    }, status=status)


def bad_request_response(message="Bad request"):
    return make_response(message, 400)


def not_found_response(message="Not found"):
    return make_response(message, 404)


def service_unavailable_response(message="Service is unavailable"):
    return make_response(message, 503)
