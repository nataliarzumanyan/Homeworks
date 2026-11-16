# 1. Importing the necessary libraries
from abc import ABC, abstractmethod
from loguru import logger
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BANDIT_REWARDS = [1, 2, 3, 4]  
NUM_TRIALS = 20000              
TAU = 1 
# So that there are no problems with saving the CSV files
output_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Bandit class from our homework file
class Bandit(ABC):
    ##==== DO NOT REMOVE ANYTHING FROM THIS CLASS ====##

    @abstractmethod
    def __init__(self, p):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def pull(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def experiment(self):
        pass

    @abstractmethod
    def report(self):
        # store data in csv
        # print average reward (use f strings to make it informative)
        # print average regret (use f strings to make it informative)
        pass
    
# 3. Visualization class
class Visualization():
    """Class that draws all the plots of the experiment."""

    def plot1(self, name, algo):
        """Visualize the learning process of one algorithm (linear and log scale).

        Parameters
        ----------
        name : str
            Name of the algorithm (used in titles).
        algo : Bandit
            Algorithm object after experiment() was run.
        """
        # Average reward after each trial (same idea as in the slides)
        cum_avg = np.cumsum(algo.rewards) / (np.arange(NUM_TRIALS) + 1)
        best = max(BANDIT_REWARDS)

        fig, axes = plt.subplots(1, 3, figsize=(18, 4))

        # Linear scale
        axes[0].plot(cum_avg, label=f"{name} average reward")
        axes[0].plot(np.ones(NUM_TRIALS) * best, label="Optimal reward")
        axes[0].set_title(f"{name}: Learning (linear)")
        axes[0].set_xlabel("Number of Trials")
        axes[0].set_ylabel("Average Reward")
        axes[0].legend()

        # Log scale
        axes[1].plot(cum_avg, label=f"{name} average reward")
        axes[1].plot(np.ones(NUM_TRIALS) * best, label="Optimal reward")
        axes[1].set_xscale("log")
        axes[1].set_title(f"{name}: Learning (log)")
        axes[1].set_xlabel("Number of Trials (log)")
        axes[1].set_ylabel("Average Reward")
        axes[1].legend()

        # How many times each bandit was chosen
        axes[2].bar([f"Bandit {k+1}" for k in range(len(BANDIT_REWARDS))], algo.N)
        axes[2].set_title(f"{name}: Times each bandit was chosen")
        axes[2].set_ylabel("Number of pulls")

        plt.tight_layout()
        fig.savefig(
            os.path.join(output_dir, f"{name}_learning.png"),
            dpi=300,
            bbox_inches="tight"
        )
        
        plt.show()
        plt.close(fig)

    def plot2(self, algos):
        """Compare cumulative rewards and cumulative regrets of the algorithms.

        Parameters
        ----------
        algos : dict
            {name: algorithm object}, e.g. {"EpsilonGreedy": eg, "ThompsonSampling": ts}.
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        for name, a in algos.items():
            axes[0].plot(np.cumsum(a.rewards), label=name)
            axes[1].plot(np.cumsum(a.regrets), label=name)

        axes[0].set_title("Cumulative Reward")
        axes[0].set_xlabel("Number of Trials")
        axes[0].set_ylabel("Cumulative Reward")
        axes[0].legend()

        axes[1].set_title("Cumulative Regret")
        axes[1].set_xlabel("Number of Trials")
        axes[1].set_ylabel("Cumulative Regret")
        axes[1].legend()

        plt.tight_layout()
        fig.savefig(
            os.path.join(output_dir, "Algorithms_comparison.png"),
            dpi=300,
            bbox_inches="tight"
        )
        
        plt.show()
        plt.close(fig)
        
# 4. Epsilon Greedy
class EpsilonGreedy(Bandit):
    """Epsilon-Greedy algorithm with decaying epsilon = 1/t."""

    def __init__(self, p):
        """Create the algorithm.

        Parameters
        ----------
        p : list
            True mean rewards of the bandits.
        """
        self.p = p
        self.p_estimate = [0.] * len(p)      
        self.N = [0] * len(p)                    
        self.rewards = np.zeros(NUM_TRIALS)     
        self.regrets = np.zeros(NUM_TRIALS)     
        self.chosen = np.zeros(NUM_TRIALS, dtype=int)  

    def __repr__(self):
        return f"EpsilonGreedy with bandit rewards {self.p}"

    def pull(self, j):
        """Pull bandit j and get a Gaussian reward (known precision TAU).

        Parameters
        ----------
        j : int
            Index of the bandit.

        Returns
        -------
        float
            The reward.
        """
        return np.random.randn() / np.sqrt(TAU) + self.p[j]

    def update(self, j, x):
        """Update the mean estimate of bandit j with new reward x.

        Parameters
        ----------
        j : int
            Index of the bandit.
        x : float
            Reward we just got.
        """
        self.N[j] += 1
        self.p_estimate[j] = ((self.N[j] - 1) * self.p_estimate[j] + x) / self.N[j]

    def experiment(self):
        """Run the experiment for NUM_TRIALS trials."""
        best = max(self.p)
        for i in range(NUM_TRIALS):
            eps = 1 / (i + 1)                  
            if np.random.random() < eps:
                j = np.random.randint(len(self.p))        
            else:
                j = int(np.argmax(self.p_estimate))       

            x = self.pull(j)
            self.update(j, x)

            self.rewards[i] = x
            self.regrets[i] = best - self.p[j]
            self.chosen[i] = j

    def report(self):
        """Save rewards to CSV and log average/cumulative reward and regret."""
        df = pd.DataFrame({"Bandit": self.chosen + 1,
                           "Reward": self.rewards,
                           "Algorithm": "EpsilonGreedy"})
        df.to_csv(os.path.join(output_dir, "EpsilonGreedy_rewards.csv"), index=False)

        logger.info(f"[EpsilonGreedy] Estimated means: {[round(e, 3) for e in self.p_estimate]}")
        logger.info(f"[EpsilonGreedy] Average reward: {self.rewards.mean():.4f}")
        logger.info(f"[EpsilonGreedy] Average regret: {self.regrets.mean():.4f}")
        logger.info(f"[EpsilonGreedy] Cumulative reward: {self.rewards.sum():.2f}")
        logger.info(f"[EpsilonGreedy] Cumulative regret: {self.regrets.sum():.2f}")
        
# 5. Thompson Sampling
class ThompsonSampling(Bandit):
    """Thompson Sampling with Gaussian rewards and KNOWN precision."""

    def __init__(self, p):
        """Create the algorithm.

        Parameters
        ----------
        p : list
            True mean rewards of the bandits.
        """
        k = len(p)
        self.p = p
        # Posterior of each bandit's mean mu: Normal(m, 1/lambda_). Prior is N(0,1)
        self.m = np.zeros(k)
        self.lambda_ = np.ones(k)
        self.tau = TAU                          
        self.N = np.zeros(k, dtype=int)
        self.sum_x = np.zeros(k)
        self.rewards = np.zeros(NUM_TRIALS)
        self.regrets = np.zeros(NUM_TRIALS)
        self.chosen = np.zeros(NUM_TRIALS, dtype=int)

    def __repr__(self):
        return f"ThompsonSampling with bandit rewards {self.p}"

    def pull(self, j):
        """Pull bandit j and get a Gaussian reward.

        Parameters
        ----------
        j : int
            Index of the bandit.

        Returns
        -------
        float
            The reward.
        """
        return np.random.randn() / np.sqrt(self.tau) + self.p[j]

    def sample(self):
        """Draw one sample from the posterior of every bandit.

        Returns
        -------
        numpy.ndarray
            One sampled mean for each bandit.
        """
        return np.random.randn(len(self.p)) / np.sqrt(self.lambda_) + self.m

    def update(self, j, x):
        """Update the posterior of bandit j with new reward x.

        Parameters
        ----------
        j : int
            Index of the bandit.
        x : float
            Reward we just got.
        """
        self.lambda_[j] += self.tau
        self.sum_x[j] += x
        self.m[j] = (self.tau * self.sum_x[j]) / self.lambda_[j]
        self.N[j] += 1

    def experiment(self):
        """Run the experiment for NUM_TRIALS trials."""
        best = max(self.p)
        for i in range(NUM_TRIALS):
            j = int(np.argmax(self.sample()))     

            x = self.pull(j)
            self.update(j, x)

            self.rewards[i] = x
            self.regrets[i] = best - self.p[j]
            self.chosen[i] = j

    def report(self):
        """Save rewards to CSV and log average/cumulative reward and regret."""
        df = pd.DataFrame({"Bandit": self.chosen + 1,
                           "Reward": self.rewards,
                           "Algorithm": "ThompsonSampling"})
        df.to_csv(os.path.join(output_dir, "ThompsonSampling_rewards.csv"), index=False)

        logger.info(f"[ThompsonSampling] Estimated means: {[round(e, 3) for e in self.m]}")
        logger.info(f"[ThompsonSampling] Average reward: {self.rewards.mean():.4f}")
        logger.info(f"[ThompsonSampling] Average regret: {self.regrets.mean():.4f}")
        logger.info(f"[ThompsonSampling] Cumulative reward: {self.rewards.sum():.2f}")
        logger.info(f"[ThompsonSampling] Cumulative regret: {self.regrets.sum():.2f}")
        
# 6. Comparison
def comparison():
    """Run both algorithms, report them and compare them visually."""
    viz = Visualization()

    eg = EpsilonGreedy(BANDIT_REWARDS)
    ts = ThompsonSampling(BANDIT_REWARDS)

    eg.experiment()
    ts.experiment()

    eg.report()
    ts.report()

    # One CSV with {Bandit, Reward, Algorithm}
    all_data = pd.concat([
        pd.DataFrame({"Bandit": eg.chosen + 1, "Reward": eg.rewards, "Algorithm": "EpsilonGreedy"}),
        pd.DataFrame({"Bandit": ts.chosen + 1, "Reward": ts.rewards, "Algorithm": "ThompsonSampling"}),
    ])
    all_data.to_csv(os.path.join(output_dir, "rewards.csv"), index=False)
    logger.info("All rewards saved to rewards.csv")

    # Plots
    viz.plot1("EpsilonGreedy", eg)
    viz.plot1("ThompsonSampling", ts)
    viz.plot2({"EpsilonGreedy": eg, "ThompsonSampling": ts})

    # Conclusion
    winner = "EpsilonGreedy" if eg.regrets.sum() < ts.regrets.sum() else "ThompsonSampling"
    logger.info(f"Lower cumulative regret in this run: {winner}")


if __name__=='__main__':
# Random seed is 1, so that we get the same result every time we run it
    np.random.seed(1)   
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    comparison()
    
# For result interpretations and bonus question, please look at the README.md file.