# Tests written by Ben Lafferty, modified by me with his permission

# This code tests the actual simulation
from virus import Virus
from person import Person
from simulation import Simulation
import random
random.seed(42)


def test_create_simulation():
    """Test to make sure the simulation is being initated correctly."""
    virus = Virus("Ebola", 0.25, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    assert len(sim.population) == 100
    assert sim.pop_size == 100
    assert sim.virus.name == "Ebola"
    assert sim.initial_infected == 1
    assert sim.total_infected == 1
    assert sim.current_infected == 1
    assert sim.vacc_percentage == 0.90
    assert sim.total_dead == 0
    assert sim.file_name == 'logs/\
Ebola_simulation_pop_100_vp_0.9_infected_1.txt'
    assert sim.logger is not None
    assert len(sim.newly_infected) == 0


def test_create_population():
    virus = Virus("Ebola", 0.25, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    normal_count = 0
    vacc_count = 0
    infec_count = 0
    for person in sim.population:
        if person.is_vaccinated:
            vacc_count += 1
        elif person.infection:
            infec_count += 1
        else:
            normal_count += 1

    assert normal_count == 9
    assert vacc_count == 90
    assert infec_count == 1


def test_simulation_should_continue_true():
    virus = Virus("Ebola", 0.25, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    assert sim._simulation_should_continue() is True


def test_simulation_should_continue_false():
    virus = Virus("Ebola", 0.25, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    for x in sim.population:
        x.is_alive = False
    sim.get_infected()

    assert sim._simulation_should_continue() is False


def test_simulation_should_continue_vaccinated():
    virus = Virus("Ebola", 0.25, 0.70)

    # Tests to see if ends with 0 infected people
    sim = Simulation(100, 0.90, virus, 0)

    assert sim._simulation_should_continue() is False


def test_interaction():
    # Test simulation interaction
    virus = Virus("Ebola", 0.25, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    person1 = Person(1, False, virus)
    person2 = Person(2, False, None)

    rand_val = sim.interaction(person1, person2)

    if rand_val < virus.repro_rate:
        assert sim.newly_infected[0] == 2
    else:
        assert len(sim.newly_infected) == 0


# Can't really test this because of the implementation
# def test_time_step():
#     virus = Virus("Ebola", 0.25, 0.70)

#     sim = Simulation(100, 0.90, virus, 1)

#     interaction = sim.time_step()
#     assert interaction == 100


def test_infect_newly_infected():
    # 100% repro rate
    virus = Virus("Ebola", 1.00, 0.70)

    sim = Simulation(100, 0.90, virus, 1)

    person1 = Person(1, False, virus)
    person2 = Person(2, False, None)

    sim.population.append(person1)
    sim.population.append(person2)

    sim.interaction(person1, person2)

    assert sim.population[2].infection is None

    sim._infect_newly_infected()

    assert sim.population[2].infection.name is not None


def test_run_func():
    virus = Virus("Ebola", 0.25, 0.70)
    sim = Simulation(100, 0.90, virus, 1)
    # Have to set seed because pytest is broken
    random.seed(42)

    output = sim.run()

    assert output == 'The simulation has ended after 5 turns.'
