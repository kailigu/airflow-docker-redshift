DROP TABle IF EXISTS public.staging_events;
DROP TABLE IF EXISTS public.staging_songs;
DROP TABLE IF EXISTS public.songplays;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.songs;
DROP TABLE IF EXISTS public.artists;
DROP TABLE IF EXISTS public.time;



CREATE TABLE public.artists (
	artistid text NOT NULL,
	name text,
	location text,
	lattitude numeric(18,0),
	longitude numeric(18,0)
);

CREATE TABLE public.songplays (
	playid varchar(32) NOT NULL,
	start_time timestamp NOT NULL,
	userid int4 NOT NULL,
	"level" text,
	songid text,
	artistid text,
	sessionid int4,
	location text,
	user_agent text,
	CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);

CREATE TABLE public.songs (
	songid text NOT NULL,
	title text,
	artistid text,
	"year" int4,
	duration numeric(18,0),
	CONSTRAINT songs_pkey PRIMARY KEY (songid)
);

CREATE TABLE public.staging_events (
	artist text,
	auth text,
	firstname text,
	gender text,
	iteminsession int4,
	lastname text,
	length numeric(18,0),
	"level" text,
	location text,
	"method" text,
	page text,
	registration numeric(18,0),
	sessionid int4,
	song text,
	status int4,
	ts int8,
	useragent text,
	userid int4
);

CREATE TABLE public.staging_songs (
	num_songs int4,
	artist_id text,
	artist_name varchar(max),
	artist_latitude numeric(18,0),
	artist_longitude numeric(18,0),
	artist_location varchar(max),
	song_id varchar(max),
	title varchar(max),
	duration numeric(18,0),
	"year" int4
);

CREATE TABLE public."time" (
	start_time timestamp NOT NULL,
	"hour" int4,
	"day" int4,
	week int4,
	"month" text,
	"year" int4,
	weekday text,
	CONSTRAINT time_pkey PRIMARY KEY (start_time)
) ;

CREATE TABLE public.users (
	userid int4 NOT NULL,
	first_name text,
	last_name text,
	gender text,
	"level" text,
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);
