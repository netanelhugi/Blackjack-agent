import BJ

# init game:
game = BJ.BlackJack()

# Manual game:
# print("# User play #")
# game.userPlay(10)

# Random agent game:
print("# Random play #")
summeryRand,avgRand = game.randomPlay(10001)
print("Average loss for 1000 rounds: ", avgRand)

# Auto agent game:
print("# Auto play #")
summeryAuto,avgAuto =game.autoPlay(10001)
print("Average loss for 1000 rounds: ", avgAuto)

# Learning process:
print("# Training #")
alpha = 0.001
gamma = 0.95
printAvg = False
game.training(5000,alpha,gamma,printAvg)

print("# Testing #")
summeryTest,avgTest = game.testing(1001)
print("Average loss for 1000 rounds: ", avgTest)
print(summeryTest)

# game.userPlayAfterTraining(10)

# For the strategy table (in the final report):
# m1,m2 = game.dictToTable();
# print(m1)
# print(m2)

