CREATE TABLE "user" (
    email VARCHAR(100) NOT NULL
        CONSTRAINT user_pk
            PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    image TEXT NOT NULL,
    label TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE news (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    imageurl VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,  -- 修改为created_at，并设置默认值
    email VARCHAR(100) NOT NULL,
    likes INTEGER DEFAULT 0,
    url VARCHAR(255),
    CONSTRAINT news_source_fk
        FOREIGN KEY (email) REFERENCES "user"(email)
);

CREATE TABLE comment (
    id BIGSERIAL PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL
        CONSTRAINT comment_user_email_fk
            REFERENCES "user"(email),
    news_id BIGSERIAL NOT NULL
        CONSTRAINT comment_news_id_fk
            REFERENCES news(id),
    comment TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_like_news (
    id BIGSERIAL PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL
        CONSTRAINT user_like_news_mail_fk
            REFERENCES "user"(email),
    news_id BIGINT NOT NULL
        CONSTRAINT user_like_news_id_fk
            REFERENCES news(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
