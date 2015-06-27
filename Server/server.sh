#!/bin/bash
s=$1
g1=chicken2
g2=blocks2
g3=prisoners
GetPorts() {
	IFS=","
	echo what is $s
	while read a b c
	do 
		p1=$a
		p2=$b
		p3=$c
	done < $HOME/Desktop/logs/servers/$s.csv
};
GetPorts
echo my ports are $p1 $p2 $p3
if [ ! -d "$HOME/Desktop/logs/servers" ]; then
	mkdir -p "$HOME/Desktop/logs/servers"
fi
echo 0 > $HOME/Desktop/logs/servers/crash$s.txt;

while :
do 
	played=`head -1 $HOME/Desktop/logs/servers/$s.txt`
	echo "------------- State: $played Port: $p1 --------------"
	if [ $played = '0' ]; then
		echo 1 > $HOME/Desktop/logs/servers/$s.txt;
		echo listening on port 0, setting up game 1 ............
		./CheapTalk $g1 54 $p1;
		###./CheapTalk $g1 54 $p1 cheaptalk;  this is the way of cheap talk

		crash=`head -1 $HOME/Desktop/logs/servers/crash$s.txt`;
		if [ $crash = "100" ]; then
			break
		fi

	elif [ $played = '1' ]; then
		echo 2 > $HOME/Desktop/logs/servers/$s.txt;
		echo listening on port 2, setting up game 2 ............
		./CheapTalk $g2 47 $p2;
		# echo 2 > $HOME/Desktop/logs/servers/1.txt;

		crash=`head -1 $HOME/Desktop/logs/servers/crash$s.txt`;
		if [ $crash = "100" ]; then
			break
		fi

	elif [ $played = "2" ]; then
		echo 3 > $HOME/Desktop/logs/servers/$s.txt;
		echo listening on port 4, setting up game 3 ............
		./CheapTalk $g3 51 $p3;

		crash=`head -1 $HOME/Desktop/logs/servers/crash$s.txt`;
		if [ $crash = "100" ]; then
			break
		fi
	else
		echo Server finished all the game. [y] only if you want to rerun:
		read next
		if [ $next = 'y' ];
			then 
			echo 0 > $HOME/Desktop/logs/servers/$s.txt;
			echo 0 > $HOME/Desktop/logs/servers/crash$s.txt;
		else
			echo Thank you
			break
		fi
	fi
done
