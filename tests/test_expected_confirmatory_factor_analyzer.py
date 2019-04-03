"""
Tests for ConfirmatoryFactorAnalyzer class

:author: Jeremy Biggs (jbiggs@ets.org)
:date: 02/12/2019
:organization: ETS
"""
import numpy as np
import pandas as pd
from factor_analyzer.test_utils import check_cfa
from factor_analyzer.confirmatory_factor_analyzer import (ModelSpecification,
                                                          ModelSpecificationParser,
                                                          ConfirmatoryFactorAnalyzer)
from nose.tools import eq_, raises
from numpy.testing import assert_array_equal


THRESHOLD = 1.0


def test_11_cfa():

    json_name_input = 'test11'
    data_name_input = 'test11'

    for check in check_cfa(json_name_input,
                           data_name_input,
                           rel_tol=0.1):
        assert check >= THRESHOLD


def test_12_cfa():

    json_name_input = 'test12'
    data_name_input = 'test12'

    for check in check_cfa(json_name_input,
                           data_name_input,
                           abs_tol=0.05):
        assert check >= THRESHOLD


def test_13_cfa():

    json_name_input = 'test13'
    data_name_input = 'test13'

    for check in check_cfa(json_name_input,
                           data_name_input,
                           index_col=0,
                           is_cov=True,
                           n_obs=64,
                           rel_tol=0.1):
        assert check >= THRESHOLD


def test_14_cfa():

    json_name_input = 'test14'
    data_name_input = 'test14'

    for check in check_cfa(json_name_input,
                           data_name_input,
                           index_col=0,
                           rel_tol=0.1):
        assert check >= THRESHOLD


@raises(ValueError)
def test_14_cfa_no_model():

    X = np.array([[0, 0, 0, 0], [0, 0, 0, 0]])

    cfa = ConfirmatoryFactorAnalyzer('string_not_model')
    cfa.fit(X)


@raises(AssertionError)
def test_14_cfa_bad_bounds():

    X = np.array([[0, 0, 0, 0], [0, 0, 0, 0]])

    cfa = ConfirmatoryFactorAnalyzer(bounds=[(0, 1)])
    cfa.fit(X)


@raises(ValueError)
def test_14_cfa_cov_with_no_obs():

    ConfirmatoryFactorAnalyzer(is_cov_matrix=True)


class TestModelSpecificationParser:

    def test_model_spec_str(self):

        ms = ModelSpecification(np.array([[0, 0, 0]]), 3, 1)
        assert str(ms).startswith('<ModelSpecification object at ')

    def test_model_spec_as_dict(self):

        loadings = np.array([[0, 0, 0]])
        n_factors = 3
        n_variables = 1
        ms = ModelSpecification(loadings, n_factors, n_variables)

        expected = {'loadings': loadings,
                    'n_variables': n_variables,
                    'n_factors': n_factors}
        new_dict = ms.get_model_specification_as_dict()
        for key, value in expected.items():
            assert key in new_dict
            if isinstance(value, np.ndarray):
                assert_array_equal(new_dict[key], value)
            else:
                eq_(new_dict[key], value)

    def test_model_spec_parser_from_dict_none(self):
        X = np.array([[0, 0, 0]])
        ms = ModelSpecificationParser.parse_model_specification_from_dict(X, None)
        assert isinstance(ms, ModelSpecification)
        eq_(ms.n_factors, 3)
        eq_(ms.n_variables, 3)
        assert_array_equal(ms.loadings, np.ones((3, 3), dtype=int))

    @raises(ValueError)
    def test_model_spec_parser_from_dict_error(self):
        X = np.array([[0, 0, 0]])
        ModelSpecificationParser.parse_model_specification_from_dict(X, 'not_a_model')

    def test_model_spec_parser_from_array_none(self):
        X = np.array([[0, 0, 0]])
        ms = ModelSpecificationParser.parse_model_specification_from_array(X, None)
        assert isinstance(ms, ModelSpecification)
        eq_(ms.n_factors, 3)
        eq_(ms.n_variables, 3)
        assert_array_equal(ms.loadings, np.ones((3, 3), dtype=int))

    def test_model_spec_parser_from_array(self):
        X = np.array([[0, 0, 0]])
        spec = np.ones((3, 3), dtype=int)
        ms = ModelSpecificationParser.parse_model_specification_from_array(X, spec)
        assert isinstance(ms, ModelSpecification)
        eq_(ms.n_factors, 3)
        eq_(ms.n_variables, 3)
        assert_array_equal(ms.loadings, np.ones((3, 3), dtype=int))

    def test_model_spec_parser_from_frame(self):
        X = np.array([[0, 0, 0]])
        spec = pd.DataFrame(np.ones((3, 3), dtype=int))
        ms = ModelSpecificationParser.parse_model_specification_from_array(X, spec)
        assert isinstance(ms, ModelSpecification)
        eq_(ms.n_factors, 3)
        eq_(ms.n_variables, 3)
        assert_array_equal(ms.loadings, np.ones((3, 3), dtype=int))

    @raises(ValueError)
    def test_model_spec_parser_from_array_error(self):
        X = np.array([[0, 0, 0]])
        ModelSpecificationParser.parse_model_specification_from_array(X, 'not_a_model')
