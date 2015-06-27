#!/bin/bash


# batch_human=`echo $1 | tr '[a-z]' '[A-Z]'`
human=$1
nick=$2

# human=${batch_human:1:1}
if [ $# = 3 ]; then
	hostname=$3
else
	hostname=localhost
fi
echo You are going to use the hostname: $hostname;

if [ ! -d "$HOME/Desktop/logs/clients" ]; then
	mkdir -p "$HOME/Desktop/logs/clients"
fi

if [ ! -f "$HOME/Desktop/logs/clients/log$human.txt" ]; then
	echo 0 >  $HOME/Desktop/logs/clients/log$human.txt
fi

GetGP() {
	IFS=","
	while read g s p
	do 
		game=$g
		server=$s
		port=$p
	done < $HOME/Desktop/logs/clients/c$human.csv
};
trap 'GetGP;`python client.py $game $human $hostname $server`;echo $game $human $server > $HOME/Desktop/logs/clients/errr.txt;exit' 0 2 3 9 15;
while :
do
	played=`head -1 $HOME/Desktop/logs/clients/log$human.txt`; 
	cat $HOME/Desktop/logs/clients/log$human.txt;

	if [ $played = '0' ];
		then
		python client.py 1 $human $hostname &&
		GetGP;
		echo $game > $HOME/Desktop/logs/clients/log$human.txt;
		python 33.py chicken2 54 "$nick $port" 0 $hostname;
		# echo $game > $HOME/Desktop/logs/clients/log$human.txt;

	elif [ $played = '1' ];
		then
		python client.py 2 $human $hostname &&
		GetGP;
		echo $game > $HOME/Desktop/logs/clients/log$human.txt;
		python 33.py blocks2 47 "$nick $port" 0 $hostname;
		# echo $game > $HOME/Desktop/logs/clients/log$human.txt;
	elif [ $played = '2' ];
		then
		python client.py 3 $human $hostname &&
		GetGP;
		echo $game > $HOME/Desktop/logs/clients/log$human.txt;
		python 33.py prisoners 51 "$nick $port" 0 $hostname;
		# echo $game > $HOME/Desktop/logs/clients/log$human.txt;
	else
		echo You finished all the games
		read next 
		if [ $next = 'y' ];
			then 
			echo 0 > $HOME/Desktop/logs/clients/log$human.txt;
		else
			echo Thank you
			echo 0 > $HOME/Desktop/logs/clients/log$human.txt;
			break
		fi
	fi
done