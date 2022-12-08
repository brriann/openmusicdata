select ar.*, a.name as sourcename, c.name as targetname
from artistrelations ar
join artists a on ar.sourceartistid = a.id
join artists c on ar.targetartistid = c.id
limit 100

select q.*, a.name as seedartistname
from queriesrelatedartist q
join artists a on q.seedartistid = a.id
limit 1000
