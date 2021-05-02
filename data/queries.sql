-- all the birds at the soundscapes
select site, birds_array from soundscapes group by site, birds_array;

--the number of calls by species in the soundscapes
WITH site_birds AS (select site, unnest(birds_array)  as bird from soundscapes),
     clean_birds AS(select sb.site , substring(sb.bird from 2 for 6) as birds from site_birds as sb where sb.bird <> $$'nocall'$$),
     bird_count AS (select cb.site, cb.birds, count(cb.birds) from clean_birds as cb group by site, birds order by site, count desc)
select bc.site, bc.count, bc.birds, bs.common_name from bird_count as bc, bird_species as bs where bc.birds = bs.spec;

--find all calls within 1000km from one of the soundscape sites
select * from individual_calls, sscape_locations where st_distance(individual_calls.geog, sscape_locations.geog) < 1000000;
