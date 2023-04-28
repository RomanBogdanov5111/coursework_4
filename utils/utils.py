from os.path import join
from time import sleep


from tqdm import tqdm
from art import tprint
from prettytable import PrettyTable

from src.head_hunter_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.table_creator import TableCreator


def print_intro() -> None:
    """Функция печатает приветствие"""

    print('\n' + '\t' * 4 + 'Hi There, this is...\n')
    tprint('Job-Job')

    input('Press Enter to start:')

    pbar = tqdm(range(100),
                leave=False,
                ncols=60,
                colour='#747671',
                bar_format='The program is loading:|{bar}|{n_fmt}/{total_fmt}%'
                )

    for i in pbar:
        sleep(0.025)
        pbar.set_description()


def print_main_menu_table(table: PrettyTable) -> None:
    """
    Функция принимает таблицу главного меню и печатает ее
    :param table: Инициализированный таблицей объект PrettyTable
    """

    print('\t' * 4 + '   Главное меню')
    print(table)
    print()


def print_vacancy_table(table: PrettyTable) -> None:
    """
    Функция принимает таблицу с вакансиями и печатает ее
    :param table: Инициализированный таблицей объект PrettyTable
    """
    print(table)
    print('[1] - Предыдущая страница \t\t\t\t[2] - Следующая страница \n'
          '[*n] - Добавить вакансию в избранное \t[3] - Главное меню')


def get_action_number(total_numbers: int) -> int or str:
    """
    Функция запрашивает ввод пользователя для выбора действия в меню, число от 1 до total_numbers или [*n] n - от 1 до 8
    :param total_numbers: Инициализированный таблицей объект PrettyTable
    :return: int, Число о 1 до total_numbers, которое ввел пользователь.
    """

    while True:

        action_num = input('Выберите номер действия: ')
        print()

        if action_num.isdigit():
            if 0 < int(action_num) <= total_numbers:
                action_num = int(action_num)
                return action_num
            else:
                print(f'Выберите другое действие!!!')

        elif action_num.startswith('*') \
                and len(action_num) == 2 \
                and action_num[1].isdigit() \
                and int(action_num[1]) in range(1, 9):
            return action_num

        else:
            print(f'Выберите другое действие!!!')


def vacancy_scroller(api_obj):

    # Создал экземпляр для АПИ hh.ru

    path_to_file = join('..', 'data', 'featured_vacancies.json')

    while True:

        # Получил данные по вакансиям с hh.ru и записал их в таблицу и напечатал

        hh_vacancies = api_obj.basic_info_about_vacancies
        vacancies_table = TableCreator.vacancies(hh_vacancies)
        print(f'Номер страницы: {api_obj.page}')
        print_vacancy_table(vacancies_table)

        # Ввод пользователя с выбором действия
        vacancy_action = get_action_number(3)

        # Блок с вариантами действий в зависимости от выбора пользователя.
        if vacancy_action == 1 and api_obj.page > 1:
            api_obj.page -= 1

        elif vacancy_action == 2:
            api_obj.page += 1

        elif vacancy_action == 3:
            break

        elif vacancy_action in ['*1', '*2', '*3', '*4', '*5', '*6', '*7', '*8']:

            # Записали номер вакансии.
            vacancy_number = int(vacancy_action[1])

            # Тут по номеру вакансии ищем ее на странице, если номер совпадает, записываем ее в JSON.
            for vacancy in hh_vacancies:

                if vacancy['number'] == vacancy_number:
                    JSONSaver.save_to_file(path_to_file, vacancy)
