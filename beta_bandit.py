
from numpy import *
from scipy.stats import beta


class BetaBandit(object):
    def __init__(self, num_options=2,prior=1):
        self.trials = zeros(shape=(num_options,), dtype=int)
        self.successes = zeros(shape=(num_options,), dtype=int)
        self.num_options = num_options
        self.prior = [1]*self.num_options

    def add_result(self, trial_id, success,reward=1):
        self.trials[trial_id] = self.trials[trial_id] + reward
        if success==1:
            self.successes[trial_id] = self.successes[trial_id] + reward

    def get_recommendation(self):
        sampled_theta = []
        for i in range(self.num_options):
            #Construct beta distribution for posterior
            print(self.prior[i]+self.successes[i],self.prior[i]+2+self.trials[i]-self.successes[i])
            dist = beta(self.prior[i]+self.successes[i],
                        self.prior[i]+2+self.trials[i]-self.successes[i])
            #Draw sample from beta distribution
            sampled_theta += [ dist.rvs() ]
        # Return the index of the sample with the largest value
        return sampled_theta.index( max(sampled_theta) )