from database.queries import plan
from flask import abort, make_response


def read_exercises():
    return list(plan.get_exercises())


def read_all():
    return list(plan.get_all())


def create(request):
    name = request.get("name")
    level = request.get("level")
    description = request.get("description")
    exercise_id = request.get("exercise_id")

    plan.save(name, level, description, exercise_id)
    return request, 201


def read_one(plan_id):
    model = plan.get_one(plan_id)

    if model is not None:
        return model
    else:
        abort(404, f"Plan with ID {plan_id} not found")


def update(plan_id, request):
    try:
        name = request.get("name")
        description = request.get("description")
        plan.update(name, description, plan_id)
        return request, 201
    except AttributeError:
        abort(
            404,
            f"Plan with ID {plan_id} not found"
        )


def delete(plan_id):
    try:
        plan.delete(plan_id)
        return make_response(f"{plan_id} successfully deleted", 204)
    except AttributeError:
        abort(
            404,
            f"Plan with ID {plan_id} not found"
        )
