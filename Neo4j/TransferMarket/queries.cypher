// 
//----------------------------------------------------------------------------------
//QUERY I. Return the 'position' of the Node with label 'Player'
// 	   and 'name' 'Pierre van Hooijdonk' 
//----------------------------------------------------------------------------------
//
match (player:Player {name:"Pierre van Hooijdonk"}) return player.position AS position;
// 
//-----------------------------------------------------------------------------------
//QUERY II. Return the 'season' and 'fee' for all Nodes with label 'Transfer' and 
//	    having a relationship with the Node with label 'Player' and 'name' 
//	    'Pierre van Hooijdonk'
//-----------------------------------------------------------------------------------
//
match (n:Player {name:"Pierre van Hooijdonk"})--(m:Transfer) return m.season AS season,m.fee AS fee;
// 
// -------------------------------------------------------------------------------------
// QUERY III. Return the maximum ('max') amount of transfers a Node with label 'Player'
//	      is involved in the dataset. 
//	      Tip: You might consider counting the number of transfers ('count') each
//	           Node with label 'Player' is involved at in order to find the 
//		   maximum among these numbers. 
// -------------------------------------------------------------------------------------
//
match (n:Player)--(m:Transfer) 
with n,count(m) AS Num 
return max(Num) AS max_num_transfers;
// 
// -------------------------------------------------------------------------------------
// QUERY IV. Return the 'name' of all Nodes with label 'Player' involved in 7 transfers 
//	     (which we know from QUERY III is the max number of transfers).	     
//	     Collect the results into a list, thus returning just 1 row.
// -------------------------------------------------------------------------------------
//
match (n:Player)--(m:Transfer) 
with n,count(m) AS Num
where count(m)=7
with collect(n.name) AS list_of_players
return list_of_players;
// 
// ------------------------------------------------------------------------------------------------------
// QUERY V. Return the player 'name' and transfer 'fee' of the most expensive transfer of season 01/02.
// ------------------------------------------------------------------------------------------------------
//
match (n:Transfer {season:"01/02"})--(m:Player)
with m,n,n.fee AS fee1
with m,n,replace(fee1,"£","") AS fees
with m,n,replace(fees,"m","") AS fee
with m,n,toFloat(fee) AS fee
order by fee desc
limit 1
return m.name,n.fee;
// 
// ------------------------------------------------------------------------------------------------------
// QUERY VI. Return the 'name' of all players transferred to the club 'PSV Eindhoven' in the season 02/03. 	     
// ------------------------------------------------------------------------------------------------------
//
match (m:Player)--(n:Transfer {season:"02/03"})-[:TO_CLUB]->(x:Club{name:"PSV Eindhoven"})
return m.name AS player_name;
// 
// -------------------------------------------------------------------------------------------------------------------
// QUERY VII. Return the number of players transferred from a Spanish to an English club.
// -------------------------------------------------------------------------------------------------------------------
//
match (y:Club{country: "Spain"})-[:FROM_CLUB]-(n:Transfer)-[:TO_CLUB]-(x:Club{country: "England"})
return count(*) AS Count;
// 
// -------------------------------------------------------------------------------------------------------------------
// QUERY VIII. Return the name of the youngest player transferred from 'Real Madrid' to an English club.
// -------------------------------------------------------------------------------------------------------------------
//
match (y:Club{name:"Real Madrid"})-[:FROM_CLUB]-(n:Transfer)-[:TO_CLUB]-(x:Club{country: "England"})
match (n)-[p:OF_PLAYER]->(m:Player)
with m,p.age AS AGE
order by AGE
limit 1
return m.name,AGE;
