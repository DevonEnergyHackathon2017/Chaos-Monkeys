/* fracking data from PI*/
SELECT
timestamp, cast(GELLINGAGENT as float) as gelling_agent, cast(CALCULATEDBHSANDCONC as float) as CALC_BH_SAND_CONC, cast(PRESSURE as float) as treating_pressure, cast(crosslinker as float) as crosslinker,  cast(slurryrate as float) as slurry_rate,  cast(SURFACESANDCONC as float) as surface_sand_conc, cast(FRBREAKER as float) as fr_breaker

INTO

   frackpbi
FROM
    frackeh

/* normal flow data from made up wells */
SELECT
    *, location.long as lon, location.lat as lat
INTO
    normalpbi
FROM
    normaldata

SELECT name as WellName, Timestamp as ProductionTime,
bopd, mcfd, bwpd, pressure
    INTO sqlserver
FROM normaldata


/* Tank Level SA*/
SELECT
    *
INTO
    tankpbi
FROM
    tankeh

SELECT name as TankName,
    Timestamp,
    Max as MaxValue,
    location.lat as Latitude,
    location.long as Longitude,
    level as TankLevel
INTO sqlserver
FROM tankeh