import gym
import random
import numpy as np


class BlackJack(object):

    def __init__(self):
        # create enviroment
        self.env = gym.make('Blackjack-v0')

        # crate Q-table
        self.action_size = self.env.action_space.n  # 2
        self.state_size = self.env.observation_space.spaces  # [32,11,2]
        self.Q_learning_table = dict()
        self.init_Q_table()

    # Init the Q-table with tuples(the keys) of all states:
    def init_Q_table(self):

        for i in range(1, 33):
            for j in range(1, 12):
                for k in range(1, 3):
                    if (k == 1):
                        state = (i, j, False)
                    else:
                        state = (i, j, True)
                    self.Q_learning_table[state] = dict((action, 0.0) for action in range(self.action_size))

    # Function for manual game mode:
    # games = number of games to play.
    def userPlay(self, games):

        # random.seed(100)

        # Statistics counters:
        winsUser = 0
        drawsUser = 0
        lossesUser = 0
        bonusUser = 0
        rewardsUser = []

        for i in range(games):
            print("NEW GAME: ")
            state = self.env.reset()
            self.stateDesc(state, self.env, False)

            # Blackjack - ace and 10/jack/queen/king.
            if (state[0] == 21):
                reward = 1.5
                bonusUser += 1
                rewardsUser.append(reward)
                print("Player won!")
                print("Your reward: ", reward)

            else:
                action = int(input("1-hit or 0-stand:"))

                while (True):
                    if (action != 0 and action != 1):
                        action = int(input("Wrong Value! - 1-hit or 0-stand:"))

                    else:
                        state, reward, done, _ = self.env.step(action)

                        if (action == 0):
                            self.stateDesc(state, self.env, True)
                        else:
                            self.stateDesc(state, self.env, False)

                        if (done == False):
                            action = int(input("good Value! - 1-hit or 0-stand:"))
                        else:
                            if (reward == -1):
                                lossesUser += 1
                                print("Dealer won!")
                            elif (reward == 0):
                                drawsUser += 1
                                print("Draw!")
                            else:
                                winsUser += 1
                                print("Player won!")
                            print(reward)
                            rewardsUser.append(reward)
                            print()
                            break

        print("Total results: wind= %d, draws= %d, losses= %d, rewards= %.1f"%(winsUser,drawsUser,lossesUser,sum(rewardsUser)))


    # Function for random agent game mode:
    # games = number of games to play.
    def randomPlay(self, games):

        # Set collection of random numbers:
        # random.seed(1000)

        # Statistics counters:
        rewardsRand = []  # Rewards counter(change to 0 every 1000 games)
        avgRewardsRand = []  # Count the rewards of every 1000 games.
        bonusRand = 0  # Count the games that end in blackjack.
        lossesRand = 0
        drawsRand = 0
        winsRand = 0
        totalRewardsRand = []  # Rewards counter(of all the games).

        for i in range(games):
            state = self.env.reset()

            # Blackjack - ace and 10/jack/queen/king.
            if (state[0] == 21):
                reward = 1.5
                bonusRand += 1
                rewardsRand.append(reward)

            else:
                action = self.env.action_space.sample()

                while (True):
                    state, reward, done, _ = self.env.step(action)

                    if (done == False):
                        action = self.env.action_space.sample()

                    else:
                        if (reward == -1):
                            lossesRand += 1
                        elif (reward == 0):
                            drawsRand += 1
                        else:
                            winsRand += 1
                        rewardsRand.append(reward)
                        totalRewardsRand.append(reward)
                        break

            # Calculate average of every 1000 games.
            if (i % 1000 == 0 and i > 999):
                avgRewardsRand.append(sum(rewardsRand))
                rewardsRand = []

        summery = [winsRand, drawsRand, lossesRand, bonusRand, sum(totalRewardsRand)]
        avgLossRand = np.mean(avgRewardsRand)

        # Return - statistics, Average loss in every 1000 games:
        return summery, avgLossRand

    # Function for random agent game mode:
    # games = number of games to play.
    def autoPlay(self, games):

        # Set collection of random numbers:
        # random.seed(1000)

        # Statistics counters:
        winsAuto = 0
        drawsAuto = 0
        lossesAuto = 0
        bonusAuto = 0  # Count the games that end in blackjack.
        rewardsAuto = []  # Rewards counter(change to 0 every 1000 games)
        avgRewardsAuto = []  # Count the rewards of every 1000 games.
        totalRewardsAuto = []  # Rewards counter(of all the games).

        for i in range(games):
            state = self.env.reset()

            # Blackjack - ace and 10/jack/queen/king.
            if (state[0] == 21):
                reward = 1.5
                bonusAuto += 1
                rewardsAuto.append(reward)

            else:
                if (sum(self.env.player) >= 18):
                    action = 0
                else:
                    action = 1

                while (True):
                    state, reward, done, _ = self.env.step(action)

                    if (done == False):
                        action = self.env.action_space.sample()

                    else:
                        if (reward == -1):
                            lossesAuto += 1
                        elif (reward == 0):
                            drawsAuto += 1
                        else:
                            winsAuto += 1
                        rewardsAuto.append(reward)
                        totalRewardsAuto.append(reward)
                        break

            # Calculate average of every 1000 games.
            if (i % 1000 == 0 and i > 999):
                avgRewardsAuto.append(sum(rewardsAuto))
                rewardsAuto = []

        summery = [winsAuto, drawsAuto, lossesAuto, bonusAuto, sum(totalRewardsAuto)]
        avgLossAuto = np.mean(avgRewardsAuto)

        # Return - statistics, Average loss in every 1000 games:
        return summery, avgLossAuto

    # State description:
    #
    # print:
    # 1. The player hand.
    # 2. The dealer hand.
    def stateDesc(self, state, env, stay):
        print("Player:", env.player, "Sum: %d" % state[0])

        if (stay == True):
            if ((env.dealer[0] == 1 and env.dealer[1] == 10) or (env.dealer[1] == 1 and env.dealer[0] == 10)):
                print("Dealer:", env.dealer, " Sum: 21")
            else:
                print("Dealer:", env.dealer, " Sum: ", sum(env.dealer))
        else:
            print("Dealer: [%d]" % env.dealer[0], " Sum: ", env.dealer[0])

    # The learning process:
    # alpha = learning rate.
    # gamma = discount factor.
    # printAvg = boolean, print the average loss every 100 training episodes.
    def training(self, games, alpha, gamma, printAvg):

        # Exploration parameters
        epsilon = 1.0  # Exploration rate
        max_epsilon = 1.0  # Exploration probability at start
        min_epsilon = 0.01  # Minimum exploration probability
        decay_rate = 0.005  # Exponential decay rate for exploration prob

        # Statistics counters:
        winsTrain = 0
        drawsTrain = 0
        lossesTrain = 0
        rewardsTrain = []

        for i in range(games):
            state = self.env.reset()
            gameover = False

            while not gameover:  # until the game is over.
                rand = random.random()

                # choice --> exploration
                # at first we need more exploration
                if rand < epsilon:
                    action = self.env.action_space.sample()
                else:
                    # argMax
                    action = max(self.Q_learning_table[state], key=self.Q_learning_table[state].get)

                newState, reward, gameover, _ = self.env.step(action)

                self.Q_learning_table[state][action] = self.Q_learning_table[state][action] + alpha * (
                        reward + gamma * max(self.Q_learning_table[newState].values()) - self.Q_learning_table[state][
                    action])
                state = newState

            if (reward == -1):
                lossesTrain += 1
            elif (reward == 0):
                drawsTrain += 1
            else:
                winsTrain += 1

            # Reduce epsilon (because we need less and less exploration)
            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * i)
            rewardsTrain.append(reward)

            # Testing the model after every 100 rounds of training:
            if (i % 100 == 0 and i > 99):
                # random.seed(50)
                summeryTesting, avgTesting = self.testing(1001)
                if (printAvg):
                    print("Average loss for 1000 rounds and %d training episodes: %.2f" % (i, avgTesting))

    # Testing after learning:
    # gamesTest = number of games to play.
    def testing(self, gamesTest):

        # Set collection of random numbers:
        # random.seed(1000)

        # Statistics counters:
        winsTest = 0
        drawsTest = 0
        lossesTest = 0
        bonusTest = 0
        rewardsTest = []
        avgRewardsTest = []
        totalRewardTest = []

        for j in range(gamesTest):

            state = self.env.reset()
            gameover = False

            # Blackjack - ace and 10/jack/queen/king.
            if (state[0] == 21):
                reward = 1.5
                bonusTest += 1
                gameover = True

            while not gameover:  # until game over, or max number of steps
                # argMax
                action = max(self.Q_learning_table[state], key=self.Q_learning_table[state].get)

                newState, reward, gameover, _ = self.env.step(action)
                state = newState

            if (reward == -1):
                lossesTest += 1
            elif (reward == 0):
                drawsTest += 1
            elif (reward == 1):
                winsTest += 1

            rewardsTest.append(reward)
            totalRewardTest.append(reward)

            # Calculate average of every 1000 games.
            if (j % 1000 == 0 and j > 999):
                avgRewardsTest.append(sum(rewardsTest))
                rewardsTest = []

        summery = [winsTest, drawsTest, lossesTest, bonusTest, sum(totalRewardTest)]
        avgLossAuto = np.mean(avgRewardsTest)

        # Return - statistics, Average loss:
        return summery, avgLossAuto

    # For the strategy table (in the final report):
    # Convert the dictionary to 2 matrix:
    # Matrix1 = the states with ace(in the player hand)
    # Matrix2 = the states without ace.
    def dictToTable(self):

        w, h = 11, 32;
        Matrix1 = [[0 for x in range(w)] for y in range(h)]  # usable
        Matrix2 = [[0 for x in range(w)] for y in range(h)]  # no usable

        for i in range(2, 32):
            for j in range(1, 11):
                stateTrue = (i, j, True)
                stateFalse = (i, j, False)

                if (max(self.Q_learning_table[stateTrue], key=self.Q_learning_table[stateTrue].get) == 1):
                    Matrix1[i][j] = "H"
                elif (max(self.Q_learning_table[stateTrue], key=self.Q_learning_table[stateTrue].get) == 0):
                    Matrix1[i][j] = "S"

                if (max(self.Q_learning_table[stateFalse], key=self.Q_learning_table[stateFalse].get) == 1):
                    Matrix2[i][j] = "H"
                elif (max(self.Q_learning_table[stateFalse], key=self.Q_learning_table[stateFalse].get) == 0):
                    Matrix2[i][j] = "S"

        return Matrix1, Matrix2



    # Function for manual game mode(after learning):
    # games = number of games to play.
    #
    # In every step, the player get advice of what action to take(according to the Q-table)
    def userPlayAfterTraining(self, games):

        # random.seed(100)

        # Statistics counters:
        winsUser = 0
        drawsUser = 0
        lossesUser = 0
        bonusUser = 0
        rewardsUser = []

        for i in range(games):
            print("NEW GAME: ")
            state = self.env.reset()
            self.stateDesc(state, self.env, False)

            # Blackjack - ace and 10/jack/queen/king.
            if (state[0] == 21):
                reward = 1.5
                bonusUser += 1
                rewardsUser.append(reward)
                print("Player won!")
                print("Your reward: ", reward)

            else:
                advice = max(self.Q_learning_table[state], key=self.Q_learning_table[state].get)

                if(advice==1):
                    action = int(input("1-hit or 0-stay(Recommended action: Hit):"))
                elif(advice==0):
                    action = int(input("1-hit or 0-stay(Recommended action: Stand):"))

                while (True):
                    if (action != 0 and action != 1):
                        if (advice == 1):
                            action = int(input("Wrong Value! - 1-hit or 0-stay(Recommended action: Hit):"))
                        elif (advice == 0):
                            action = int(input("Wrong Value! - 1-hit or 0-stay(Recommended action: Stand):"))

                    else:
                        state, reward, done, _ = self.env.step(action)

                        if (action == 0):
                            self.stateDesc(state, self.env, True)
                        else:
                            self.stateDesc(state, self.env, False)

                        if (done == False):

                            advice = max(self.Q_learning_table[state], key=self.Q_learning_table[state].get)

                            if (advice == 1):
                                action = int(input("1-hit or 0-stay(Recommended action: Hit):"))
                            elif (advice == 0):
                                action = int(input("1-hit or 0-stay(Recommended action: Stand):"))

                        else:
                            if (reward == -1):
                                lossesUser += 1
                                print("Dealer won!")
                            elif (reward == 0):
                                drawsUser += 1
                                print("Draw!")
                            else:
                                winsUser += 1
                                print("Player won!")
                            print(reward)
                            rewardsUser.append(reward)
                            print()
                            break
        print("Total results: wind= %d, draws= %d, losses= %d, rewards= %.1f"%(winsUser,drawsUser,lossesUser,sum(rewardsUser)))
