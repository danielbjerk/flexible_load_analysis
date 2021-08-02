import network
import numpy as np

def add_new_load_to_network(n_new_load_name, n_new_load_data, n_parent_node_ID, n_old_loads, g_network):
    #n_old_loads[n_load.ID] = n_load
    n_old_loads[n_new_load_name] = n_new_load_data
    network.add_node(g_network, n_new_load_name, n_parent_node_ID)
    return n_old_loads, g_network

def remove_node_from_network(n_loads, g_network, n_node):
    n_loads.pop(n_node)
    g_network = network.remove_node(g_network, n_node)
    return n_loads, g_network


def interactively_add_new_loads_to_network(n_loads, g_network):

    bool_continue_adding_loads = True
    while bool_continue_adding_loads:
        
        bool_successfully_generated_load = False
        while not bool_successfully_generated_load:
            print("Select how to generate the new load")
            print(30 * "-" , "MENU" , 30 * "-")
            print("1: Copy of existing load")
            print("2: Model based on existing load")
            print("3: Model based on max power")
            print("4: Model based on load-categorization")

            print(67 * "-")

            str_choice = input()

            if str_choice == '1':
                #n_new_load_data = interactively_copy_existing_load(n_loads)
                n_new_load_data = np.array([[1, 200], [2, 300], [3, 400]])
            elif str_choice == '2':
                #n_new_load_data = interactively_model_based_on_existing_load(n_loads)
                n_new_load_data = np.array([[1, 200], [2, 300], [3, 400]])
            elif str_choice == '3':
                #n_new_load_data = interactively_model_based_on_max_power(n_loads)
                n_new_load_data = np.array([[1, 200], [2, 300], [3, 400]])
            elif str_choice == '4':
                #n_new_load_data = interactively_model_based_on_categorization(n_loads)
                n_new_load_data = np.array([[1, 200], [2, 300], [3, 400]])
            else:
                print("Input not recognized, try again!")
                continue
        
            # graphically represent n_new_load_data
            print("New load generated: ")
            print(n_new_load_data)
            bool_retry_input = True
            while bool_retry_input:
                print("Is the generated load correct? yes/no")
                str_choice = str.lower(input())
                if str_choice == "yes" or str_choice == 'y':
                    bool_successfully_generated_load = True
                    bool_retry_input = False
                elif str_choice == "no" or str_choice == 'n':
                    bool_successfully_generated_load = False
                    bool_retry_input = False
                else:
                    print("Unrecognizd input, try again")
                    bool_retry_input = True

            if not bool_successfully_generated_load:
                bool_retry_input = True
                while bool_retry_input:
                    print("Try generating load again or abort? g/a")
                    str_choice = str.lower(input())
                    if str_choice == 'g':
                        print("Restarting load-generation")
                        bool_successfully_generated_load = False
                        bool_retry_input = False
                    elif str_choice == 'a':
                        print("Aborting adding of new load to network!")
                        bool_retry_input = False
                        return n_loads, g_network
                    else:
                        print("Unrecognizd input, try again")
                        bool_retry_input = True            

        print("Successfully generated new load data!")

        print("Add the new load to the network")
        # function interactively_add_load_to_network
        # print network
        print("Input name of new load-point")
        n_new_load_name = input()
        
        bool_happy_with_load_placement = False
        while not bool_happy_with_load_placement:
            print("Network as of right now:")
            network.plot_network(g_network)
 
            print("Nodes in network: ")
            list_nodes_in_network = network.list_nodes(g_network)
            print(list_nodes_in_network)

            print("Input name of parent node of", n_new_load_name)
            n_parent_node = input()

            if not n_parent_node in list_nodes_in_network:
                print("Unrecognized parent node, try again!")
                continue
            else:
                # Check if not trafo/not compatible node, then 
                # add newload to new network
                n_loads, g_network = add_new_load_to_network(n_new_load_name, n_new_load_data, n_parent_node, n_loads, g_network)

                print("The new network will look as follows:")
                network.plot_network(g_network)

                # Are you happy?
                # if yes: g_network = g_new_network
                # if not: try again or abort?
                bool_retry_input = True
                while bool_retry_input:
                    print("Happy with the placement? yes/no")
                    str_choice = str.lower(input())
                    if str_choice == "yes" or str_choice == "y":
                        bool_happy_with_load_placement = True
                        bool_retry_input = False

                    elif str_choice == "no" or str_choice == "n":
                        bool_retry_input = False
                        bool_retry_input_nested = True
                        n_loads, g_network = remove_node_from_network(n_loads, g_network, n_new_load_name)

                        while bool_retry_input_nested:
                            print("Retry placing load again or abort? r/a")
                            str_choice = str.lower(input())
                            if str_choice == 'r':
                                bool_happy_with_load_placement = False
                                bool_retry_input_nested = False
                            elif str_choice == 'a':
                                print("Aborting adding of new load to network!")
                                bool_retry_input_nested = False
                                return n_loads, g_network
                            else:
                                print("Unrecognizd input, try again")
                                bool_retry_input_nested = True
                    else:
                        print("Unrecognizd input, try again")
                        bool_retry_input = True
        
        print("Do you want to stop adding loads to netork (No)/Yes?")
        str_choice = str.lower(input())
        if str_choice == "yes" or str_choice == 'y':
            bool_continue_adding_loads = False

    print("Finished adding loads to network!")
    return n_loads, g_network


def UI(n_loads, g_network):

    list_choice_log = []
    bool_continue = True

    while bool_continue:
        print("Recieved the following customers: ")
        for key in n_loads:
            print(key)
        print("Recieved the following network: ")
        print(g_network)
        print(30 * "-" , "MENU" , 30 * "-")
        print("1: Examine loads")    # plot data (timeseries) of chosen customer
        print("2: Add new load")
        print("3: Modify load")
        print("4: Modify network")
        print("9: Exit modification")
        print(67 * "-")

        str_choice = input()
        list_choice_log.append(str_choice)

        if str_choice == '1':
            #inspect_desired_loads_until_exit_signal()
            print("Not yet implemented!")
        elif str_choice == '2':
            interactively_add_new_loads_to_network(n_loads, g_network)
        elif str_choice == '3':
            #modify_load_in_net_work()
            print("Not yet implemented!")
        elif str_choice == '4':
            #modify_network()
            print("Not yet implemented!")
        elif str_choice == '9':
            print("Exiting grid_modification!")
            bool_continue = False
        else:
            print("Input not recognized, try again!")
        
    return n_loads, g_network