from flask import render_template, request
from services import plan, goal, action, discrepancy, procedural_memory
import connexion
from apscheduler.schedulers.background import BackgroundScheduler


def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")
    procedural_memory.run()


schedule = BackgroundScheduler(daemon=True)
schedule.add_job(sensor, 'interval', minutes=1)
schedule.start()
app = connexion.App(__name__, specification_dir="../")
# C:/Users/heide/PycharmProjects/its/app/swagger.yml
#
app.add_api("/app/swagger.yml")


@app.route('/', methods=['GET'])
def hello():
    id = None
    labels = []
    attempts = []
    errors = []
    responses = []
    p = {}

    if request.url.lower().__contains__('id='):
        id = request.url.split('id=')[1]
        responses = procedural_memory.get_responses_student(id)

        for d in responses:
            print(d)
            d['extended'] = procedural_memory.get_responses_extended_student(d['exercise_id'], id)
            t = p.setdefault(d['name'], [])
            t.append(d)
        for item in p:
            labels.append(item.split(' ')[len(item.split(' '))-1][0:6])
            attempts.append(sum(item['attempts'] for item in p[item]))
            errors.append(sum(int(item['errors']) for item in p[item]))
    else:
        responses = procedural_memory.get_responses()
        for d in responses:
            t = p.setdefault(d['name'], [])
            t.append(d)
        for item in p:
            labels.append(item.split(' ')[len(item.split(' '))-1][0:6])
            attempts.append(sum(item['attempts'] for item in p[item]))
            errors.append(sum(int(item['errors']) for item in p[item]))

    return render_template('index.html', current=request.endpoint,
                           labels=labels,
                           attempts=attempts,
                           errors=errors,
                           id=id,
                           responses=responses)


@app.route('/plans', methods=['GET'])
def plans():
    return render_template('plan/index.html',
                           current=request.endpoint, exercises=plan.read_exercises(),
                           plans=plan.read_all())


@app.route('/plans/<id>/actions', methods=['GET'])
def actions(id):
    return render_template('action/index.html',
                           current=request.endpoint,
                           plan_id=id,
                           actions=action.read_all(id),
                           procedural_memory=procedural_memory.read_all())


@app.route('/plans/<id>/goal', methods=['GET'])
def goals(id):
    return render_template('goal/index.html', current=request.endpoint, plan_id=id, goals=goal.read_all(id))


@app.route('/plans/<id>/discrepancy', methods=['GET'])
def discrepancies(id):
    return render_template('discrepancy/index.html',
                           current=request.endpoint, plan_id=id,
                           discrepancies=discrepancy.read_all(id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
