CREATE TABLE users(
    user_id INT NOT NULL UNIQUE,
    chat_id VARCHAR(50) NOT NULL UNIQUE,
    username VARCHAR(50),
    PRIMARY KEY(chat_id)
);

CREATE TABLE topics(
   topic_id VARCHAR(50) NOT NULL,
   chat_id VARCHAR(50) NOT NULL,
   name VARCHAR(100) NOT NULL,
   PRIMARY KEY(topic_id, chat_id),
   CONSTRAINT fk_chat_id
      FOREIGN KEY(chat_id)
      REFERENCES users(chat_id)
);

CREATE TABLE channels(
   channel_id VARCHAR(50) NOT NULL,
   name VARCHAR(100) NOT NULL,
   topic_id VARCHAR(50) NOT NULL,
   chat_id VARCHAR(50) NOT NULL,
   PRIMARY KEY(channel_id),
   CONSTRAINT fk_topic
      FOREIGN KEY(topic_id, chat_id)
      REFERENCES topics(topic_id, chat_id)
);

CREATE TABLE subscribed(
    user_id INT NOT NULL,
    subscribed INT NOT NULL,
    CONSTRAINT user_id
      FOREIGN KEY(user_id)
      REFERENCES users(user_id)
);