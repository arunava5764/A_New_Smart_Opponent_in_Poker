import poker_constants
import constants
deck=[0]*52

import sys
def fprintf(stream, format_spec, *args):
    stream.write(format_spec % args)


def findit( key ):
    low = 0
    high = 4887 #mid

    while ( low <= high ):
        mid = (high+low) >> 1      #divide by two
        if ( key < constants.products[mid] ):
            high = mid - 1
        elif ( key > constants.products[mid] ):
            low = mid + 1
        else:
            return mid 
    
    print( "ERROR:  no match found; key = ", key )
    return -1 

def init_deck( deck ):
    n = 0
    suit = 0x8000
    for i in range(4):
        
        for j in range(13):
            deck[n] = constants.primes[j] | j << 8 | suit | (1 << (16+j))
            n += 1
        suit = suit >> 1
    
    return deck

# def eval_5cards(c1,c2,c3,c4,c5):
#     # q,s;
#     q = (c1|c2|c3|c4|c5) >> 16

#     ''' check for Flushes and StraightFlushes '''
#     if ( c1 & c2 & c3 & c4 & c5 & 0xF000 ):
# 	    return constants.flushes[q] 

#     ''' check for Straights and HighCard hands '''

#     s = constants.unique5[q]
#     if  s :  return  s  

#     ''' let's do it the hard way '''

#     q = (c1&0xFF) * (c2&0xFF) * (c3&0xFF) * (c4&0xFF) * (c5&0xFF)
def find_card(rank, suit, deck):
    for i in range(52):
        c=deck[i]
        if (c & suit) and (poker_constants.RANK(c)==rank):
            return i
    return -1

def print_hand(hand,n):
    rank="23456789TJQKA"
    for i in range(n):
        r=(hand>>8) & 0xF
        if hand & 0x8000:
            suit='c'
        elif ( hand & 0x4000 ):
            suit='d'
        elif ( hand & 0x2000 ):
            suit='h'
        else:
            suit='s'

        print( rank[r], suit )
        hand+=1


def hand_rank( val ):
    if (val > 6185): 
        return(poker_constants.HIGH_CARD)        # 1277 high card
    if (val > 3325):
        return(poker_constants.ONE_PAIR)         # 2860 one pair
    if (val > 2467): 
        return(poker_constants.TWO_PAIR)         #  858 two pair
    if (val > 1609): 
        return(poker_constants.THREE_OF_A_KIND)  #  858 three-kind
    if (val > 1599): 
        return(poker_constants.STRAIGHT)         #   10 straights
    if (val > 322):  
        return(poker_constants.FLUSH)            # 1277 flushes
    if (val > 166):  
        return(poker_constants.FULL_HOUSE)       #  156 full house
    if (val > 10):   
        return(poker_constants.FOUR_OF_A_KIND)   #  156 four-kind
    return(poker_constants.STRAIGHT_FLUSH)       #   10 straight-flushes


def eval_5cards(c1,c2,c3,c4,c5):
    # q,s;
    q = (c1|c2|c3|c4|c5) >> 16

    ''' check for Flushes and StraightFlushes '''
    if ( c1 & c2 & c3 & c4 & c5 & 0xF000 ):
        return constants.flushes[q] 

    ''' check for Straights and HighCard hands '''

    s = constants.unique5[q]
    if  s :  return  s  

    ''' let's do it the hard way '''

    q = (c1&0xFF) * (c2&0xFF) * (c3&0xFF) * (c4&0xFF) * (c5&0xFF)


    q = findit( q )

    return constants.values[q]

def eval_5hand(hand):
    #int c1, c2, c3, c4, c5;
    hand[0]+=1
    c1 = hand[0]  #c1 = *hand++;
    hand[0]+=1
    c2 = hand[0]  #c2 = *hand++;
    hand[0]+=1
    c3 = hand[0]  #c3 = *hand++;
    hand[0]+=1
    c4 = hand[0]  #c4 = *hand++;
    c5 = hand[0]     #c5 = *hand;

    return eval_5cards(c1,c2,c3,c4,c5)



def eval_7hand( hand ):
    #int i, j, q, 
    best = 9999
    subhand=[0]*5

    for i in range(21):  #( i = 0; i < 21; i++ )
        for j in range(5):  #( j = 0; j < 5; j++ )
            subhand[j] = hand[ constants.perm7[i][j] ]
        q = eval_5hand( subhand )
        if ( q < best ):
            best = q
    return best

def finddeckindex(suit , card):
    #int s ,c
    if (suit=='c'):
        s=0
    elif (suit=='d'):
        s=1
    elif (suit=='h'):
        s=2
    else:
        s=3

    if (card=='A'):
        c=12
    elif (card=='K'):
        c=11
    elif (card=='Q'):
        c=10
    elif (card=='J'):
        c=9
    elif (card=='T'):
        c=8
    else:
        c=(ord(card)-ord('0'))-2

    return s*13+c




def handStrength(n1,n2,n3,n4,n5):
    #int c1, c2, c3, c4, c5,m,n;
    #int opprank,ourrank;
    #float strength,a,b,c,e;
    #print("\n ok till here 2 \n");


    c1 = deck[n1]
    c2 = deck[n1]
    c3 = deck[n3]
    c4 = deck[n4]
    c5 = deck[n5]

    ourrank=eval_5cards(c1,c2,c3,c4,c5)
    #print("\n ok till here 3 \n");
    ahead=0
    tied=0
    behind=0
    #handstrength=0;

    for i in range(52):   #(int i=0;i<52;i++)
        for j in range(i+1, 52):   #(int j=i+1;j<52;j++)
            if i==n1 or i==n2 or i==n3 or i==n4 or i==n5 or j==n1 or j==n2 or j==n3 or j==n4 or j==n5:
                continue
            else:
                m=deck[i]
                n=deck[j]
                opprank=eval_5cards(m,n,c3,c4,c5)
                if opprank<ourrank:
                    ahead+=1
                elif ourrank==opprank:
                    tied+=1
                else:
                    behind+=1

        
    
    print("ahead  is ",  ahead)
    print("tied   is ",  tied)
    print("behind is ",  behind)
    a=tied/2
    b=ahead+a
    c=ahead+tied+behind
    e=b/c

    strength=e
    print("strength is ",  strength)

    return strength



def Ppot(hand):
    HP=[[0]*3]*3
    HPTotal=[0]*3
    hand7=[0]*7
    #float p1,p2,p3,p4,p5,p6,p7,p8,p9;
    #int m,n,u,v,ourrank,opprank,index,oppbest,ourbest,c1,c2,count;
    hand7[0]=deck[hand[0]]
    hand7[1]=deck[hand[1]]
    hand7[2]=deck[hand[2]]
    hand7[3]=deck[hand[3]]
    hand7[4]=deck[hand[4]]
    c1=hand7[0]
    c2=hand7[1]

    HPTotal[0]=0
    HPTotal[1]=0
    HPTotal[2]=0
    for a in range(3):  #(int a=0;a<3;a++)
        for b in range(3):  #(int b=0;b<3;b++)
            HP[a][b]=0

    ourrank=eval_5cards(hand7[0],hand7[1],hand7[2],hand7[3],hand7[4])
    print("ourrank ",ourrank)
    count=0
    for i in range(52):  #(int i=0;i<52;i++)
        if (i==hand[0] or i==hand[1] or i==hand[2] or i==hand[3] or i==hand[4] ):
            continue
        for j in range(i+1,52):  #(int j=i+1;j<52;j++)
            if (j==hand[0] or j==hand[1] or j==hand[2] or j==hand[3] or j==hand[4]):
                continue
            else:
                count+=1
                m=deck[i]
                n=deck[j]
                opprank=eval_5cards(m,n,hand7[2],hand7[3],hand7[4])
                #print("5 is ok\n")
                if (opprank<ourrank):
                    index=0
                elif (ourrank==opprank):
                    index=1
                else:
                    index=2
                HPTotal[index]+=1

                for k in range(52):  #(int k=0;k<52;k++)
                    if (k==hand[0] or k==hand[1] or k==hand[2] or k==hand[3] or k==hand[4] or k==i or k==j):
                        continue
                    for l in range(k+1,52):  #(int l=k+1;l<52;l++)
                        if (l==hand[0] or l==hand[1] or l==hand[2] or l==hand[3] or l==hand[4] or l==i or l==j):
                            continue
                        else:
                            hand7[0]=c1
                            hand7[1]=c2
                            hand7[5]=deck[k]
                            hand7[6]=deck[l]
                            ourbest=eval_7hand(hand7)
                            #print(" ourbest ",ourbest)
                            hand7[0]=m
                            hand7[1]=n
                            oppbest=eval_7hand(hand7)
                            #print("7 is ok \n")
                            #if(oppbest<ourbest):
                                #print(" oppbest ",oppbest)
                            if (oppbest<ourbest):
                                HP[index][0]+=1
                            elif (ourbest==oppbest):
                                HP[index][1]+=1
                            else:
                                HP[index][2]+=1
                     
    print(count,"count \n")

    p1=float(HP[1][2])/2;
    p2=float(HP[0][1])/2;
    p3=float(HP[0][2]);
    p4=float(HP[0][1])+float(HP[0][0])+float(HP[0][2]);
    p5=float(HP[1][0])+float(HP[1][1])+float(HP[1][2]);
    if (p4>0):
        p6=p2/p4
        p7=p3/p4
    else:
        p6=0
        p7=0
    if(p5>0):
        p8=p1/p5
    else:
        p8=0
    p9=p6+p7+p8
    print(p1,":p1 ",p2,":p2 ",p3,":p3 ",p4,":p4 \n",p5,":p5 ",p6,":p6 ",p7,":p7 ",p8,":p8 ",p9,":p9 ")

    return p8



def Npot(hand):
    HP=[[0]*3]*3
    HPTotal=[0]*3
    hand7=[0]*7
    #float p1,p2,p3,p4,p5,p6,p7,p8,p9;
    #int m,n,u,v,ourrank,opprank,index,oppbest,ourbest,c1,c2,count;
    hand7[0]=deck[hand[0]]
    hand7[1]=deck[hand[1]]
    hand7[2]=deck[hand[2]]
    hand7[3]=deck[hand[3]]
    hand7[4]=deck[hand[4]]
    c1=hand7[0]
    c2=hand7[1]

    HPTotal[0]=0
    HPTotal[1]=0
    HPTotal[2]=0
    for a in range(3):  #(int a=0;a<3;a++)
        for b in  range(3):  #(int b=0;b<3;b++)
            HP[a][b]=0
    ourrank=eval_5cards(hand7[0],hand7[1],hand7[2],hand7[3],hand7[4])
    print("ourrank ",ourrank)
    count=0
    for i in range(52):   #(int i=0;i<52;i++)
        if (i==hand[0] or i==hand[1] or i==hand[2] or i==hand[3] or i==hand[4] ):
            continue
        for j in range(i+1,52):  #(int j=i+1;j<52;j++)
            if (j==hand[0] or j==hand[1] or j==hand[2] or j==hand[3] or j==hand[4]):
                continue
            else:
                count+=1
                m=deck[i]
                n=deck[j]
                opprank=eval_5cards(m,n,hand7[2],hand7[3],hand7[4])
                #print("5 is ok\n")
                if (opprank<ourrank):
                    index=0
                elif (ourrank==opprank):
                    index=1
                else:
                    index=2
                HPTotal[index]+=1

                for k in range(52):  #(int k=0;k<52;k++)
                    if (k==hand[0] or k==hand[1] or k==hand[2] or k==hand[3] or k==hand[4] or k==i or k==j): 
                        continue
                    for l in range(k+1,52):  #(int l=k+1;l<52;l++)
                        if (l==hand[0] or l==hand[1] or l==hand[2] or l==hand[3] or l==hand[4] or l==i or l==j):
                            continue
                        else:
                            hand7[0]=c1
                            hand7[1]=c2
                            hand7[5]=deck[k]
                            hand7[6]=deck[l]
                            ourbest=eval_7hand(hand7)
                            #print(" ourbest ",ourbest)
                            hand7[0]=m
                            hand7[1]=n
                            oppbest=eval_7hand(hand7)
                            #print("7 is ok \n")
                            #if (oppbest<ourbest):
                                #print(" oppbest ",oppbest)
                            if (oppbest<ourbest):
                                HP[index][0]+=1
                            elif (ourbest==oppbest):
                                HP[index][1]+=1
                            else:
                                HP[index][2]+=1
                            
                     
                
            
        
    

    print(count,"count \n")
    p1=float(HP[2][1])/2
    p2=float(HP[1][0])/2
    p3=float(HP[2][0])
    p4=float(HP[2][1])+float(HP[2][0])+float(HP[2][2])
    p5=float(HP[1][0])+float(HP[1][1])+float(HP[1][2])
    if (p4>0):
        p6=p1/p4
        p7=p3/p4    
    else:
        p6=0
        p7=0
    if (p5>0):
        p8=p2/p5
    else:
        p8=0
    p9=p6+p7+p8
    print(p1,":p1 ",p2,":p2 ",p3,":p3 ",p4,":p4 \n",p5,":p5 ",p6,":p6 ",p7,":p7 ",p8,":p8 ",p9,":p9 ")
    return p8

def EHS(hand):
    #int c1,c2,c3,c4,c5;
    #float S,P,N,E;
    c1=hand[0]
    c2=hand[1]
    c3=hand[2]
    c4=hand[3]
    c5=hand[4]
    S=handStrength(c1,c2,c3,c4,c5)
    P=Ppot(hand)
    N=Npot(hand)
    E=S*(1-N)+(1-S)*P
    return E

    # q = findit( q );

    # return values[q] 


# res = init_deck([0]*52)

# print('res',res)

