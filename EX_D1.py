import sys
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': "a0ebab980b0450969155454777334073",
    'token': "decc60460c684352ab895e06bf7460b9b6ca3f0ed81bc6ac9d5f542a3eee708e",
}
board_id = "HuLhQ4u6"


def read():
    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + " - ({})".format(len(task_data)))

        if not task_data:
            print('\t' + 'Нет задач')
            continue
        for task in task_data:
            print('\t' + task['name'] + '\t' + task['id'])


def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']

    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})


def move(name, column_name):
    duplicate_tasks = get_task_duplicates(name)
    if len(duplicate_tasks) > 1:
        print("Задач с таким названием несколько штук:")
        for index, task in enumerate(duplicate_tasks):
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']
            print("Задача №{}\tid: {}\tНаходится в колонке: {}\t ".format(index, task['id'], task_column_name))
        task_id = input("Введите ID задачи, которую нужно переместить: ")
    else:
        task_id = duplicate_tasks[0]['id']

    
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})


def column_check(column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            return column['id']
    return


def create_column(column_name):
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()


def get_task_duplicates(task_name):
    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    
    duplicate_tasks = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == task_name:
                duplicate_tasks.append(task)
    return duplicate_tasks


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
