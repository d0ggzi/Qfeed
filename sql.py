import psycopg2
import config

class SQL:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(f"""
            host=rc1b-2wfn2w8hz6rt5hfv.mdb.yandexcloud.net
            port=6432
            sslmode=verify-full
            dbname={config.dbname}
            user={config.dbuser}
            password={config.dbpassword}
            target_session_attrs=read-write
        """)
        self.cursor = self.conn.cursor()

    def add_user(self, user_id, chat_id, username):
        with self.conn:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
            result = self.cursor.fetchall()
            if not bool(len(result)):
                self.cursor.execute("INSERT INTO users (user_id, chat_id, username) VALUES (%s, %s, %s)", (user_id, chat_id, username,))

    def add_channel(self, channel_id, name, topic_id):
        with self.conn:
            self.cursor.execute("INSERT INTO channels (channel_id, name, topic_id) VALUES (%s, %s, %s)", (channel_id, name, topic_id))

    def add_topic(self, topic_id, name, chat_id):
        with self.conn:
            self.cursor.execute("INSERT INTO topics (topic_id, name, chat_id) VALUES (%s, %s, %s)", (topic_id, name, chat_id))

    def get_topics(self, chat_id):
        with self.conn:
            topic_list = []
            self.cursor.execute("SELECT name, topic_id FROM topics WHERE chat_id=%s", (str(chat_id),))
            result = self.cursor.fetchall()
            for topic in result:
                topic_list.append(topic)
            return topic_list

    def add_channel(self, name: str):
        """Добавление основного канала"""
        with self.conn:
            # Проверка на наличие записи такого канала
            self.cursor.execute("SELECT channel FROM config WHERE channel=%s", (name,))
            result = self.cursor.fetchall()
            if not bool(len(result)):
                self.cursor.execute("INSERT INTO config (channel) VALUES (%s)", (name,))
                return f'Запись {name} добавлена.'
            return f'Запись {name} существует.'

    def get_channels(self):
        with self.conn:
            topic_list = []
            self.cursor.execute("SELECT name FROM channels")
            result = self.cursor.fetchall()
            for topic in result:
                if topic[0] is None:
                    pass
                else:
                    topic_list.append(topic[0])
            return topic_list

    def delete_channel(self, name: str):
        """Удаление основного канала"""
        with self.connection:
            # Проверка на наличие записи такого канала
            self.cursor.execute("SELECT channel FROM config WHERE channel = %s", (name,))
            result = self.cursor.fetchall()
            if not bool(len(result)):
                return f'Запись {name} не найдена.'
            else:
                self.cursor.execute("DELETE FROM config WHERE channel = %s", (name,))
                return f'Запись {name} удалена.'

    def get_all_users(self):
        with self.conn:
            users_list = []
            self.cursor.execute("SELECT chat_id FROM users")
            result = self.cursor.fetchall()
            for chat in result:
                if chat[0] is None:
                    pass
                else:
                    users_list.append(chat[0])
            return users_list

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()




# conn = psycopg2.connect(f"""
#     host=rc1b-2wfn2w8hz6rt5hfv.mdb.yandexcloud.net
#     port=6432
#     sslmode=verify-full
#     dbname={config.dbname}
#     user={config.dbuser}
#     password={config.dbpassword}
#     target_session_attrs=read-write
# """)
# cursor = conn.cursor()
#
# cursor.execute(f"Select chat_id FROM users")
# for table in cursor.fetchall():
#     print(table)
# print('---')