# Tests initially created by Ben Lafferty, with modifications to fit my program

import os
from virus import Virus
from person import Person
from logger import Logger
import pytest
pytest


def test_logger_metadata():
    logger = Logger('logs/test_log.txt')
    logger.write_metadata(100, 0.9, 'Ebola', 0.7, 0.25)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert val == ('Pop_size: 100    Vacc_percentage: 0.9'
                       '    Virus_name: Ebola    Mortality_rate: 0.7    '
                       'Repro_num: 0.25\n')

    os.remove('logs/test_log.txt')


def test_log_interaction_first_case():
    logger = Logger('logs/test_log.txt')

    virus = Virus("Ebola", 0.25, 0.70)

    person1 = Person(1, False, virus)
    person2 = Person(2, True, None)

    logger.log_interaction(person1, person2, True, False, False)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        print(val)
        assert "Person 1 does not infect person 2 because already infected"\
               in val

    os.remove('logs/test_log.txt')


def test_log_interaction_second_case():
    logger = Logger('logs/test_log.txt')

    virus = Virus("Ebola", 0.25, 0.70)

    person1 = Person(1, False, virus)
    person2 = Person(2, True, None)

    logger.log_interaction(person1, person2, False, True, False)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert "Person 1 does not infect person 2 because vaccinated"\
               in val

    os.remove('logs/test_log.txt')


def test_log_interaction_third_case():
    logger = Logger('logs/test_log.txt')

    virus = Virus("Ebola", 0.25, 0.70)

    person1 = Person(1, False, virus)
    person2 = Person(2, True, None)

    logger.log_interaction(person1, person2, False, False, True)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert "Person 1 infects person 2" in val

    os.remove('logs/test_log.txt')


def test_log_infection_survival_survied():
    logger = Logger('logs/test_log.txt')

    person1 = Person(1, False, None)

    logger.log_infection_survival(person1, False)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert 'Person 1 survived infection' in val

    os.remove('logs/test_log.txt')


def test_log_infection_survival_died():
    logger = Logger('logs/test_log.txt')

    person1 = Person(1, False, None)

    logger.log_infection_survival(person1, True)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert 'Person 1 died from infection' in val

    os.remove('logs/test_log.txt')


def test_log_timestep():
    logger = Logger('logs/test_log.txt')

    logger.log_time_step(1)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert 'Time step 1 ended, beginning 2' in val

    logger.log_time_step(2)

    with open('logs/test_log.txt', 'r') as f:
        val = f.read()
        assert 'Time step 2 ended, beginning 3' in val

    os.remove('logs/test_log.txt')
