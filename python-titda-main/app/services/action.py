from database.queries import action
from flask import abort, make_response


def read_all(plan_id):
    return list(action.get_all(plan_id))


def create(request):
    name = request.get("name")
    description = request.get("description")
    type = request.get("type")
    value = request.get("value")
    plan_id = request.get("plan_id")
    procedural_memory_id = request.get("procedural_memory_id")

    action.save(name, description, type, value, plan_id, procedural_memory_id)
    return request, 201


def read_one(action_id):
    model = action.get_one(action_id)

    if model is not None:
        return model
    else:
        abort(404, f"Action with ID {action_id} not found")


def update(action_id, request):
    try:
        name = request.get("name")
        description = request.get("description")
        type = request.get("type")
        value = request.get("value")
        request.update(name, description, type, value, action_id)
        return request, 201
    except AttributeError:
        abort(
            404,
            f"Action with ID {action_id} not found"
        )


def delete(action_id):
    try:
        action.delete(action_id)
        return make_response(f"{action_id} successfully deleted", 204)
    except AttributeError:
        abort(
            404,
            f"Plan with ID {action_id} not found"
        )
