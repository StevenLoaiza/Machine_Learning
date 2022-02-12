import logging

# logger
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def pvalue_sim(observed_mean, feature, sample_size, sim_number):
    """ Adapted from Khan Academy Video: Estimating P Value from Simulation

    Source: https://www.khanacademy.org/math/ap-statistics/xfb5d8e68:inference-categorical-proportions/idea-significance-tests/e/estimating-p-values-and-making-conclusions

    Args:
        observed_mean: self
        feature: Large population of the feature value
        sample_size: Number of samples to take from large population
        sim_number: Number of simulations
    """
    logger.info('Simulating P value')
    sim_value = []

    for i in range(sim_number):
        temp = feature.sample(sample_size).copy()
        sim_value.append(temp.mean())

    return len([1 for i in sim_value if i >= observed_mean])/len(sim_value)


if __name__ == '__main__':
    from sklearn import datasets
    import pandas as pd
    import numpy as np

    iris = datasets.load_iris()
    df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                      columns=iris['feature_names'] + ['target'])

    feature = df.loc[:, 'sepal length (cm)']
    spl_size = 15
    assumption = 6.1
    logger.info(
        'Lets test out our hypothesis that the %s is on average %s cm' %
        ('sepal length (cm)', assumption)
    )

    logger.info('The true average is %s' % feature.mean())

    p_val = pvalue_sim(
        observed_mean=assumption,
        feature=feature,
        sample_size=spl_size,
        sim_number=40
    )
    logger.info('P Value: %s' % p_val)
