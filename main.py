from enums import Card, Position, getFullDeck
import board
import boardState
from player import Player
import playerHandle
import util
from moveObj import MoveObj
from sampleBots import *
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from multiprocessing import Process, Queue

def createPlayer(cardDeck, handSize, pos, handle):
	cards = []
	for i in range(handSize):
		n = random.randint(0, len(cardDeck)-1)
		cards.append(cardDeck[n])
		cardDeck.remove(cardDeck[n])
	return Player(handle, cards, pos)

def sortPlayers(boardState, players):
	for i in range(len(players)):
		for j in range(i + 1, len(players)):
			if util.getScore(boardState, players[j-1].pos) < util.getScore(boardState, players[j].pos):
				temp = players[j]
				players[j] = players[j-1]
				players[j-1] = temp

def multSim():
	# parameters
	numProcesses = 7
	numRunsTotal = 100
	northBot = BacktrackingBot(Position.SOUTH)
	southBot = RandomBot(Position.NORTH)
	
	# data handling
	q = Queue()
	
	# track winner
	numNorth = 0
	
	# track time
	totalTimeNorth = 0
	totalTimeSouth = 0
	startTime = 0
	lastTimePrinted = 0
	
	# extra stats
	scoreNorth = [0 for _ in range(11)]
	scoreSouth = [0 for _ in range(11)]
	cardsPlayedNorth = {}
	cardsPlayedSouth = {}
	
	print("Number of Runs:", numRunsTotal)
	print("Number of Processes:", numProcesses)
	
	processes = []
	
	for i in range(numProcesses):
		num = numRunsTotal // numProcesses
		if i < numRunsTotal % numProcesses:
			num += 1
		p = Process(target=multiProcessingHelper, args=(num, q, northBot, southBot,)) # TODO: fix numRuns/numProcesses
		p.start()
		processes.append(p)
	
	startTime = timer()
	numGathered = 0
	while numGathered < numRunsTotal:
		finalBoards, timeNorth, timeSouth = q.get()
		numGathered += 1
		# track winner
		finalBoard = finalBoards[len(finalBoards)-1]
		if getScore(finalBoard, Position.NORTH) > getScore(finalBoard, Position.SOUTH):
			numNorth += 1
		# track time
		totalTimeNorth += timeNorth
		totalTimeSouth += timeSouth
		# time update
		curTime = timer()
		if curTime - startTime - lastTimePrinted > 10:
			lastTimePrinted = curTime
			avgTimePerGame = (curTime - startTime) / numGathered * numProcesses
			print("{:.2f}".format(numGathered * 100 / numRunsTotal) + "%", end=" ")
			print(str(numNorth) + "/" + str(numGathered - numNorth), end=" ")
			print("Elapsed time:", "{:.2f}".format(curTime - startTime), "sec", end=" ")
			print("Expected time left :", "{:.2f}".format(avgTimePerGame * (numRunsTotal - numGathered) / numProcesses), "sec")
		# avg score per round
		for i in range(11):
			b = finalBoards[i]
			scoreNorth[i] += util.getScore(b, Position.NORTH)
			scoreSouth[i] += util.getScore(b, Position.SOUTH)
		# update cards
		for i in range(20):
			if finalBoard.history[i].pos.value == 0:
				if finalBoard.history[i].card in cardsPlayedNorth:
					cardsPlayedNorth[finalBoard.history[i].card][i // 2] += 1
				else:
					cardsPlayedNorth[finalBoard.history[i].card] = [0 for _ in range(10)]
					cardsPlayedNorth[finalBoard.history[i].card][i // 2] += 1
			else:
				if finalBoard.history[i].card in cardsPlayedSouth:
					cardsPlayedSouth[finalBoard.history[i].card][i // 2] += 1
				else:
					cardsPlayedSouth[finalBoard.history[i].card] = [0 for _ in range(10)]
					cardsPlayedSouth[finalBoard.history[i].card][i // 2] += 1
	for p in processes:
		p.join()
	
	# display winner
	print("Percent of times won:")
	print("north:", "{:.2f}".format(numNorth * 100 / numRunsTotal) + "%")
	print("south:", "{:.2f}".format((numRunsTotal - numNorth) * 100 / numRunsTotal) + "%")
	
	# display avg time
	print("Avg time per game:")
	print("north:", "{:.2f}".format(totalTimeNorth / numRunsTotal), "sec")
	print("south:", "{:.2f}".format(totalTimeSouth / numRunsTotal), "sec")
	
	# graphs
	# average score per round
	plt.title('Average Score per Round')
	plt.plot([x / numRunsTotal for x in scoreNorth], 'r-o', label='north')
	plt.plot([x / numRunsTotal for x in scoreSouth], 'g-o', label='south')
	plt.legend(loc='lower right')
	plt.ylabel('Average Score')
	plt.xlabel('Round')
	plt.figure()
	# average change in score per round
	plt.title('Average Change in Score per Round')
	plt.plot(range(1, 11), [scoreNorth[i] / numRunsTotal - scoreNorth[i - 1] / numRunsTotal for i in range(1, 11)], 'r-o', label='north')
	plt.plot(range(1, 11), [scoreSouth[i] / numRunsTotal - scoreSouth[i - 1] / numRunsTotal for i in range(1, 11)], 'g-o', label='south')
	plt.legend(loc='upper left')
	plt.ylabel('Average Change in Score')
	plt.xlabel('Round')
	plt.figure()
	# num of times each card played per round
	plt.title('Number of Times Each Card Played per Round (North)')
	for key, val in cardsPlayedNorth.items():
		plt.plot(val, '-o', label=str(key))
	plt.legend(loc='upper right')
	plt.ylabel('Average Number of Times Played')
	plt.xlabel('Round')
	plt.figure()
	plt.title('Number of Times Each Card Played per Round (South)')
	for key, val in cardsPlayedSouth.items():
		plt.plot(val, '-o', label=str(key))
	plt.legend(loc='upper right')
	plt.ylabel('Average Number of Times Played')
	plt.xlabel('Round')
	plt.show()

# runs numRuns games, puts output in q after each run
# outputs: final board state, time taken this round, elapsedTime north, elapsedTime south
def multiProcessingHelper(numRuns, q, northBot, southBot):
	util.setLogging(False)
	for i in range(numRuns):
		#start = timer()
		players, finalBoards = playGame(10, 10, northBot, southBot)
		#winner = players[0].pos
		# update number of wins
		#northWon = 0
		northPlayer = players[1]
		southPlayer = players[0]
		if players[0].pos.value == 0:
		#	northWon = 1
			northPlayer = players[0]
			southPlayer = players[1]
		# update time
		timeNorth = northPlayer.elapsedTime
		timeSouth = southPlayer.elapsedTime
		# score per round
		#scoreNorth = []
		#scoreSouth = []
		#for i in range(11):
	#		b = finalBoards[i]
#			scoreNorth.append(util.getScore(b, Position.NORTH))
#			scoreSouth.append(util.getScore(b, Position.SOUTH))
#		end = timer()
		q.put([finalBoards, timeNorth, timeSouth])

def runSim():
	# parameters
	util.setLogging(False)
	numRuns = 100
	northBot = MaxBot(Position.SOUTH)
	southBot = BacktrackingBot(Position.NORTH)
	
	# track winner
	numNorth = 0
	numSouth = 0
	
	# track avg time
	lastTimePrint = 0
	totalTime = 0
	totalTimeNorth = 0
	totalTimeSouth = 0
	
	# extra stats
	scoreNorth = [0 for _ in range(11)]
	scoreSouth = [0 for _ in range(11)]
	cardsPlayed = {}
	cardsPlayedCounting = Position.SOUTH
	
	print("Number of Runs:", numRuns)
	for i in range(numRuns):
		# play game
		start = timer()
		players, finalBoards = playGame(10, 10, northBot, southBot)
		end = timer()
		winner = players[0].pos
		finalBoard = finalBoards[len(finalBoards) - 1]
		
		# update number of wins
		if winner.value == 0:
			numNorth += 1
		elif winner.value == 1:
			numSouth += 1
		
		# time printout
		if players[0].pos.value == 0:
			totalTimeNorth += players[0].elapsedTime
		else:
			totalTimeSouth += players[0].elapsedTime
		if players[1].pos.value == 0:
			totalTimeNorth += players[1].elapsedTime
		else:
			totalTimeSouth += players[1].elapsedTime
		totalTime += end - start
		if totalTime - lastTimePrint > 10:
			lastTimePrint = totalTime
			avgTimePerRound = totalTime / i
			print(str(i * 100 / numRuns) + "%", end=" ")
			print("Elapsed time:", "{:.2f}".format(totalTime), "sec", end=" ")
			print("Expected time left :", "{:.2f}".format(avgTimePerRound * (numRuns - i)), "sec")
		
		# update avg scores
		for i in range(11):
			b = finalBoards[i]
			scoreNorth[i] += util.getScore(b, Position.NORTH)
			scoreSouth[i] += util.getScore(b, Position.SOUTH)
		
		# update cards
		for i in range(20):
			if finalBoard.history[i].pos == cardsPlayedCounting:
				if finalBoard.history[i].card in cardsPlayed:
					cardsPlayed[finalBoard.history[i].card][i // 2] += 1
				else:
					cardsPlayed[finalBoard.history[i].card] = [0 for _ in range(10)]
					cardsPlayed[finalBoard.history[i].card][i // 2] += 1
	
	# display winner
	print("Percent of times won:")
	print("north:", str(numNorth * 100 / numRuns) + "%")
	print("south:", str(numSouth * 100 / numRuns) + "%")
	
	# display avg time
	print("Avg time per game:")
	print("north:", "{:.2f}".format(totalTimeNorth / numRuns), "sec")
	print("south:", "{:.2f}".format(totalTimeSouth / numRuns), "sec")
	
	# graphs
	# average score per round
	plt.title('Average Score per Round')
	plt.plot([x / numRuns for x in scoreNorth], 'r-o', label='north')
	plt.plot([x / numRuns for x in scoreSouth], 'g-o', label='south')
	plt.legend(loc='lower right')
	plt.ylabel('Average Score')
	plt.xlabel('Round')
	plt.figure()
	# average change in score per round
	plt.title('Average Change in Score per Round')
	plt.plot(range(1, 11), [scoreNorth[i] / numRuns - scoreNorth[i - 1] / numRuns for i in range(1, 11)], 'r-o', label='north')
	plt.plot(range(1, 11), [scoreSouth[i] / numRuns - scoreSouth[i - 1] / numRuns for i in range(1, 11)], 'g-o', label='south')
	plt.legend(loc='upper left')
	plt.ylabel('Average Change in Score')
	plt.xlabel('Round')
	plt.figure()
	# num of times each card played per round
	plt.title('Number of Times Each Card Played per Round')
	for key, val in cardsPlayed.items():
		plt.plot(val, '-o', label=str(key))
	plt.legend(loc='upper right')
	plt.ylabel('Average Number of Times Played')
	plt.xlabel('Round')
	plt.show()
	

def playGame(numRounds, handSize, northBot, southBot):
	# init board
	b = board.Board()
	
	# init players
	cardDeck = getFullDeck()
	players = []
	players.append(createPlayer(cardDeck, handSize, Position.NORTH, northBot))
	players.append(createPlayer(cardDeck, handSize, Position.SOUTH, southBot))
	
	# board stats
	boardList = [b.boardState]
	
	# play game
	for i in range(numRounds):
		sortPlayers(b.boardState, players)
		
		# round info
		util.log("")
		util.log("------------------------- Round " + str(i + 1) + " -------------------------")
		b.boardState.printBoard()
		util.log("")
		util.log("Scores:")
		for player in players:
			util.log(str(player.pos) + ": " + str(util.getScore(b.boardState, player.pos)))
		util.log("")
		
		# players move
		order = 0
		for player in players:
			b.playCard(player.takeTurn(order, b.boardState))
			order = order + 1
		
		# update stats
		boardList.append(b.boardState)
	
	# final scores/stats
	util.log("")
	util.log("Final Scores:")
	sortPlayers(b.boardState, players)
	for player in players:
		util.log(str(player.pos) + ": " + str(util.getScore(b.boardState, player.pos)))
	
	return [players, boardList]

if __name__ == "__main__":
	multSim()