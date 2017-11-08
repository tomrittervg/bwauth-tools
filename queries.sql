-- Calculate the percent difference between two relays
SELECT 
	r1.timestamp, 
	r1.fingerprint,
	(abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 5

-- Calculate the percent difference between two bwauth votes, for all relays
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 5
group by r1.timestamp


-- Calculate the percent difference between two bwauth votes, for relays with a measured bw > 100
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 5
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp



-- Calculate the percent difference between all bwauth votes
SELECT 
	ts.timestamp,
	three_five_all.percent_difference as maatuska_vanilla_all,
	three_five_hundred.percent_difference  as maatuska_vanilla_hundred,
	
	three_six_all.percent_difference as maatuska_nodns_all,
	three_six_hundred.percent_difference  as maatuska_nodns_hundred,
	
	three_one_all.percent_difference as maatuska_bastet_all,
	three_one_hundred.percent_difference as maatuska_bastet_hundred,

	three_two_all.percent_difference as maatuska_faravahar_all,
	three_two_hundred.percent_difference as maatuska_faravahar_hundred,

	three_four_all.percent_difference as maatuska_moria_all,
	three_four_hundred.percent_difference as maatuska_moria_hundred
FROM
relays as ts

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 5
group by r1.timestamp
) as three_five_all
on ts.timestamp = three_five_all.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 5
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp
) as three_five_hundred
on ts.timestamp = three_five_hundred.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 6
group by r1.timestamp
) as three_six_all
on ts.timestamp = three_six_all.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 6
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp
) as three_six_hundred
on ts.timestamp = three_six_hundred.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 1
group by r1.timestamp
) as three_one_all
on ts.timestamp = three_one_all.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 1
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp
) as three_one_hundred
on ts.timestamp = three_one_hundred.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 2
group by r1.timestamp
) as three_two_all
on ts.timestamp = three_two_all.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 2
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp
) as three_two_hundred
on ts.timestamp = three_two_hundred.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 4
group by r1.timestamp
) as three_four_all
on ts.timestamp = three_four_all.timestamp

left outer join
(
SELECT 
	r1.timestamp, 
	AVG((abs(r1.bw - r2.bw) / ((r1.bw + r2.bw) / 2)) * 100) as percent_difference
FROM `relays` as r1
inner join relays as r2
on r1.timestamp = r2.timestamp
and r1.fingerprint = r2.fingerprint
and r1.bwauth = 3
and r2.bwauth = 4
and r1.bw > 100
and r2.bw > 100
group by r1.timestamp
) as three_four_hundred
on ts.timestamp = three_four_hundred.timestamp

INTO OUTFILE '/var/lib/mysql-files/bwauth-diffs-2017-11-05.04.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';