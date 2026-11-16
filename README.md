Below you can find the interpretations of the results, as well as the answer to the bonus question.

1. The Epsilon-Greedy algorithm gradually learned to identify Bandit 4 as the best option. As the exploration probability decreased over time according to the (1/t) schedule, the algorithm increasingly selected the bandit with the highest estimated reward. Out of 20,000 trials, Bandit 4 was selected 19,879 times, and the final average reward reached approximately 3.987. The cumulative regret was 142, showing that the algorithm made relatively few suboptimal selections.

2. Thompson Sampling also successfully identified Bandit 4 as the optimal option. It selected Bandit 4 19,154 times out of 20,000 trials and achieved a final average reward of approximately 3.952. However, it selected Bandit 3 more frequently than Epsilon-Greedy, which contributed to its higher cumulative regret of 863. The learning curve shows that the algorithm gradually improved its performance, as it collected more information about the available bandits.

3. Both algorithms achieved average rewards close to the optimal expected reward of 4, meaning that they successfully learned to select the best advertisement option. However, Epsilon-Greedy achieved a higher cumulative reward of approximately 79,736, compared with 79,029 for Thompson Sampling. It also had considerably lower cumulative regret, with 142 compared to 863. Therefore, Epsilon-Greedy performed better in this particular experiment, although the results may differ with other random seeds and experimental runs.

*BONUS - Suggest better implementation plan.*
In the current implementation, each algorithm is tested once with 20,000 trials. However, the results can change depending on the random seed and the rewards received during the experiment.

To improve the implementation, we may do the following:
1. Run each algorithm several times with different random seeds instead of testing it only once.
2. Calculate the average cumulative reward and regret from all runs to get a fairer comparison.
3. Try different values of epsilon and prior precision to see how they affect the algorithms.
4. Show the average reward and regret across all runs to make the results easier to compare.
5. Calculate the standard deviation to understand how much the results change between experiments.