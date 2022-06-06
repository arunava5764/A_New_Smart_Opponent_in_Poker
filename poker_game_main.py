#import numpy as np
from dataclasses import dataclass
import time
import pandas as pd  
import random 
from utility import finddeckindex,EHS
class Card:

    # SUIT_TO_STRING = {1: "s", 2: "h", 3: "d", 4: "c"}

    # RANK_TO_STRING = {
    #     2: "2",
    #     3: "3",
    #     4: "4",
    #     5: "5",
    #     6: "6",
    #     7: "7",
    #     8: "8",
    #     9: "9",
    #     10: "T",
    #     11: "J",
    #     12: "Q",
    #     13: "K",
    #     14: "A",
    # }

    # STRING_TO_SUIT = dict([(v, k) for k, v in SUIT_TO_STRING.items()])
    # STRING_TO_RANK = dict([(v, k) for k, v in RANK_TO_STRING.items()])

    def __init__(self):
        self.rank = None
        self.suit = None

    # def compareCards()
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        return self.rank < other.rank

@dataclass
class CARD:
    def __init__(self):
        self.rank = None
        self.suit = None
    
#@dataclass
class Pair:
    def __init__(self):
        self.u = None
        self.v= None

suits = [0]*4
ranks = [0]*13
val=[0]*169
reflop=[]
threshold=None
weight=[0]*1326

def returnCard(n):
   c=CARD()
   i=n%13;
   j=(n-1)/13;

   if(j==0): 
       c.suit='s'
   elif(j==1):
       c.suit='h'
   elif(j==2):
       c.suit='d'
   elif(j==3):
       c.suit='c'

   if(i>=2 and i<=9):
       c.value=chr(i+48)
   elif(i==1):
       c.value='A'
   elif(i==10):
       c.value='T'
   elif(i==11):
       c.value='J'
   elif(i==12):
       c.value='Q'
   elif(i==0):
       c.value='K' 
   return c


def cardToTable(i,j):
    p=Pair()

    c=CARD()
    d=CARD()
    
    s=""
    t=""
    c=returnCard(i)
    d=returnCard(j)

    if(c.value==d.value):
        t=s
    elif(c.suit==d.suit):
        s=s+c.value
        s=s+d.value
        s=s+'s'
        t=t+c.value
        t=t+d.value
        t=t+'s'
    else:
        s=s+c.value
        s=s+d.value
        s=s+'o'
        t=t+c.value
        t=t+d.value
        t=t+'o'
    p.u=s
    p.v=t
    return s,t

def readInitialHand():
    file0=pd.read_csv('file1.csv',header=None)
    i=0
    q=len(file0)
    while ( i<q ):
        reflop.append(file0[0][i])
        #print(reflop[i])
        i+=1
    file= open('file3.csv', 'r')
    Lines = file.readlines()
    i=0
    q=len(Lines)
    while (i<169):
        val[i]= float(Lines[i])
        #print( reflop[i] , " " , val[i])
        i+=1
    file.close()
    #reflop=reflop[168:]
    #print(val)




def compareCards(card1, card2):
    return card1.rank - card2.rank



class Deck:    
   
    
    # cards = [ Card(0,0) for i in range(52) ]
    def __init__(self):
        # cards = [ Card(0,0) for i in range(52) ]
        # global cards
        self.cards = [ Card() for i in range(52) ]
        for i in range(4):
            for j in range(13):
                self.cards[i*13+j].suit = i
                self.cards[i*13+j].rank = j

        # return cards
        suits[0] = "D"
        suits[1] = "S"
        suits[2] = "H"
        suits[3] = "C"
        ranks[0] = "2"
        ranks[1] = "3"
        ranks[2] = "4"
        ranks[3] = "5"
        ranks[4] = "6"
        ranks[5] = "7"
        ranks[6] = "8"
        ranks[7] = "9"
        ranks[8] = "T"
        ranks[9] = "J"
        ranks[10] = "Q"
        ranks[11] = "K"
        ranks[12] = "A"
    

    def print(self):
        print("Printing the deck...")
        # sleep(1);
        time.sleep(1)
        for i in range(52):
            print(ranks[self.cards[i].rank], suits[self.cards[i].suit])


    def shuffle(self):
            self.top = 51
            
            tempCard = Card()

            for i in range(4):
                for j in range(13):
                    self.cards[i*13+j].suit = i
                    self.cards[i*13+j].rank = j

            
            print("Shuffling the cards and dealing...")
            # sleep(2);
            time.sleep(2)

            for i in range(52):
                x = random.randint(0,100) % 52
                tempCard = self.cards[i]
                self.cards[i] = self.cards[x]
                self.cards[x] = tempCard


    def hitme(self):
        self.top = self.top-1
        return self.cards[self.top+1]



class Player:
    def __init__(self):
        self.name = None
        self.money = None
        self.playing = None
        self.round1=None
        self.goodToGo=None
        self.cards = [ Card() for i in range(2) ]

# class Poker_Game:

class Poker_Game:
    def __init__(self):
        self.players=[ Player() for i in range(6) ]
        self.deck1= Deck()
        self.bind=None
        self.tableCards=[ Card() for i in range(5) ]
        self.pot=None
        self.action=None
        self.bet=None
        self.rational=None
        self.betOn=None
        self.winner=None
        self.maxPoints=None
        self.roundWinner=None
        self.handPoints=[0]*6
        self.bestHand=[[0]*3]*6

    def playersLeft(self):
            count = 0;
            for i in range(6):
                if (self.players[i].money>0):
                    count+=1
            return count
        

    def computerAction(self,playerNum,b,p):
        hand=[0]*5
        
        if((b+p)>0):
            po=b/(p+b)
        hand[0]=cardToIndex(self.players[playerNum].cards[0]);
        hand[1]=cardToIndex(self.players[playerNum].cards[1]);
        hand[2]=cardToIndex(self.tableCards[0]);
        hand[3]=cardToIndex(self.tableCards[1]);
        hand[4]=cardToIndex(self.tableCards[2]);
        E=EHS(hand)
        d=E-po
        if (d>0): 
            return 2
        if (d==0):
            return 1
        if (d<0):
            return 0
# =============================================================================
#         if (self.players[playerNum].cards[0].rank < 8 and self.players[playerNum].cards[1].rank < 8):
#             if (self.players[playerNum].cards[0].rank!=self.players[playerNum].cards[1].rank):
#                 return 0
#             else:
#                 return 1
#         
#         elif (self.players[playerNum].cards[0].rank < 10 and self.players[playerNum].cards[1].rank < 10):
#             if (self.players[playerNum].cards[0].rank!=self.players[playerNum].cards[1].rank):
#                 return 1
#             else:
#                 return 2
#         
#         else:
#             return 2
# =============================================================================
        
    

    #checks if someone still got bet/call
    def playersToBet(self):
        for i in range(6):
            if (self.players[i].round1==1 and self.players[i].goodToGo==0):
                return 1

        return 0


    def takeBets(self):
            self.betOn = 0
            for k in range(6):
                self.players[k].goodToGo = 0
            winp=0.0
            for k in range(self.bind+1,self.bind+7): 
                # human player actions 
                if (k%6==4 and self.players[4].round1):
                    if (self.betOn):
                        #print("Your action: (1) FLOP (3) BET/CALL ")
                        self.action=int(input("Your action: (1) FLOP (3) BET/CALL "))
                        while (self.action!=1 and self.action!=3):
                            print("Invalid number pressed.")
                            print("Your action: (1) FLOP (3) BET/CALL ")
                            self.action=int(input())
                    else:
                        print("Your action: (1) FLOP (2) CHECK (3) BET/CALL ")
                        self.action=int(input())
                        while (self.action<1 or self.action>3):
                            print("Invalid number pressed.")
                            print("Your action: (1) FLOP (2) CHECK (3) BET/CALL ")
                            self.action=int(input())

                    if (self.action==1):
                        self.players[4].round1 = 0
                    elif(self.action==2):
                        continue
                    else:
                        if (self.betOn):
                            self.pot+=self.betOn
                            self.players[4].money-=self.betOn
                            self.players[4].goodToGo = 1
                        else:
                            print("How much do you want to bet: ")
                            self.bet=int(input())
                            if(self.players[4].money!=0):
                                while (self.bet> self.players[4].money or self.bet<1):
                                    print("Invalid number to bet.")
                                    print("How much do you want to bet: ")
                                    self.bet=int(input())
                            else:
                                print("You have no money to bet")
                                self.bet=0;
                            self.pot+=self.bet;
                            self.players[4].money-=self.bet;
                            self.betOn = self.bet;
                            self.players[4].goodToGo = 1;
                        
                    
                

                #computers actions
                else:
                    if (self.players[k%6].round1==0):
                        continue
                    self.rational = random.randint(0,32767) % 2;
                    if (self.rational):
                        #self.action = self.computerAction(k%6)
                        if(self.tableCards[3].rank == -1):
                             i=cardToIndex(self.players[k%6].cards[0]);
                             j=cardToIndex(self.players[k%6].cards[1]);
                             p=Pair()
                             s,t=cardToTable(i,j)
                             p.u=s
                             p.v=t
                             for k in range(169):
                                  #print(reflop[f],p.u)
                                  if(reflop[k]==p.u or reflop[k]==p.v):
                                      #print(val[f])
                                      winp=val[k]
                             if(winp>threshold):
                                 self.action=2
                             elif(winp<threshold):
                                 self.action=0
                             else:
                                 self.action=1
                        else:
                            self.action = self.computerAction(k%6,self.betOn,self.pot)
                        
                    else:
                        self.action = random.randint(0,32767) % 3
                    if (self.action==0):
                        self.players[k%6].round1=0
                        print(self.players[k%6].name , " flops...")
                    elif (self.action==1 and self.betOn==0):
                        print(self.players[k%6].name , " checks.")
                        continue
                    else:
                        if (self.betOn):
                            self.pot+=self.betOn
                            self.players[k%6].money -= self.betOn
                            print(self.players[k%6].name , " calls!")
                            self.players[k%6].goodToGo = 1
                        else:
                            self.bet = int(random.randint(0,32767) % (self.players[k%6].money / 3) + 10)
                            self.pot+=self.bet
                            self.players[k%6].money -= self.bet
                            print('\a')
                            print(self.players[k%6].name , " bets " , self.bet )
                            self.betOn = self.bet
                            self.players[k%6].goodToGo = 1
                        
                    
                    #sleep(1);
                    time.sleep(1)

            if (self.betOn and self.playersToBet()):
                for k in range(self.bind+1,self.bind+7):   
                    if (k%6==4):
                        if (self.players[4].round1 and self.players[4].goodToGo==0):
                            print("Your action: (1) FLOP (3) BET/CALL ")
                            self.action=int(input())
                            while (self.action!=1 and self.action!=3):
                                print("Invalid number pressed.")
                                print("Your action: (1) FLOP (3) BET/CALL ")
                                self.action=int(input())
                            if (self.action==1):
                                self.players[4].round1 = 0
                            else:
                                self.pot+=self.betOn
                                self.players[4].money-=self.betOn
                                self.players[4].goodToGo = 1

                    else:
                        if (self.players[k%6].round1==0 or self.players[k%6].goodToGo==1):
                            continue
                        self.action = random.randint(0,32767) % 2
                        if (self.action==0):
                            self.players[k%6].round1=0
                            print(self.players[k%6].name , " flops...")
                        else:
                            self.pot+=self.betOn;
                            self.players[k%6].money -= self.betOn;
                            print(self.players[k%6].name , " calls!")
                            self.players[k%6].goodToGo = 1



    def oneLeft(self):
        count = 0
        for k in range(6):
            if (self.players[k].round1):
                count+=1
        if (count==1):
            return 1
        else:
            return 0

    def getWinner(self):
        winner=0
        for k in range(6):
            if (self.players[k].round1):
                winner = k
        return winner

    def getScore(self, hand):
       
        #hand=sorted(hand,key=Card().rank)
        hand.sort(key=lambda x: x.rank)
        straight=None
        flush=None
        three=None
        four=None
        full=None
        pairs=None
        high=None
        k=None

        straight = flush = three = four = full = pairs = high = 0
        k = 0

        #checks for flush
        while (k<4 and hand[k].suit==hand[k+1].suit):
            k+=1
        if (k==4):
            flush = 1

        #checks for straight
        k=0
        while (k<4 and hand[k].rank==hand[k+1].rank-1):
            k+=1
        if (k==4):
            straight = 1

        #checks for fours 
        for i in range(2):
            k = i
            while (k<i+3 and hand[k].rank==hand[k+1].rank):
                k+=1
            if (k==i+3):
                four = 1
                high = hand[i].rank

        #checks for threes and fullhouse
        if (not four):
            for i in range(3):
                k = i
                while (k<i+2 and hand[k].rank==hand[k+1].rank):
                    k+=1
                if (k==i+2):
                    three = 1
                    high=hand[i].rank
                    if (i==0):
                        if (hand[3].rank==hand[4].rank):
                            full=1;
                    elif(i==1):
                        if (hand[0].rank==hand[4].rank):
                            full=1;
                    else:
                        if (hand[0].rank==hand[1].rank):
                            full=1

        if (straight and flush):
            return 170 + hand[4].rank
        elif(four):
            return 150 + high
        elif(full):
            return 130 + high
        elif(flush):
            return 110
        elif(straight):
            return 90 + hand[4].rank
        elif(three):
            return 70 + high

        #checks for pairs
        for k in range(4):
            if (hand[k].rank==hand[k+1].rank):
                pairs+=1
                if (hand[k].rank>high):
                    high = hand[k].rank

        if (pairs==2):
            return 50 + high
        elif(pairs):
            return 30 + high
        else:
            return hand[4].rank

    def tryHand(self,array, player):
        hand=[Card() for i in range(5)]

        #get cards from table and player
        for i in range(1,4):
            hand[i-1] = self.tableCards[array[i]]

        for i in range(2):
            hand[i+3] = self.players[player].cards[i]

        return self.getScore(hand)

    def evaluateHands(self):
        stack=[0]*10
        k=None
        currentPoints=None

        for q in range(6):
            if (self.players[q].round1):
                stack[0]=-1; #-1 is not considered as part of the set
                k = 0
                while(1):
                    if (stack[k]<4):
                        stack[k+1] = stack[k] + 1
                        k+=1
                    else:
                        stack[k-1]+=1
                        k-=1
                    if (k==0):
                        break

                    if (k==3):
                        currentPoints = self.tryHand(stack,q)
                        if (currentPoints>self.handPoints[q]):
                            self.handPoints[q] = currentPoints
                            for x in range(3):
                                self.bestHand[q][x] = stack[x+1];
    

    #end of evaluateHands() */

    def printWinningHand(self,winner):
        winningHand=[Card() for i in range(5)]
        for i in range(3):
            winningHand[i] = self.tableCards[self.bestHand[winner][i]]

        for i in range(2):
            winningHand[i+3] = self.players[winner].cards[i]

        winningHand.sort(key=lambda x: x.rank)

        print("   The winning hand:")
        print("   ___   ___   ___   ___   ___")
        print("  | " , ranks[winningHand[0].rank] , " | | " , ranks[winningHand[1].rank] , " | | " , ranks[winningHand[2].rank] , " | | " , ranks[winningHand[3].rank] , " | | " , ranks[winningHand[4].rank] , " |")
        print("  | " , suits[winningHand[0].suit] , " | | " , suits[winningHand[1].suit] , " | | " , suits[winningHand[2].suit] , " | | " , suits[winningHand[3].suit] , " | | " , suits[winningHand[4].suit] , " |")
        print("  |___| |___| |___| |___| |___|")
        
        #sleep(3);
        time.sleep(3)

    #main gameplay function
    def startGame(self):
        i = 0

        while(self.playersLeft()>1):
            #starting default values
            for z in range(6):
                if (self.players[z].money<1):
                    self.players[z].playing = 0
                    self.players[z].round1 = 0
            for z in range(6):
                if (self.players[z].playing):
                    self.players[z].round1 = 1
                self.handPoints[z]=-1
            for x in range(6):
                for y in range(3):
                    self.bestHand[x][y] = -1

            #checking for game over
            if(self.players[4].playing==0):
                print("You are out of money, sorry.")
                print("Game over.")
                break

            self.bind = i % 6

            #paying bind
            self.pot = 20;
            if (self.players[self.bind].money>=20):
                self.players[self.bind].money-=20
            else:
                self.players[self.bind].playing = 0

            print("Get ready for round " , (i+1) , "...")
            #sleep(1)
            time.sleep(1)
            #random.shuffle(self.deck1)
            self.deck1.shuffle()
            #pre-flop
            self.deal()
            self.printTable()
            self.takeBets()
            if (self.oneLeft()):
                self.winner = self.getWinner()
                print(self.players[self.winner].name , " wins $" , self.pot)
                i+=1
                continue

            #flop
            self.flop()
            #
            self.printTable()
            self.takeBets()
            if (self.oneLeft()):
                self.winner = self.getWinner()
                print(self.players[self.winner].name , " wins $" , self.pot)
                i+=1
                continue

            #turn
            self.turn()
           
            self.printTable()
            self.takeBets()
            if (self.oneLeft()):
                self.winner = self.getWinner()
                print(self.players[self.winner].name , " wins $" , self.pot)
                i+=1
                continue
            

            #river
            self.river()
            
            self.printTable()
            self.takeBets()

            self.evaluateHands()

            #find and declare round winner
            maxPoints = 0
            for q in range(6):
                if(self.players[q].round1):
                    if (self.handPoints[q]>maxPoints):
                        maxPoints = self.handPoints[q]
                        self.roundWinner = q
            
            print(self.players[self.roundWinner].name , " wins $" , self.pot , " with ")
            if (maxPoints<30):
                print("HIGH CARD")
            elif (maxPoints<50):
                print("SINGLE PAIR")
            elif (maxPoints<70):
                print("TWO PAIRS")
            elif (maxPoints<90):
                print("THREE OF A KIND")
            elif(maxPoints<110):
                print("STRAIGHT")
            elif(maxPoints<130):
                print("FLUSH")
            elif(maxPoints<150):
                print("FULL HOUSE")
            elif(maxPoints<170):
                print("FOUR OF A KIND")
            else:
                print("STRAIGHT FLUSH")
            

            self.printWinningHand(self.roundWinner)

            self.players[self.roundWinner].money+=self.pot

            i+=1



    #public functions and variables
    def start(self,name):
        for i in range(6):
            self.players[i].money=1000
            self.players[i].playing=1
        self.players[0].name = "Souraj"
        self.players[1].name = "Ayush"
        self.players[2].name = "Rahul"
        self.players[3].name = "Anmol"
        self.players[4].name = name
        self.players[5].name = "Sourav"
        self.startGame()


    def deal(self):
            for i in range(6):
                for j in range(2):
                    if (self.players[i].playing):
                        self.players[i].cards[j] = self.deck1.hitme()
        
            for i in range(5):
                self.tableCards[i].rank=-1

    def flop(self):
        for i in range(3):
            self.tableCards[i] = self.deck1.hitme()

    def turn(self):
        self.tableCards[3] = self.deck1.hitme()

    def river(self):
        self.tableCards[4] = self.deck1.hitme()

    
    def printTable(self):
        print("  " ,self.players[0].name if self.players[0].playing else "      " , "         " ,self.players[1].name if self.players[1].playing else "     " , "           ",self.players[2].name if self.players[2].playing else "    ")
# =============================================================================
#         print("   $", setw(4) ,self.players[0].money if self.players[0].playing else 0 , "         $" , setw(4) , self.players[1].money if self.players[1].playing else 0,"           $" ,setw(4) ,self.players[2].money if self.players[2].playing else 0)
# =============================================================================
        print("   $",'{:>4}'.format(self.players[0].money) if self.players[0].playing else '{:>2}'.format(0) , "         $" , '{:>4}'.format(self.players[1].money) if self.players[1].playing else '{:>2}'.format(0),"           $" ,'{:>4}'.format(self.players[2].money) if self.players[2].playing else '{:>4}'.format(0))
        print("     _____________________________")
        print("    / " ,"@" if self.bind==0 else " ", "            " , "@" if self.bind==1 else " " , "            " , "@" if self.bind==2 else " " , " \\")
        print("   /  ___   ___   ___   ___   ___  \\")
        print("   | | " ,ranks[self.tableCards[0].rank] if (self.tableCards[0].rank)>=0 else " " , " | | " , ranks[self.tableCards[1].rank] if (self.tableCards[1].rank)>=0 else " "  , " | | " , ranks[self.tableCards[2].rank] if (self.tableCards[2].rank)>=0 else " "  , " | | ",ranks[self.tableCards[3].rank] if (self.tableCards[3].rank)>=0 else " " , " | | " , ranks[self.tableCards[4].rank] if (self.tableCards[4].rank)>=0 else " "  , " | |")
        print("   | | " , suits[self.tableCards[0].suit] if (self.tableCards[0].rank)>=0 else " ", " | | " , suits[self.tableCards[1].suit] if (self.tableCards[1].rank)>=0 else " " , " | | " , suits[self.tableCards[2].suit] if (self.tableCards[2].rank)>=0 else " " , " | | ",suits[self.tableCards[3].suit] if (self.tableCards[3].rank)>=0 else " ", " | | " , suits[self.tableCards[4].suit] if (self.tableCards[4].rank)>=0 else " ", " | |")
        print("   | |___| |___| |___| |___| |___| |")
        print("   |                               |")
# =============================================================================
#         print("   |          Pot = $" , setw(4) , self.pot , "         |")
# =============================================================================
        print("   |          Pot = $" , self.pot , "         |")
        print("   \\                               /")
        print("    \\_" , "@" if self.bind==5 else "_" , "_____________" , "@" if self.bind==4 else "_" , "___________" , "@" if self.bind==3 else "_" , "_/")
        print("  " , self.players[5].name if self.players[5].playing else "      " , "          " , self.players[4].name if self.players[4].playing else "      ", "         ",self.players[3].name if self.players[3].playing else "      ")
# =============================================================================
#         print("   $" , setw(4) ,self.players[5].money if self.players[5].playing else  0 , "          $" , setw(4) , self.players[4].money if self.players[4].playing else  0,"         $" , setw(4) , self.players[3].money if self.players[3].playing else  0)
# =============================================================================
        print("   $" ,self.players[5].money if self.players[5].playing else  0 , "          $" , self.players[4].money if self.players[4].playing else  0,"         $" , self.players[3].money if self.players[3].playing else  0)
        if (self.players[4].round1):
            print("   Your hand:")
            print("    ___    ___")
            print("   | " , ranks[self.players[4].cards[0].rank] , "|  | " , ranks[self.players[4].cards[1].rank] , " |")
            print("   | " , suits[self.players[4].cards[0].suit] , "|  | " , suits[self.players[4].cards[1].suit] , " |")
            print("   |___|  |___|")
        
        #sleep(3)
        time.sleep(3)



def cardToIndex(card):
  s=''
  c=''
  i=0
  #print(card.suit, card.rank)
  if(card.suit==0):
    s='d'
  if(card.suit==1):
    s='h'
  if(card.suit==2):
    s='s'
  if(card.suit==3):
    s='c'
  if(card.rank==0):
    c='2'
  if(card.rank==1):
    c='3'
  if(card.rank==2):
    c='4'
  if(card.rank==3):
    c='5'
  if(card.rank==4):
    c='6'
  if(card.rank==5):
    c='7'
  if(card.rank==6):
    c='8'
  if(card.rank==7):
    c='9'
  if(card.rank==8):
    c='T'
  if(card.rank==9):
    c='J'
  if(card.rank==10):
    c='Q'
  if(card.rank==11):
    c='K'
  if(card.rank==12):
    c='A'

  i=finddeckindex(s,c)
  
  return i

threshold=50
def main():
    name=None
    game1=Poker_Game()
    
    readInitialHand()
    random.seed(time.time())
    print("Welcome to...")
    #sleep(0.2);
    time.sleep(0.2)
    print("#######                        ###### ")
    print("   #    ###### #    # #####    #     #  ####  #    # ###### #####")
    print("   #    #       #  #    #      #     # #    # #   #  #      #    #")
    print("   #    #####    ##     #      ######  #    # ####   #####  #    #")
    print("   #    #        ##     #      #       #    # #  #   #      #####")
    print("   #    #       #  #    #      #       #    # #   #  #      #   #")
    print("   #    ###### #    #   #      #        ####  #    # ###### #    #")

    #print("Please type your name: ",end=" ")

    name=input("Please type your name: ")

    print("OK " , name , " let's play some poker!")
    #sleep(2)
    time.sleep(2)
    game1.start(name)

if __name__ == "__main__":
    main()




