import multiprocessing
import os
import time
from process_allocation_algo import process_alloc
import config
from test_reader import test_reader
from signal import signal, SIGINT
import sys
from core_function import process
from config_arg import parse_arg
import subprocess








#arguments parsing
ARGS = parse_arg()
NUMBER_OF_ITERATIONS = ARGS.iteration
RESULT_DEST = ARGS.dest_loc
CORES = ARGS.cores
RANDOM_PATH = ARGS.random_path










def exit_func(signal_received, frame):  
    
    '''
    the function handles exit from module.
    '''
    


    module_end_time = time.time()       #evaluating module running time and storing it
    module_running_time = module_end_time - module_start_time

    with open(f'{RESULT_DEST}/module_report.txt','w') as fw:
        fw.write("Module running time (in s) :"+str(module_running_time)+"\n")
        
    print('EXITING...')
    
    sys.exit(0)












module_start_time = time.time()

Tests = test_reader(ARGS.tests_file)    #contains the list of all the tests to run on random number generator.


#Total tests in test file
total_tests_all = len(Tests)








#local events for each process
process_event = []
for i in range(CORES):
    process_event.append(multiprocessing.Event())
    process_event[i].set()


#global event
process_event_global = multiprocessing.Event()
process_event_global.set()








#variable for each process running
process_arr = [None]*CORES
iteration_over_tests = 0    #iteration over the test file







signal(SIGINT, exit_func)   #initialization of signal to handle exit from module









while(True):        #infinite loop over test-file

    



    tests_completed = 0    #total tests completed till this moment.
    total_wait_time = 0     #total wait time for the main module.




    #exit from loop
    if(iteration_over_tests == int(NUMBER_OF_ITERATIONS)):
        exit_func(None, None)
    
    
    iteration_over_tests = iteration_over_tests + 1
    
    
    
    
    
    
    #array contaning n-lists of tests, each for a particular core according 
    #to time to execute.
    process_list = process_alloc(Tests, CORES)






    #check if test execution time exists.
    if(process_list!=-1):

        
                
        #array of number of tests in a particular core
        total_tests_arr = []

        for i in range(CORES):
            total_tests_arr.append(len(process_list[i]))



        
        #contains the number of tests allocated on a core
        process_comleted_arr = []
        for i in range(CORES):
            process_comleted_arr.append(0)
    

        while tests_completed < total_tests_all:
                                    
            #wait time calculation
            start_time = time.time()
            process_event_global.wait()
            end_time = time.time()
            
            #resetting global event
            process_event_global.clear()                
            total_wait_time = total_wait_time + (end_time - start_time)
    
    
    
        
            #checking each core to find which generated event.
            for i in range(CORES):
        
                if(process_event[i].is_set() and process_comleted_arr[i] < total_tests_arr[i]):
                
                    #resetting local event
                    process_event[i].clear()
                    
                    
                    
                    
                    test_file = RANDOM_PATH+f'_{iteration_over_tests-1}.bin'
                    
                    out = subprocess.run(f'test -e {test_file} && echo True || echo False ', stdout=subprocess.PIPE, shell = True)
                    FILE_EXIST = out.stdout.decode('utf-8')
                    if('True' not in FILE_EXIST):
                        print('!!!Random File doesn\'t exist.!!!' )
                        sys.exit(0)
                    
                    
                    
                    
                    process_start_time = time.time()        #contains the start time of the test executing.
                    #starting the process
                    process_arr[i] = multiprocessing.Process(target=process, args=(process_list[i][process_comleted_arr[i]], process_event_global, process_event[i], test_file, iteration_over_tests, process_start_time, i, RESULT_DEST))
                    
                    try:
                        process_arr[i].start()
                    except:
                        print('!!!Error in process core {i}, test {process_list[i][process_comleted_arr[i]]}, exiting')
                        sys.exit(0)
                        



                    process_comleted_arr[i] = process_comleted_arr[i] + 1
                    tests_completed = tests_completed + 1
                
            






    else:
        
        
        
        
        while tests_completed < total_tests_all:
        
            #wait time calculation
            start_time = time.time()
            process_event_global.wait()
            end_time = time.time()
        
            #resetting global event
            process_event_global.clear()
            total_wait_time = total_wait_time + (end_time - start_time)
    
    
    
    
        
            #checking each core to find which generated event.
            for i in range(CORES):
      
                
                if(process_event[i].is_set() and tests_completed < total_tests_all):
                    
                    #resetting local event
                    process_event[i].clear()
                    
                    
                    
                    test_file = RANDOM_PATH+f'_{iteration_over_tests-1}.bin'
                    
                    out = subprocess.run(f'test -e {test_file} && echo True || echo False ', stdout=subprocess.PIPE, shell = True)
                    FILE_EXIST = out.stdout.decode('utf-8')
                    if('True' not in FILE_EXIST):
                        print('!!!Random File doesn\'t exist.!!!' )
                        sys.exit(0)
                    
                    
                    

                    process_start_time = time.time()        #contains the start time of the test executing.
                    #starting the process
                    process_arr[i] = multiprocessing.Process(target=process, args=(Tests[tests_completed], process_event_global, process_event[i], test_file, iteration_over_tests, process_start_time, i, RESULT_DEST))
                    
                    try:
                        process_arr[i].start()
                    except:
                        print('!!!Error in process core {i}, test {Tests[tests_completed]}, exiting')
                        sys.exit(0)
                
                
                    tests_completed = tests_completed + 1
                
                





    #waiting for each core to complete execution
    for i in range(CORES):
        process_event[i].wait()




    #Writing all the details to output file
    for Test in Tests:    
        if(Test[config.SUITE]=='dieharder' and 
           (Test[config.ID] == '200' 
            or Test[config.ID] == '201' 
            or Test[config.ID] == '202' 
            or Test[config.ID] == '203')):
            
            
            with open(f'{RESULT_DEST}/file_{iteration_over_tests}/{Test[config.SUITE]}_{Test[config.ID]}_{Test[config.N_TUPL]}_time.txt','r') as fr:
                Test[config.TIME] = str(round(float((fr.readline()).strip()),2))
            os.system(f'rm {RESULT_DEST}/file_{iteration_over_tests}/{Test[config.SUITE]}_{Test[config.ID]}_{Test[config.N_TUPL]}_time.txt')
        else:
            with open(f'{RESULT_DEST}/file_{iteration_over_tests}/{Test[config.SUITE]}_{Test[config.ID]}_time.txt','r') as fr:
                Test[config.TIME] = str(round(float((fr.readline()).strip()),2))
            os.system(f'rm {RESULT_DEST}/file_{iteration_over_tests}/{Test[config.SUITE]}_{Test[config.ID]}_time.txt')






    #storing the wait time into file
    with open(f'{RESULT_DEST}/file_{iteration_over_tests}/final_report.txt','w') as fw:
        fw.write("Total_wait_time (in s) :"+str(total_wait_time)+"\n")
        fw.write('SUITE'.rjust(15))
        fw.write('NAME'.rjust(30))
        fw.write('ID'.rjust(3))
        fw.write('TIME'.rjust(10))
        fw.write('SIZE'.rjust(15))
        fw.write('N_TUPLE'.rjust(10))
        fw.write("\n")
        for Test in range(len(Tests)):
            fw.write(Tests[Test][config.SUITE].rjust(15))
            fw.write(Tests[Test][config.NAME].rjust(30))
            fw.write(Tests[Test][config.ID].rjust(3))
            fw.write(Tests[Test][config.TIME].rjust(10))
            fw.write(Tests[Test][config.SIZE].rjust(15))
            if(len(Tests[Test]) == config.N_TUPL+1):
                fw.write(Tests[Test][config.N_TUPL].rjust(10))
            fw.write("\n")
    
