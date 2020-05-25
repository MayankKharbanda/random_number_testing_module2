import argparse

def parse_arg():
    
    '''
    The function takes command line arguments.

    Returns
    -------
    args : all the argument values.

    '''
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--iteration", dest = "iteration", help="Number of random files", type=int, required=True)
    #number of random file to run test file on.
    
    parser.add_argument("-t", "--tests_file", dest = "tests_file", help="Location of file containing tests to execute", type=str, required=True)
    #path to test file, containing description of all the tests to run(Compulsory).
    
    parser.add_argument("-d", "--dest_loc", dest = "dest_loc", default = "results", help="Location where the results are stored", type=str)
    #destination to store result.
    
    parser.add_argument("-c", "--cores", dest = "cores", default = "4", help="Number of cores for process", type=int)
    #number of cores to make a process for each to run tests.
    
    parser.add_argument("-m", "--test_files_path", dest = "random_path", help="Path to files containing random numbers", type=str, required=True)
    #maximum size of the file to be created for testing.
    
    args = parser.parse_args()
    
    return args