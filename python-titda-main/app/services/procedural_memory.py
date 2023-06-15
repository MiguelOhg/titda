import os
import requests
import time
from database.queries import procedural_memory, perception, plan, action, system
import json
from urllib.request import Request, urlopen
import bs4
import urllib3


def read_all():
    return list(procedural_memory.get_memories())


def get_responses():
    return list(system.get_responses())


def get_responses_student(id):
    return list(system.get_responses_student(id))


def get_responses_extended_student(exercise_id, id):
    return list(system.get_responses_extended_student(exercise_id, id))


def read_url(url):
    try:
        url = url.replace(" ", "%20")
        req = Request(url)
        a = urlopen(req).read()
        soup = bs4.BeautifulSoup(a, 'html.parser')
        x = (soup.find_all('a'))
        for i in x:
            file_name = i.extract().get_text()
            url_new = url + file_name
            url_new = url_new.replace(" ", "%20")
            if file_name.endswith('.py') or file_name.endswith('.txt'):
                read_url(url_new)
                return url_new
    except NotADirectoryError:
        print('error')


def run():
    perception.insert_all()
    list_perceptions = perception.get_all()

    for i, item in enumerate(list_perceptions):
        print(i)
        # TODO:: get file from user
        [exercise, user, trying] = item['input'].split('-')
        path = 'http://31.220.56.44:3000/vpl_data/{}/usersdata/{}/{}/submittedfiles/'.format(exercise, user, trying)
        url = read_url(path)
        response_id = system.save_response(exercise, user, trying)
        if url is not None:
            response = requests.get(url)
            lines = response.content.decode('utf-8').split('\n')
            if len(lines) > 0:
                result = plan.get_one_by_attr('exercise_id', exercise)
                print('lines')
                print(lines)
                if len(result):
                    actions = action.get_all(result[0]['id'])
                    if len(actions):
                        # print('se encontraron acciones ejecutando')
                        operations = []
                        for t, todo in enumerate(actions):
                            if todo['procedural_memory_id'] == 2 and \
                                    (todo['value'].lower() == 'inicio' or todo["value"] == ''):
                                op = call_function(todo['procedural_memory_id'], lines[0], todo['type'], todo['value'])
                                operations.append(op)
                                system.save_revision(response_id, todo['id'], todo['procedural_memory_id'], lines[0],
                                                     op)
                            elif todo['procedural_memory_id'] == 4:
                                sub_operations = []
                                for index, line in enumerate(lines):
                                    if line != '' and index != 0:
                                        op = call_function(todo['procedural_memory_id'],
                                                           line,
                                                           'const',
                                                           todo['value'])
                                        sub_operations.append(op)
                                if any(x.startswith('done') for x in sub_operations):
                                    operations.append('done')
                                else:
                                    operations.append('fail')
                                system.save_revision(response_id, todo['id'], todo['procedural_memory_id'],
                                                     lines[t], sub_operations[t])
                            elif todo['procedural_memory_id'] != 2:
                                sub_operations = []
                                print(lines)
                                for index, line in enumerate(lines):
                                    if line != '' and index != 0:
                                        op = call_function(todo['procedural_memory_id'],
                                                           line,
                                                           todo['type'],
                                                           todo['value'])
                                        sub_operations.append(op)
                                if any(x.startswith('done') for x in sub_operations):
                                    operations.append('done')
                                else:
                                    operations.append('fail')

                                print('verify')
                                print(sub_operations)
                                print(t)
                                if t < len(sub_operations):
                                    system.save_revision(response_id, todo['id'], todo['procedural_memory_id'],
                                                         lines[t], sub_operations[t])
                                else:
                                    system.save_revision(response_id, todo['id'], todo['procedural_memory_id'],
                                                         lines[0], '')
                            else:
                                print(todo['type'])
                                if todo['type']:
                                    type = todo['type']
                                else:
                                    type = ""
                                if t < len(lines):
                                    op = call_function(todo['procedural_memory_id'], lines[t], type, todo['value'])
                                    operations.append(op)
                                    system.save_revision(response_id, todo['id'], todo['procedural_memory_id'],
                                                         lines[t], op)
                                else:
                                    operations.append('fail out of lines')

                        course = system.get_course_id(exercise, user)
                        if course is not None:
                            if any(x.startswith('fail') for x in operations):
                                system.save(course[0]['id'], user, 0, time.time())
                                system.update_response(response_id, 'fail', 'fail in operation')
                            else:
                                system.save(course[0]['id'], user, 1, time.time())
                                system.update_response(response_id, 'win', 'win in operation')
                        else:
                            system.update_response(response_id, 'fail', 'curso no encontrado')
                        perception.update(item['input'], 'done', item['id'])
                        return operations
                    else:
                        system.update_response(response_id, 'fail', 'no hay acciones configuradas para este plan')
                        perception.update(item['input'], 'done', item['id'])
                else:
                    system.update_response(response_id, 'fail', 'no se encontro plan')
                    perception.update(item['input'], 'done', item['id'])
            else:
                system.update_response(response_id, 'fail', 'no se encontraron lineas escritas por el usuario')
                perception.update(item['input'], 'done', item['id'])
        else:
            system.update_response(response_id, 'fail', 'fallo al encontrar el archivo')
            perception.update(item['input'], 'done', item['id'])

    return []


def read_txt(path):
    lines = []
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            lines.append(line.strip())
    return lines


def call_function(_id: int, string: str, type: str, value: str):
    instance = procedural_memory.call_function(_id)
    if len(instance) > 0:
        function_name = instance[0]['function_name']
        params = json.loads(instance[0]['params'])

        if 'contain' in params:
            if value is not None and value != '':
                params['contain'] = value.lower()
            else:
                params['contain'] = params['contain'].lower()

        if type is not None and type != '':
            params['type'] = type.lower()

        params['string'] = params['string'].replace("%", string).lower()

        # print(params)
        return globals()[function_name](**params)
    else:
        return 'row {} don´t exist'.format(instance)


def eval_string_contain(contain="", type="", string=""):
    if contain in string:
        return 'done'
    else:
        return 'fail in define string with {}'.format(string)


def eval_define_variable(contain="", type="", string=""):
    if type in string:
        return 'done'
    else:
        return 'fail in define variable with {}'.format(string)


def eval_define_constant(contain="", type="", value="", string=""):
    if contain in string and value in string:
        return 'done'
    else:
        return 'fail in define constant with {}'.format(string)


def eval_define_arithmetic_operation(type="", string=""):
    if type in string:
        return 'done'
    else:
        return 'fail in define arithmetic operation with {}'.format(string)


def eval_define_if(contain="", value="", type="", string=""):
    if contain in string:
        if type != '':
            if ' ' in type:
                types = type.split(' ')
                sp = []
                for t in types:
                    if t in string:
                        sp.append('done')
                    else:
                        sp.append('fail')
                if any(x.startswith('fail') for x in sp):
                    return 'fail in eval type with if in'.format(types)
                else:
                    return 'done'
            elif value != '' and value in string and type in string:
                return 'done'
            elif type in string:
                return 'done'
            else:
                return 'fail in eval type with if in'.format(type)
        else:
            return 'done'
    else:
        return 'fail in define if with {}'.format(string)


def eval_define_else(contain="", type="", value="", string=""):
    if contain in string and value in string:
        return 'done'
    else:
        return 'fail in define else with {}'.format(string)


def eval_define_elseif(contain="", value="", type="", string=""):
    if contain in string:
        if type != '':
            if ' ' in type:
                types = type.split(' ')
                sp = []
                for t in types:
                    if t in string:
                        sp.append('done')
                    else:
                        sp.append('fail')
                if any(x.startswith('fail') for x in sp):
                    return 'fail in eval type with if in'.format(types)
                else:
                    return 'done'
            elif value != '' and value in string and type in string:
                return 'done'
            elif type in string:
                return 'done'
            else:
                return 'fail in eval type with if in'.format(type)
        else:
            return 'done'
    else:
        return 'fail in define if with {}'.format(string)


def eval_define_for(contain="", type="", value="", string=""):
    if type in string:
        return 'done'
    else:
        return 'fail in define for with {}'.format(string)


def eval_define_do_while(contain="", type="", value="", string=""):
    if type in string:
        return 'done'
    else:
        return 'fail in define do while with {}'.format(string)
