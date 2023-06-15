from database.queries import plan, goal
from flask import abort, make_response


def read_all(plan_id):
    return list(goal.get_all(plan_id))


def create(request):
    name = request.get("name")
    description = request.get("description")
    plan_id = request.get("plan_id")

    id = goal.save(name, description, plan_id)
    plan.update_plan(plan_id, id, "goal_id")
    return request, 201


def read_one(goal_id):
    model = goal.get_one(goal_id)

    if model is not None:
        return model
    else:
        abort(404, f"Goal with ID {goal_id} not found")


def update(goal_id, request):
    try:
        name = request.get("name")
        description = request.get("description")
        goal.update(name, description, goal_id)
        return request, 201
    except AttributeError:
        abort(
            404,
            f"Goal with ID {goal_id} not found"
        )


def delete(goal_id):
    try:
        goal.delete(goal_id)
        return make_response(f"{goal_id} successfully deleted", 204)
    except AttributeError:
        abort(
            404,
            f"Goal with ID {goal_id} not found"
        )
