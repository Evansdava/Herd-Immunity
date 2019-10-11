class Logger(object):
    """Utility class to log all interactions during the simulation."""

    # TODO: Write a test suite for this class to make sure each method is
    # working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        """Initialize starting values"""
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage,
                       virus_name, mortality_rate, basic_repro_num):
        """
        The simulation class should use this method immediately to log the
        specific parameters of the simulation as the first line of the file.
        """
        f = open(self.file_name, "w")
        f.write(f"Pop_size: {pop_size}    Vacc_percentage: {vacc_percentage}"
                f"    Virus_name: {virus_name}    Mortality_rate: "
                f"{mortality_rate}    Repro_num: {basic_repro_num}\n")
        f.close()

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        r"""
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects
        {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated'
            or 'already sick'} \n"
        """
        f = open(self.file_name, "a")
        if did_infect:
            f.write(f"Person {person._id} infects person {random_person._id}"
                    "\n")
        elif random_person_vacc:
            f.write(f"Person {person._id} does not infect person "
                    f"{random_person._id} because vaccinated\n")
        elif random_person_sick:
            f.write(f"Person {person._id} does not infect person "
                    f"{random_person._id} because already infected\n")
        else:
            f.write(f"Person {person._id} does not infect person "
                    f"{random_person._id}\n")
        f.close()

    def log_infection_survival(self, person, did_die_from_infection):
        r"""
        The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived
            infection.\n"
        """
        f = open(self.file_name, "a")
        if did_die_from_infection:
            f.write(f"Person {person._id} died from infection\n")
        else:
            f.write(f"Person {person._id} survived infection\n")
        f.close()

    def log_time_step(self, time_step_number, new_infections=0, new_deaths=0,
                      new_vaccinations=0, total_infections=0, total_deaths=0,
                      total_vaccinations=0, vacc_saves=0):
        r"""
        STRETCH CHALLENGE DETAILS:

        If you choose to extend this method, the format of the summary
        statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time
            step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including
            the newly infected
            The total number of dead, including those that died during this
            time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning
            {time_step_number + 1}\n"
        """
        # TODO: Finish this method. This method should log when a time step
        # ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        f = open(self.file_name, "a")
        f.write(f"""Infections this step: {new_infections}
Total infections: {total_infections}
Deaths this step: {new_deaths}
Total deaths: {total_deaths}
Vaccinations this step: {new_vaccinations}
Total Vaccinations: {total_vaccinations}
Possible infections stopped by Vaccination: {vacc_saves}
""")
        f.write(f"Time step {time_step_number} ended, beginning "
                f"{time_step_number + 1}\n")
        f.close()
