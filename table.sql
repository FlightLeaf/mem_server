create sequence comment_id_seq;

create sequence comment_news_id_seq;

create sequence news_id_seq;

create sequence user_follows_id_seq;

create sequence user_like_news_id_seq;

create sequence videos_comment_id_seq;

create sequence videos_comment_videos_id_seq;

create sequence videos_id_seq;

create sequence videos_love_id_seq;

create sequence videos_love_videos_id_seq;

create table img_head
(
    url text
);

create table img_title
(
    url text
);

create table "user"
(
    email      varchar(100) not null
        constraint user_pk
            primary key,
    name       varchar(255) not null,
    password   varchar(255) not null,
    image      text         not null,
    label      text,
    created_at timestamptz(6) default CURRENT_TIMESTAMP
);

create table news
(
    id          int8           default nextval('news_id_seq'::regclass) not null
        constraint news_pkey
            primary key,
    title       varchar(255),
    description text,
    imageurl    varchar(255),
    created_at  timestamptz(6) default CURRENT_TIMESTAMP,
    email       varchar(100)                                            not null
        constraint news_source_fk
            references "user",
    likes       int4           default 0,
    url         varchar(255)
);

create table comment
(
    id         int8           default nextval('comment_id_seq'::regclass)      not null
        constraint comment_pkey
            primary key,
    user_email varchar(100)                                                    not null
        constraint comment_user_email_fk
            references "user",
    news_id    int8           default nextval('comment_news_id_seq'::regclass) not null
        constraint comment_news_id_fk
            references news,
    comment    text                                                            not null,
    created_at timestamptz(6) default CURRENT_TIMESTAMP
);

create table user_follows
(
    id                int4           default nextval('user_follows_id_seq'::regclass) not null
        constraint user_follows_pkey
            primary key,
    user_email        varchar(100)                                                    not null
        constraint user_follows_user_email_email_fk_1
            references "user",
    follow_user_email varchar(100)                                                    not null
        constraint user_follows_user_email_email_fk_2
            references "user",
    created_at        timestamptz(6) default CURRENT_TIMESTAMP                        not null
);

comment on table user_follows is '用户关注表';

create table user_like_news
(
    id         int8           default nextval('user_like_news_id_seq'::regclass) not null
        constraint user_like_news_pkey
            primary key,
    user_email varchar(100)                                                      not null
        constraint user_like_news_mail_fk
            references "user",
    news_id    int8                                                              not null
        constraint user_like_news_id_fk
            references news,
    created_at timestamptz(6) default CURRENT_TIMESTAMP
);

create table videos
(
    id          int4           default nextval('videos_id_seq'::regclass) not null
        constraint videos_pkey
            primary key,
    name        varchar(50)                                               not null,
    artistname  varchar(50)                                               not null,
    "desc"      text,
    cover       text                                                      not null,
    publishtime varchar(50)                                               not null,
    email       varchar(100)
        constraint videos_source_fk
            references "user",
    url         text           default 'mv'                               not null,
    created_at  timestamptz(6) default CURRENT_TIMESTAMP
);

create table videos_comment
(
    id         int8           default nextval('videos_comment_id_seq'::regclass)        not null
        constraint videos_comment_pk
            primary key,
    videos_id  int8           default nextval('videos_comment_videos_id_seq'::regclass) not null
        constraint videos_comment_videos_id_fk
            references videos,
    user_email varchar(100)                                                             not null
        constraint videos_comment_user_email_fk
            references "user",
    comment    text                                                                     not null,
    created_at timestamptz(6) default CURRENT_TIMESTAMP
);

create table videos_love
(
    id         int8           default nextval('videos_love_id_seq'::regclass)        not null
        constraint videos_love_pk
            primary key,
    videos_id  int8           default nextval('videos_love_videos_id_seq'::regclass) not null
        constraint videos_love_videos_id_fk
            references videos,
    user_email varchar(100)                                                          not null
        constraint videos_love_user_email_fk
            references "user",
    created_at timestamptz(6) default CURRENT_TIMESTAMP
);

--url,name,cover,author,pub,date,score,des
create table book
(
    url text,
    name text,
    cover text,
    author text,
    pub text,
    date text,
    score text,
    des text
);


show server_encoding;

show client_encoding;

\encoding GBK;

show client_encoding;