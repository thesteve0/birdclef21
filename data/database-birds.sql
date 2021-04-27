-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---


-- object: public.bird_species | type: TABLE --
-- DROP TABLE IF EXISTS public.bird_species CASCADE;
CREATE TABLE public.bird_species (
	spec text NOT NULL,
	common_name text,
	sci_name text,
	spec6 text,
	CONSTRAINT bird_species_pk PRIMARY KEY (spec)

);

-- object: bird_species_6_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.bird_species_6_idx CASCADE;
CREATE INDEX bird_species_6_idx ON public.bird_species
	USING btree
	(
	  spec6
	);
-- ddl-end --

-- object: public.sscape_dates | type: TABLE --
-- DROP TABLE IF EXISTS public.sscape_dates CASCADE;
CREATE TABLE public.sscape_dates (
	id smallint NOT NULL,
	site text,
	string_date text,
	date date,
	CONSTRAINT sscape_dates_pk PRIMARY KEY (id)

);

-- object: public.individual_calls | type: TABLE --
-- DROP TABLE IF EXISTS public.individual_calls CASCADE;
CREATE TABLE public.individual_calls (
	id integer NOT NULL GENERATED ALWAYS AS IDENTITY ,
	primary_label text,
	secondary_labels text[],
	call_type text[],
	lat numeric(7,4),
	lon numeric(7,4),
	geog geography(POINT, 4326),
	author text,
	date_string text,
	date_recorded date,
	filename text,
	rating numeric(3,1),
	CONSTRAINT individual_calls_pk PRIMARY KEY (id)

);

-- object: ind_calls_primary_species_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.ind_calls_primary_species_idx CASCADE;
CREATE INDEX ind_calls_primary_species_idx ON public.individual_calls
	USING btree
	(
	  primary_label
	);
-- ddl-end --

-- object: ind_calls_geog_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.ind_calls_geog_idx CASCADE;
CREATE INDEX ind_calls_geog_idx ON public.individual_calls
	USING gist
	(
	  geog
	);
-- ddl-end --

-- object: ind_calls_rating_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.ind_calls_rating_idx CASCADE;
CREATE INDEX ind_calls_rating_idx ON public.individual_calls
	USING btree
	(
	  rating
	);
-- ddl-end --

-- object: public.soundscapes | type: TABLE --
-- DROP TABLE IF EXISTS public.soundscapes CASCADE;
CREATE TABLE public.soundscapes (
	row_id text NOT NULL,
	site text,
	audio_id integer,
	seconds_in smallint,
	birds_array text[],
	CONSTRAINT soundscapes_pk PRIMARY KEY (row_id)

);

-- object: public.sscape_locations | type: TABLE --
-- DROP TABLE IF EXISTS public.sscape_locations CASCADE;
CREATE TABLE public.sscape_locations (
	id text NOT NULL,
	place_name text,
	country text,
	lat numeric(6,2),
	lon numeric(6,2),
	geog geography(POINT, 4326),
	CONSTRAINT sscape_locations_pk PRIMARY KEY (id)

);

-- object: sscape_locations_geog_idx | type: INDEX --
-- DROP INDEX IF EXISTS public.sscape_locations_geog_idx CASCADE;
CREATE INDEX sscape_locations_geog_idx ON public.sscape_locations
	USING gist
	(
	  geog
	);
-- ddl-end --
