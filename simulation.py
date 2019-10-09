import random
import sys
from person import Person
from logger import Logger
from virus import Virus
random.seed(42)


class Simulation(object):
    """Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when
    file is run.

    Simulates the spread of a virus through a given population.  The percentage
    of the
    population that are vaccinated, the size of the population, and the amount
    of initially
    infected people in a population are all variables that can be set when the
    program is run.
    """

    def __init__(self, pop_size, vacc_percentage, virus, initial_infected=1):
        """
        Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of
        population vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected
        with the disease.
        The total infected people is the running total that have been infected
        since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die
        as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is
        run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        """
        self.pop_size = pop_size  # Int
        self.next_person_id = 0  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_infected = 0  # Int
        self.current_infected = 0  # Int
        self.new_deaths = 0  # Int
        self.total_dead = 0  # Int
        self.new_vaccinations = 0  # Int
        self.total_vaccinated = 0  # Int
        self.population = self._create_population(self.initial_infected)
        # List of people objects
        self.file_name = "logs/{}_simulation_pop_{}_vp_{}_infected_{}\
.txt".format(virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []

        self.logger.write_metadata(self.pop_size, self.vacc_percentage,
                                   self.virus.name, self.virus.mortality_rate,
                                   self.virus.repro_rate)

    def _create_population(self, initial_infected):
        """
        This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the
                simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        """
        # Use the attributes created in the init method to create a population
        # that has the correct intial vaccination percentage and initial
        # infected.
        pop_list = []
        vacc_number = int(self.pop_size * self.vacc_percentage)
        for person_num in range(self.pop_size):
            if person_num < initial_infected:
                pop_list.append(Person(person_num, False, self.virus))
                self.total_infected += 1
            elif person_num < initial_infected + vacc_number:
                pop_list.append(Person(person_num, True))
                self.total_vaccinated += 1
            else:
                pop_list.append(Person(person_num, False))

        return pop_list

    def _simulation_should_continue(self):
        """
        The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should
                end.

        """
        if len(self.get_infected()) == 0:
            return False
        else:
            return True

    def get_infected(self):
        """Helper function to get and return the list of infected people"""
        inf_list = []
        self.current_infected = 0
        for person in self.population:
            if person.infection is not None and person.is_alive:
                inf_list.append(person)
                self.current_infected += 1

        return inf_list

    def run(self):
        """
        This method should run the simulation until all requirements for ending
        the simulation are met.
        """
        time_step_counter = 0
        should_continue = True

        while should_continue:
            # Complete another step of the simulation
            time_step_counter += 1
            self.time_step()
            self.logger.log_time_step(time_step_counter, self.current_infected,
                                      self.new_deaths, self.new_vaccinations,
                                      self.total_infected, self.total_dead,
                                      self.total_vaccinated)
            should_continue = self._simulation_should_continue()

        print('The simulation has ended after',
              f'{time_step_counter} turns.'.format(time_step_counter))

    def time_step(self):
        """
        This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected
            person in the population
            2. If the person is dead, grab another random person from the
            population.
                Since we don't interact with dead people, this does not count
                as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
        """
        # Create list of infected people
        self.new_deaths = 0
        self.new_vaccinations = 0
        inf_list = self.get_infected()

        # Iterate through infected population and interact with 100 people
        for person in inf_list:
            interaction_count = 0
            while interaction_count < 100:
                random_person = random.choice(self.population)
                while not random_person.is_alive:
                    random_person = random.choice(self.population)
                self.interaction(person, random_person)
                interaction_count += 1

        # Check if infected people survive the infection
        for person in inf_list:
            survived = person.did_survive_infection()
            if survived:
                self.total_vaccinated += 1
                self.new_vaccinations += 1
                self.logger.log_infection_survival(person, False)
            else:
                self.total_dead += 1
                self.new_deaths += 1
                self.logger.log_infection_survival(person, True)

        # Infect newly infected people
        self._infect_newly_infected()
        self.get_infected()

    def interaction(self, person, random_person):
        """
        This method should be called any time two living people are selected
        for an
        interaction. It assumes that only living people are passed in as
        parameters.

        Args:
            person (person): The initial infected person
            random_person (person): The person that person1 interacts with.

        """
        # Assert statements are included to make sure that only living people
        # are passed
        # in as params
        assert person.is_alive is True
        assert random_person.is_alive is True

        """
        Check Cases:
        If vaccinated or sick, do nothing
        Otherwise find random percentage and check against repro_rate
            If it's lower, add random_person to newly_infected list
            Otherwise, nothing happens
        """
        if random_person.is_vaccinated:
            self.logger.log_interaction(person, random_person,
                                        False, True, False)
        elif random_person.infection is not None:
            self.logger.log_interaction(person, random_person,
                                        True, False, False)
        else:
            inf_chance = random.random()
            if (inf_chance < person.infection.repro_rate
               and self.newly_infected.count(random_person._id) == 0):
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person,
                                            False, False, True)
            else:
                self.logger.log_interaction(person, random_person,
                                            False, False, False)

    def _infect_newly_infected(self):
        """
        This method should iterate through the list of ._id stored in
        self.newly_infected
        and update each Person object with the disease.
        """
        for person_id in self.newly_infected:
            self.population[person_id].infection = self.virus
            self.total_infected += 1

        self.newly_infected.clear()


def test_create_population():
    virus = Virus("Test", 0.8, 0.2)
    # 100 people, 80% vaccination, 10 initial infected
    sim = Simulation(100, 0.7, virus, 10)

    inf_list = []
    vacc_list = []

    print("People", len(sim.population))
    assert len(sim.population) == 100

    for person in sim.population:
        if person.infection is not None:
            inf_list.append(person)
        elif person.is_vaccinated:
            vacc_list.append(person)

    print("Infected", len(inf_list))
    assert len(inf_list) == 10

    print("Vaccinated", len(vacc_list))
    assert len(vacc_list) == 70

    assert sim.total_vaccinated == len(vacc_list)


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus, initial_infected)

    sim.run()
