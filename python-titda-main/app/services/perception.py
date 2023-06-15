from database.queries import perception


def read_all():
    return list(perception.get_all())


def create(request):
    input = request.get("input")
    id = perception.save(input)
    return request, 201


def update(request):
    id = request.get("id")
    input = request.get("input")
    status = request.get("status")
    id = perception.update(input, status, id)
    return request, 201


def delete(request):
    perception_id = request.get("id")
    id = perception.delete(perception_id)
    return request, 201



