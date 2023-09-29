'''
Code for an entity in the network. This is where you should implement the
distance-vector algorithm.
'''

import packet as pk
import math



class Entity:
    '''
    Entity that represents a node in the network.

    Each function should be implemented so that the Entity can be instantiated
    multiple times and successfully run a distance-vector routing algorithm.
    '''

    def __init__(self, entity_index, number_entities):
        '''
        This initialization function will be called at the beginning of the
        simulation to setup all entities.

        Arguments:
        - `entity_index`:    The id of this entity.
        - `number_entities`: Number of total entities in the network.

        Return Value: None.
        '''
        # Save state
        self.index = entity_index
        self.number_of_entities = number_entities
        self.dist_vec = [[(math.inf, math.inf) for i in range(number_entities)] for j in range(number_entities)]

        self.neighbor_index = []
        # print("BEFORE zero DEBUG init DV")
        # print(self.dist_vec)
        #https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
        for i in range(0, number_entities):
            #Update cost to 0 for a nodes dist to itself
            self.dist_vec[i][i] = (0, i)
            # print("NEXT ROUND")
            # print(self.dist_vec[0])
            # print(self.dist_vec[1])
            # print(self.dist_vec[2])
            # print(self.dist_vec[i][i])

        # print("DEBUG init DV")
        # print(self.dist_vec)

        # print("------------------------------")


    def initialize_costs(self, neighbor_costs):
        '''
        This function will be called at the beginning of the simulation to
        provide a list of neighbors and the costs on those one-hop links.

        Arguments:
        - `neighbor_costs`:  Array of (entity_index, cost) tuples for
                             one-hop neighbors of this entity in this network.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''

        pack_list = []


        #Initializing neighbor costs should be accepted because they are infinity before
        neighbor_indices = []

        for tup in neighbor_costs:
            neighbor_indices.append(tup[0]) #Track neighbor indices
            self.neighbor_index.append(tup[0])
            #the tuple is: (neighbor_index, cost)
            #CHECK -- if the neighbor index is itself???
            self.dist_vec[self.index][tup[0]] = (tup[1], tup[0])
            #update this entities dist vec with first index. Second index is the correct spot in the DV. value is cost.


        #Must return array of 0 or more packets. Send DV to each neighbor

        #Grab the dist vec ---->> self.dist_vec[self.index]
        for neighbor in neighbor_indices:
            #create a packet to send and add to pack list
            #add the sending node's index num to the end of array sent. Make it easier to tell at recipient who to update
            dv = self.dist_vec[self.index]
            #dv_plus_sender_index.append(self.index)
            new_packet = pk.Packet(neighbor, dv)
            new_packet.set_source(self.index)
            pack_list.append(new_packet)

        # print("Sanity check: pack list in init costs is:")
        # print(pack_list)


        return pack_list


    def update(self, packet):
        # print("Start update fn")
        # print(self.dist_vec)
        # print("-----------")
        '''
        This function is called when a packet arrives for this entity.

        Arguments:
        - `packet`: The incoming packet of type `Packet`.

        Return Value: This function should return an array of `Packet`s to be
        sent from this entity (if any) to neighboring entities.
        '''

        #update the sending node's DV row in the recipient's overall table

        #how to get sending node's index? IT IS THE LAST SPOT IN ARRAY SENT! I AM PUTTING INDEX THERE

        #self.dist_vec[packet[-1]] = packet
        for i in range(0, self.number_of_entities):        #len(packet.get_costs()
            #self.dist_vec[packet.get_costs()[packet.get_source()]][i] = packet[i]
            # print("Packet recevied. peek at dv sent in so i can parse it rightly")
            # print(packet.get_costs())
            self.dist_vec[packet.get_source()][i] = packet.get_costs()[i]
        #this updates one row -- the sender's row.
        #index of sender is in last spot of packet.
        #and i update it one by one

        #now, check if i need to update the node's row with anything.
        updated = False     #If update something, change to true
        #i is the target index
        for i in range(0, self.number_of_entities):


            #find min cost for each spot in DV
            #Consider for each nieghbor!!!
            #min cost starts from the one node's index to a neighbor
            # then, 2nd part is from neighbor to final node it is trying to get to
            for neighbor in self.neighbor_index:
                if (self.index == 0):
                    print("Neighbor is:", neighbor)
                # print("AYYYYY")
                # print(self.dist_vec)
                cost = self.dist_vec[self.index][neighbor][0] + self.dist_vec[neighbor][i][0]
                # interesting_case = False
                # if (i == 2 & self.index == 0):
                #     print("Interesting case")
                #     interesting_case = True
                #     print("COST IS:", cost)
                # if (i == 0 & self.index == 2):
                #     print("Interesting case")
                #     interesting_case = True

                #if (cost == 3 & (self.index == 0 or self.index == 2)): #interesting_case == True):
                    # print("Found it")
                    # print("neighbor is : ", neighbor)
                    # print("Source entity is ", self.index)
                    #
                    # print("SRC", self.index, "to target", i, "stored (Cost, neighbor) is")
                    # print(self.dist_vec[self.index][i])

                #Compare cost to the old value. update if necessary
                if (cost < self.dist_vec[self.index][i][0]):
                    #if (self.index == 0):
                        # print("DV BEFORE UPDATE")
                        # print(self.dist_vec)
                        # print("the target to change is:", i)
                        # print("neighbor is", neighbor)
                        # print("cost:", cost)
                        # print("show real vals now")
                        # print(self.dist_vec[self.index][neighbor][0])
                        # print(self.dist_vec[neighbor][i][0])
                        #
                        # print("DV AFTER UPDATE")
                        # print(self.dist_vec)

                    self.dist_vec[self.index][i] = (cost, self.dist_vec[self.index][neighbor][1])     #was neighbor before. But issue --
                    #i may have a neighbor... BUT the efficient way to get to that neighbor is not direct!!
                    #Access it by saying from this src to tits neighbot (ex. from 0 to neighbor 2, give me the best path to it
                    #if this screws other stuff up, i didnt initialize it correctly then.
                    #because i am accessing the spot in dist vec for a node
                    updated = True


        #WHEN RETURNIONG, FOLLOW CONVENTION OF SENDING INDEX IN LAST SPOT OF ARRAY
        pack_list = []
        if (updated == True):
            for neighbor in self.neighbor_index:
                #send a packet to each neighbor
                dv = self.dist_vec[self.index]
                #dv_plus_sender_index.append(self.index)
                new_packet = pk.Packet(neighbor, dv)
                new_packet.set_source(self.index)
                pack_list.append(new_packet)
        # print("END update fn")
        # print(self.dist_vec)
        # print("-----------")
        return pack_list



    def get_all_costs(self):
        '''
        This function is used by the simulator to retrieve the calculated routes
        and costs from an entity. This is most useful at the end of the
        simulation to collect the resulting routing state.

        Return Value: This function should return an array of (next_hop, cost)
        tuples for _every_ entity in the network based on the entity's current
        understanding of those costs. The array should be sorted such that the
        first element of the array is the next hop and cost to entity index 0,
        second element is to entity index 1, etc.
        '''
        all_costs = []
        for i in range(0, self.number_of_entities):
            all_costs.append((self.dist_vec[self.index][i][1], self.dist_vec[self.index][i][0]))
        #print("ALL COSTS")
            #from the current entity, itll get the dist vec row for that one.
        return all_costs

    def forward_next_hop(self, destination):
        '''
        Return the best next hop for a packet with the given destination.

        Arguments:
        - `destination`: The final destination of the packet.

        Return Value: The index of the best neighboring entity to use as the
        next hop.
        '''
        return self.dist_vec[self.index][destination][1]


