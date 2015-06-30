![alt tag](https://github.com/tennom/humanMachineGaming/blob/master/human/shot.png)  

# Introduction 
HumanMachineGaming is a thesis project on human-robot interaction(HRI). This work so far includes the complete code for a pair 
or multiple human pairs to play matrix games (Prisoner's Dilemma, Chicken and Blocks are included so far, but you can play your 
own game by adding it into the `\games` directory).
Each directory is responsible for separate tasks.  
   
`\Server` is the game server.  
`\games` contains the payoff structure of the each games, so if you want to play your own game, you need to locate
a text file containing your game payoffs in this directory.   
`\human` includes human client interface and some other files that are associated with automatic game settings.  
`\logistics` has files for automatic game settings.  
`\result analysis` for making plots and analysis.

# Dependencies
For the game interface, no dependency is required. For data ananysis, `numpy` and `pyplot` are neccessary to make plots. In 
addition, game server is coded in C++, you have to run make in `Server` directory to build the server.

# How to install and set up a game  
  
  build the game server. Note, this is only once after your cloned the code, not everytime you set up a new game.  
  ```sh
  cd ..\Server
  make
  ```
  
  
Start game server:
```sh
cd ..\Server
./CheapTalk <GAMENAME> <ROUND NUMBERS> 0 cheaptalk 
``` 
Replace `GAMENAME` with the game you want to play; for example, prisons, chicken2 or blocks2. and specify the rounds
like 50 or 100 in place of `ROUND NUMBERS`.  
   
   
Human clients:
  Human client 1, in a new terminal window,
```sh
cd ../human
python 33.py <GAMENAME> <ROUND NUMBERS> '<YOURNICKNAME> 0' 1 localhost
```  
The other parameters are the same as the game server, except for `'<YOURNICKNAME> 0'` where you choose your name;
 for example, Spider. You may also change `localhost` to the server IP if you the client is on another machine.
   
  Human client 2, in a new terminal window,
```sh
cd ../human
python 33.py <GAMENAME> <ROUND NUMBERS> '<YOURNICKNAME> 1' 1 localhost
```  
The same as above. Now, you should see the game as shown in the screen shot. You may follow the annotated steps to play a game.   
# Contact me:
[tennomyathog@gmail.com](mailto:tennomgmail@gmail.com)





