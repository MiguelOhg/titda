from database.queries import plan, discrepancy
from flask import abort, make_response


def read_all(plan_id):
    return list(discrepancy.get_all(plan_id))


def create(request):
    description = request.get("description")
    plan_id = request.get("plan_id")

    id = discrepancy.save(description, plan_id)
    plan.update_plan(plan_id, id, "discrepancy_id")
    return request, 201


def read_one(discrepancy_id):
    model = discrepancy.get_one(discrepancy_id)

    if model is not None:
        return model
    else:
        abort(404, f"Discrepancy with ID {discrepancy_id} not found")


def update(discrepancy_id, request):
    try:
        description = request.get("description")
        discrepancy.update(description, discrepancy_id)
        return request, 201
    except AttributeError:
        abort(
            404,
            f"Discrepancy with ID {discrepancy_id} not found"
        )


def delete(discrepancy_id):
    try:
        discrepancy_id.delete(discrepancy_id)
        return make_response(f"{discrepancy_id} successfully deleted", 204)
    except AttributeError:
        abort(
            404,
            f"Discrepancy with ID {discrepancy_id} not found"
        )
