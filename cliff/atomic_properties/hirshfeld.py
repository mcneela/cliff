#!/usr/bin/env python
#
# Hirshfeld class. Predict Hirshfeld ratios.
#
# Tristan Bereau (2017)

from system import System
import scipy
from scipy import stats
from scipy.spatial.distance import pdist, cdist, squareform
import logging
import pickle
import numpy as np
import utils

# Set logger
logger = logging.getLogger(__name__)

class Hirshfeld:
    'Hirshfeld class. Predicts Hirshfeld ratios.'

    def __init__(self, _calculator):
        self.calculator = _calculator
        self.descr_train = []
        self.target_train = []
        # kernel ridge regression
        self.alpha_train = None
        # support vector regression
        self.clf = None
        logger.setLevel(self.calculator.get_logger_level())
        self.max_neighbors = self.calculator.get_hirshfeld_max_neighbors()
        self.krr_kernel = self.calculator.get_hirshfeld_krr_kernel()
        self.krr_sigma = self.calculator.get_hirshfeld_krr_sigma()
        self.krr_lambda = self.calculator.get_hirshfeld_krr_lambda()
        self.svr_kernel = self.calculator.get_hirshfeld_svr_kernel()
        self.svr_C = self.calculator.get_hirshfeld_svr_C()
        self.svr_epsilon = self.calculator.get_hirshfeld_svr_epsilon()

        self.from_file = _calculator.get_hirshfeld_file_read()
        self.filepath = _calculator.get_hirshfeld_filepath()


    def load_ml(self):

        if self.from_file == 'True':
            return

        training_file = self.calculator.get_hirshfeld_training()
        logger.info(
            "Reading Hirshfeld training from %s" % training_file)
        with open(training_file, 'rb') as f:
            self.descr_train, self.alpha_train = pickle.load(f, encoding='bytes')

    def train_ml(self, ml_method):
        '''Train machine learning model.'''
        size_training = len(self.target_train)
        if len(self.descr_train) == 0:
            logger.error("No molecule in the training set.")
            exit(1)
        if ml_method == "krr":
            logger.info("building kernel matrix of size (%d,%d); %7.4f Gbytes" \
                % (size_training, size_training, 8*size_training**2/1e9))
            print("building kernel matrix of size (%d,%d); %7.4f Gbytes" \
                % (size_training, size_training, 8*size_training**2/1e9))
            if self.krr_kernel == 'gaussian':
                pairwise_dists = squareform(pdist(self.descr_train, 'euclidean'))
                kmat = scipy.exp(- pairwise_dists**2 / (2.*self.krr_sigma**2) )
            elif self.krr_kernel == 'laplacian':
                pairwise_dists = squareform(pdist(self.descr_train, 'cityblock'))
                kmat = scipy.exp(- pairwise_dists / self.krr_sigma )
            else:
                print("Kernel",self.krr_kernel,"not implemented.")
            kmat += self.krr_lambda*np.identity(len(self.target_train))
            self.alpha_train = np.linalg.solve(kmat,self.target_train)
        else:
            logger.error("unknown ML method %s" % ml_method)
            exit(1)
        logger.info("training finished.")
        return None

    def predict_mol(self, _system, ml_method):
        '''Predict coefficients given  descriptors.'''

        _system.build_coulomb_matrices(self.max_neighbors)
        if self.from_file == "True" :
            h_ratios = []
            for hfile in _system.xyz:
                hfile = self.filepath + hfile.split('/')[-1]
                with open(hfile,'r') as infile:
                    for line in infile:
                        line = line.split()
                        if len(line) == 6:
                            h_ratios.append(float(line[4])) 

            _system.hirshfeld_ratios = h_ratios

        elif ml_method == "krr":
            if self.krr_kernel == 'gaussian':
                pairwise_dists = cdist(_system.coulomb_mat, self.descr_train,
                    'euclidean')
                kmat = scipy.exp(- pairwise_dists**2 / (2.*self.krr_sigma**2) )
            elif self.krr_kernel == 'laplacian':
                pairwise_dists = cdist(_system.coulomb_mat, self.descr_train,
                    'cityblock')
                kmat = scipy.exp(- pairwise_dists / self.krr_sigma )
            else:
                logger.error("Kernel %s not implemented" % self.krr_kernel)
                exit(1)
            _system.hirshfeld_ratios = np.dot(kmat,self.alpha_train)
        else:
            logger.error("unknown ML method %s" % ml_method)
            exit(1)
        logger.info("Prediction: %s" % _system.hirshfeld_ratios)
        return None

    def add_mol_to_training(self, new_system):
        'Add molecule to training set'
        new_system.build_coulomb_matrices(self.max_neighbors)
        if len(new_system.hirshfeld_ref) != len(new_system.coulomb_mat):
            logger.error("Inconcistency in training data for %s" % new_system)
            exit(1)
        self.descr_train += new_system.coulomb_mat
        self.target_train += [i for i in new_system.hirshfeld_ref]
        logger.info("Added file to training set: %s" % new_system)
        return None