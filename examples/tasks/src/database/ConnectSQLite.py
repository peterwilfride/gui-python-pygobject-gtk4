# -*- coding: utf-8 -*-
"""."""

import pathlib
import sqlite3

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATABASE = BASE_DIR.joinpath('data.sqlite3')


class ConnectDB:

    def __init__(self):
        self.con = sqlite3.connect(DATABASE)

        self.cur = self.con.cursor()

        # self.drop_table(table='tasks')
        self.create_table_tasks()

    def create_table_tasks(self):
        query = '''CREATE TABLE IF NOT EXISTS `tasks` (
        `pk`    INTEGER NOT NULL PRIMARY KEY,
        `task`  TEXT NOT NULL,
        `complete`  BOOLEAN NOT NULL DEFAULT 0
        );'''
        try:
            self.cur.execute(query)
        except Exception as e:
            print(f'\n[x] The table tasks was not created. [x]: {e}')
        else:
            print('\n[!] Table tasks created [!]')

    def drop_table(self, table: str):
        query = f'DROP TABLE IF EXISTS {table};'
        try:
            self.cur.execute(query)
        except Exception as e:
            print(f'\n[x] Failed to remove table [x]: {e}')
        else:
            self.con.commit()
            print(f'\n[!] Table {table} removed successfully [!]')
            return True
        return False

    def create_task(self, task: str):
        query = '''INSERT INTO tasks (task) VALUES (?);'''
        try:
            self.cur.execute(query, (task,))
        except Exception as e:
            self.con.rollback()
            print('\n[x] Failed to insert record [x]')
            print(f'[x] Reverting operation (rollback) [x]: {e}\n')
        else:
            self.con.commit()
            print('\n[!] Record inserted successfully [!]')
            return True
        return False

    def read_tasks(self, limit: int = 5):
        query = 'SELECT * FROM tasks LIMIT ?;'
        self.cur.execute(query, (limit,))
        return self.cur.fetchall()

    def read_task_by_id(self, pk: int):
        query = 'SELECT * FROM tasks WHERE pk = ?;'
        self.cur.execute(query, (pk,))
        return self.cur.fetchone()

    def update_task(self, pk: int, task: str):
        query = 'UPDATE tasks SET task = ? WHERE pk = ?;'
        try:
            self.cur.execute(query, (task, pk))
        except Exception as e:
            self.con.rollback()
            print(f'\n[x] set_task_status failed({pk}, {task}) [x]')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
        else:
            self.con.commit()
            print(f'\n[!] Registro ({pk}) alterado com sucesso [!]')
            return True
        return False

    def update_task_status(self, pk: int, status: bool):
        query = '''UPDATE tasks SET complete = ? WHERE pk = ?;'''
        try:
            self.cur.execute(query, (status, pk))
        except Exception as e:
            self.con.rollback()
            print(f'\n[x] set_task_status failed({pk}, {status}) [x]')
            print(f'[x] Revertendo operação (rollback) [x]: {e}\n')
        else:
            self.con.commit()
            print(f'\n[!] Registro ({pk}) alterado com sucesso [!]')
            return True
        return False

    def delete_task(self, pk: int):
        query = 'DELETE FROM tasks WHERE pk = ?;'
        try:
            self.cur.execute(query, (pk,))
        except Exception as e:
            self.con.rollback()
            print('\n[x] Failed to remove record [x]')
            print(f'[x] Reverting operation (rollback) [x]: {e}\n')
        else:
            self.con.commit()
            print('\n[!] Record removed successfully [!]')
            return True
        return False

    def get_last_row_id(self, table: str='tasks'):
        self.cur.execute(f'SELECT rowid from {table} order by ROWID DESC limit 1;')
        return self.cur.fetchone()[0]


if __name__ == '__main__':
    database = ConnectDB()
    database.con.close()
