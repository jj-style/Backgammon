import random
def getSpikeFromNumber(target_no,Board):
    i = 0
    k = 0
    while i < 2:
        while k < 12:
            if Board[i][k].getSpikeNo() == target_no:
                return Board[i][k]
            k+=1
        i+=1
        k=0

def getOpenPieces(Board,Game):
    open_pieces = []
    for i in range(2):
        for k in range(12):
            if Board[i][k].getNumberOfPieces() == 1 and Board[i][k].getContainsColor() == Game.getTurn():
                open_pieces.append(Board[i][k])
    return open_pieces

def canSafelyMoveOpenPiece(open_pieces,Board,Game,Dice):
    if len(open_pieces) == 0: return False,False
    safe_moves = []
    open_pieces_length = len(open_pieces)
    roll_list_length = len(Dice.getRollList())
    piece_count = 0
    dice_count = 0
    while piece_count < open_pieces_length:
        while dice_count < roll_list_length:
            number = Dice.getRollList()[dice_count]
            if Game.getTurn() == Game.AIColor: number*=-1
            temp_piece = open_pieces[piece_count]
            temp_dest = temp_piece.getSpikeNo() + number
            if temp_dest < 1 or temp_dest > 24:
                dice_count+=1
                continue
            temp_dest = getSpikeFromNumber(temp_dest,Board)
            if temp_dest.getContainsColor() == Game.getTurn():
                safe_moves.append([temp_piece,temp_dest])
            dice_count += 1
        piece_count+=1
        dice_count = 0
    if len(safe_moves) == 0:
        return False,False
    else:
        move = random.choice(safe_moves)
        piece = move[0]
        dest = move[1]
        return piece,dest
        
def canSafelyCoverOpenPiece(open_pieces,Board,Game,Dice):
    if len(open_pieces) == 0: return False,False
    safe_moves = []
    more_than_two = []
    for i in range(2):
        for k in range(12):
            if Board[i][k].getContainsColor() == Game.getTurn() and Board[i][k].getNumberOfPieces() >=3:
                more_than_two.append(Board[i][k])               
    more_than_two_length = len(more_than_two)
    roll_list_length = len(Dice.getRollList())
    piece_count = 0
    dice_count = 0
    while piece_count < more_than_two_length:
        while dice_count < roll_list_length:
            number = Dice.getRollList()[dice_count]
            if Game.getTurn() == Game.AIColor: number*=-1
            temp_piece = more_than_two[piece_count]
            temp_dest = temp_piece.getSpikeNo() + number
            if temp_dest < 1 or temp_dest > 24:
                dice_count+=1
                continue
            temp_dest = getSpikeFromNumber(temp_dest,Board)
            if temp_dest.getContainsColor() == Game.getTurn() and temp_dest in open_pieces:
                safe_moves.append([temp_piece,temp_dest])
            dice_count+=1
        piece_count+=1
        dice_count = 0
    if len(safe_moves) == 0:
        return False,False
    else:
        move = random.choice(safe_moves)
        piece = move[0]
        dest = move[1]
        return piece,dest

def canSafelyMove(Board,Game,Dice):
    safe_moves = []
    pieces = []
    for i in range(2):
        for k in range(12):
            if Board[i][k].getContainsColor() == Game.getTurn():
                pieces.append(Board[i][k])
    pieces_length = len(pieces)
    roll_list_length = len(Dice.getRollList())
    piece_count = 0
    dice_count = 0
    while piece_count < pieces_length:
        while dice_count < roll_list_length:
            number = Dice.getRollList()[dice_count]
            if Game.getTurn() == Game.AIColor: number*=-1
            temp_piece = pieces[piece_count]
            temp_dest = temp_piece.getSpikeNo() + number
            if temp_dest < 1 or temp_dest > 24:
                dice_count+=1
                continue
            temp_dest = getSpikeFromNumber(temp_dest,Board)
            if temp_dest.getContainsColor() == Game.getTurn():
                safe_moves.append([temp_piece,temp_dest])
            dice_count +=1
        piece_count+=1
        dice_count = 0
    if len(safe_moves) == 0:
        return False,False
    else:
        move = random.choice(safe_moves)
        piece = move[0]
        dest = move[1]
        return piece,dest

def canMoveDoubleMoveSafely(Board,Game,Dice):
    if len(Dice.getRollList()) != 2:
        return False,False
    safe_moves = []
    i = 0
    k = 0
    while i < 2:
        while k < 12:
            if Board[i][k].getContainsColor() == Game.getTurn():
                piece = Board[i][k]
                combined_roll = Dice.getRollList()[0] + Dice.getRollList()[1]
                if Game.getTurn() == Game.AIColor: combined_roll *=-1
                double_dest = piece.getSpikeNo() + combined_roll
                if double_dest <= 24 and double_dest >= 1:
                    double_dest_spike = getSpikeFromNumber(double_dest,Board)
                    if double_dest_spike.getContainsColor() == Game.getTurn():
                        count = 0
                        while count < 2:
                            number = Dice.getRollList()[count]
                            if Game.getTurn() == Game.AIColor: number*=-1
                            single_dest = getSpikeFromNumber(piece.getSpikeNo() + number,Board)
                            if single_dest.getContainsColor() in [Game.getTurn(),None] or (single_dest.getContainsColor() not in [Game.getTurn(),None] and single_dest.getNumberOfPieces() == 1):
                                safe_moves.append([piece,single_dest])
                            count+=1
            k+=1
        i+=1
        k=0
    if len(safe_moves) == 0:
        return False,False
    else:
        move = random.choice(safe_moves)
        piece = move[0]
        dest = move[1]
        return piece,dest

def canMakeDoubleSeperateMoveSafely(Board,Game,Dice):
    if len(Dice.getRollList()) != 2:
        return False,False
    safe_moves = []
    i = 0
    k = 0
    while i < 2:
        while k < 12:
            if Board[i][k].getContainsColor() == Game.getTurn():
                piece = Board[i][k]
                attempt = 0
                first_roll_num = 0
                second_roll_num = 1
                while attempt < 2:
                    first_roll = Dice.getRollList()[first_roll_num]
                    if Game.getTurn() == Game.AIColor: first_roll*=-1
                    first_move = piece.getSpikeNo() + first_roll
                    if first_move <= 24 and first_move >= 1:
                        first_move_spike = getSpikeFromNumber(first_move,Board)
                        if (first_move_spike.getContainsColor() in [Game.getTurn(),None]) or (first_move_spike.getContainsColor() != Game.getTurn() and first_move_spike.getNumberOfPieces() == 1):
                            if Game.getTurn() == Game.PlayerColor: second_roll *=-1
                            second_roll = Dice.getRollList()[second_roll_num]
                            second_move = first_move + second_roll
                            if second_move <= 24 and second_move >= 1:
                                second_move =  getSpikeFromNumber(second_move,Board)
                                if (second_move.getNumberOfPieces() > 2 or second_move.getNumberOfPieces() == 1) and second_move.getContainsColor() == Game.getTurn():
                                    safe_moves.append([piece, getSpikeFromNumber(first_move,Board)])
                    attempt +=1
                    first_roll_num = 1
                    second_roll_num = 0
            k+=1
        i+=1
        k=0
    if len(safe_moves) == 0:
        return False,False
    else:
        move = random.choice(safe_moves)
        piece = move[0]
        dest = move[1]
        return piece,dest

def canSafelyMoveBarPiece(Board,Game,Dice):
    if Game.getTurn() == Game.PlayerColor: piece_spike = 0
    else: piece_spike = 25
    average_dest = []
    best_dest = []
    for number in Dice.getRollList():
        if Game.getTurn() == Game.AIColor: number*=-1
        temp_dest = getSpikeFromNumber(piece_spike + number,Board)
        if temp_dest.getContainsColor() == Game.getTurn():
            if temp_dest.getNumberOfPieces() > 1:
                average_dest.append(temp_dest)
            elif temp_dest.getNumberOfPieces() == 1:
                best_dest.append(temp_dest)

    if len(best_dest) == 0 and len(average_dest) > 0:
        return average_dest[0]
    elif len(best_dest) > 0:
        return best_dest[0]
    else:
        return False

def evaluateSafety(dest,Board,Game):
    distances = [6,7,8]
    if Game.getTurn() == Game.PlayerColor:
        for i in range(len(distances)):
            distances[i]*=-1
    worst_threat = 0
    for i in range(len(distances)):
        if dest+distances[i] > 24 or dest+distances[i] <= 0:
            i+=1
            continue
        else:
            threat = getSpikeFromNumber(dest+distances[i],Board)
            if threat.getContainsColor() != Game.getTurn() and (threat.getNumberOfPieces() == 1 or threat.getNumberOfPieces() > 2):
                if abs(distances[i]) == 7:
                    worst_threat = 3
                elif abs(distances[i]) == 6 or abs(distances[i]) == 8:
                    if worst_threat < 2: worst_threat = 2
            else:
                if worst_threat < 1: worst_threat = 1
            i+=1
    return worst_threat
#____________________________GAME STRATEGIES____________________________#
def getHighestCurrentSpike2(rank,color,Board,Game):
    order_of_spikes = []
    if color == Game.AIColor:
        start,stop,step = 1,25,1
    else:
        start,stop,step = 24,0,-1
    for i in range(start,stop,step):
        spike = getSpikeFromNumber(i,Board)
        if spike.getContainsColor() == color:
            order_of_spikes.append(spike)
    return order_of_spikes[-rank]

def getInLateGame2(rank,Board,Game):
    black_highest = getHighestCurrentSpike2(rank,Game.PlayerColor,Board,Game).getSpikeNo()
    white_highest = getHighestCurrentSpike2(rank,Game.AIColor,Board,Game).getSpikeNo()
    return white_highest < black_highest
#__________________________MOVE_________________#
def getSafeMove(Board,Game,Dice):
    open_pieces = getOpenPieces(Board,Game)
    piece,dest = canSafelyMoveOpenPiece(open_pieces,Board,Game,Dice)
    if not piece and not dest:
        piece,dest = canSafelyCoverOpenPiece(open_pieces,Board,Game,Dice)
        if not piece and not dest:
            piece,dest = canMoveDoubleMoveSafely(Board,Game,Dice)
            if not piece and not dest:
                piece,dest = canMakeDoubleSeperateMoveSafely(Board,Game,Dice)
                if not piece and not dest:
                    piece,dest = canSafelyMove(Board,Game,Dice)
                    if not piece and not dest:
                        return False,False
    return piece,dest

