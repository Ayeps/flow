"""Script containing the base vehicle kernel class."""


class KernelVehicle(object):
    """Flow vehicle kernel.

    This kernel sub-class is used to interact with the simulator with regards
    to all vehicle-dependent components. Specifically, this class contains
    methods for:

    * Interacting with the simulator: This includes apply acceleration, lane
      change, and routing commands to specific vehicles in the simulator. In
      addition, methods exist to add or remove a specific vehicle from the
      network, and update internal state information after every simulation
      step in order to support and potentially speed up all state-acquisition
      methods.
    * Visually distinguishing vehicles by type: In the case when some vehicles
      are controlled by a reinforcement learning agent or some other
      controller, these methods can be used to visually distinguish the
      vehicles during rendering by RL/actuated, human-observed, and
      human-unobserved. The traci simulator, for instance, renders RL vehicles
      as red, observed human vehicles as cyan, and unobserved human vehicles as
      white. In the absence of RL/actuated agents, all vehicles are white.
    * State acquisition: Finally, this methods contains several methods for
      acquiring state information from specific vehicles. For example, if you
      would like to get the speed of a vehicle from the environment, that can
      be done by calling:

        >>> from flow.envs.base_env import Env
        >>> env = Env(...)
        >>> veh_id = "test_car"  # name of the vehicle
        >>> speed = env.k.vehicle.get_speed(veh_id)

    All methods in this class are abstract, and must be filled in by the child
    vehicle kernel of separate simulators.
    """

    def __init__(self,
                 master_kernel,
                 kernel_api,
                 sim_params):
        """Instantiate the Flow vehicle kernel.

        Parameters
        ----------
        master_kernel : flow.core.kernel.Kernel
            the higher level kernel (used to call methods from other
            sub-kernels)
        kernel_api : any
            an API that may be used to interact with the simulator
        sim_params : flow.core.params.SumoParams  # FIXME: make ambiguous
            simulation-specific parameters
        """
        self.master_kernel = master_kernel
        self.kernel_api = kernel_api
        self.sim_step = sim_params.sim_step

    ###########################################################################
    #               Methods for interacting with the simulator                #
    ###########################################################################

    def update(self, reset):
        """Update the vehicle kernel with data from the current time step.

        This method is used to optimize the computational efficiency of
        acquiring vehicle state information from the kernel.

        Parameters
        ----------
        reset : bool
            specifies whether the simulator was reset in the last simulation
            step
        """
        raise NotImplementedError

    def add(self, veh_id, initial_params):
        """Add a vehicle to the network.

        Parameters
        ----------
        veh_id : str
            unique identifier of the vehicle to be added
        initial_params : dict
            dictionary specifying the initial speed, position, route, and type
            of the vehicle being added
        """
        raise NotImplementedError

    def remove(self, veh_id):
        """Remove a vehicle.

        This method removes all traces of the vehicle from the vehicles kernel
        and all valid ID lists, and decrements the total number of vehicles in
        this class.

        In addition, if the vehicle is still in the network, this method calls
        the necessary simulator-specific commands to remove it.

        Parameters
        ----------
        veh_id : str
            unique identifier of the vehicle to be removed
        """
        raise NotImplementedError

    def apply_acceleration(self, veh_ids, acc):
        """Apply the acceleration requested by a vehicle in the simulator.

        Parameters
        ----------
        veh_ids : list of str
            list of vehicle identifiers
        acc : numpy ndarray or list of float
            requested accelerations from the vehicles
        """
        raise NotImplementedError

    def apply_lane_change(self, veh_ids, direction):
        """Apply an instantaneous lane-change to a set of vehicles.

        This method also prevents vehicles from moving to lanes that do not
        exist, and set the "last_lc" variable for RL vehicles that lane changed
        to match the current time step, in order to assist in maintaining a
        lane change duration for these vehicles.

        Parameters
        ----------
        veh_ids : list of str
            list of vehicle identifiers
        direction : list of {-1, 0, 1}
            -1: lane change to the right
             0: no lane change
             1: lane change to the left

        Raises
        ------
        ValueError
            If any of the direction values are not -1, 0, or 1.
        """
        raise NotImplementedError

    def choose_routes(self, veh_ids, route_choices):
        """Update the route choice of vehicles in the network.

        Parameters
        ----------
        veh_ids : list
            list of vehicle identifiers
        route_choices : numpy ndarray or list of floats
            list of edges the vehicle wishes to traverse, starting with the
            edge the vehicle is currently on. If a value of None is provided,
            the vehicle does not update its route
        """
        raise NotImplementedError

    ###########################################################################
    # Methods to visually distinguish vehicles by {RL, observed, unobserved}  #
    ###########################################################################

    def update_vehicle_colors(self):
        """Modify the color of vehicles if rendering is active."""
        raise NotImplementedError

    def set_observed(self, veh_id):
        """Add a vehicle to the list of observed vehicles."""
        raise NotImplementedError

    def remove_observed(self, veh_id):
        """Remove a vehicle from the list of observed vehicles."""
        raise NotImplementedError

    def get_observed_ids(self):
        """Return the list of observed vehicles."""
        raise NotImplementedError

    ###########################################################################
    #                        State acquisition methods                        #
    ###########################################################################

    def get_ids(self):
        """Return the names of all vehicles currently in the network."""
        raise NotImplementedError

    def get_human_ids(self):
        """Return the names of all non-rl vehicles currently in the network."""
        raise NotImplementedError

    def get_controlled_ids(self):
        """Return the names of all flow acceleration-controlled vehicles.

        This only include vehicles that are currently in the network.
        """
        raise NotImplementedError

    def get_controlled_lc_ids(self):
        """Return the names of all flow lane change-controlled vehicles.

        This only include vehicles that are currently in the network.
        """
        raise NotImplementedError

    def get_rl_ids(self):
        """Return the names of all rl-controlled vehicles in the network."""
        raise NotImplementedError

    def get_ids_by_edge(self, edges):
        """Return the names of all vehicles in the specified edge.

        If no vehicles are currently in the edge, then returns an empty list.
        """
        raise NotImplementedError

    def get_inflow_rate(self, time_span):
        """Return the inflow rate (in veh/hr) of vehicles from the network.

        This value is computed over the specified **time_span** seconds.
        """
        raise NotImplementedError

    def get_outflow_rate(self, time_span):
        """Return the outflow rate (in veh/hr) of vehicles from the network.

        This value is computed over the specified **time_span** seconds.
        """
        raise NotImplementedError

    def get_num_arrived(self):
        """Return the number of vehicles that arrived in the last time step."""
        raise NotImplementedError

    def get_speed(self, veh_id, error=-1001):
        """Return the speed of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        float
        """
        raise NotImplementedError

    def get_absolute_position(self, veh_id, error=-1001):
        """Return the absolute position of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        float
        """
        raise NotImplementedError

    def get_position(self, veh_id, error=-1001):
        """Return the position of the vehicle relative to its current edge.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        float
        """
        raise NotImplementedError

    def get_edge(self, veh_id, error=""):
        """Return the edge the specified vehicle is currently on.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        str
        """
        raise NotImplementedError

    def get_lane(self, veh_id, error=-1001):
        """Return the lane index of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        int
        """
        raise NotImplementedError

    def get_route(self, veh_id, error=list()):
        """Return the route of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        list of str
        """
        raise NotImplementedError

    def get_length(self, veh_id, error=-1001):
        """Return the length of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        float
        """
        raise NotImplementedError

    def get_leader(self, veh_id, error=""):
        """Return the leader of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        str
        """
        raise NotImplementedError

    def get_follower(self, veh_id, error=""):
        """Return the follower of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        str
        """
        raise NotImplementedError

    def get_headway(self, veh_id, error=-1001):
        """Return the headway of the specified vehicle(s).

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        float
        """
        raise NotImplementedError

    def get_last_lc(self, veh_id, error=-1001):
        """Return the last time step a vehicle changed lanes.

        Note: This value is only stored for RL vehicles. All other vehicles
        calling this will cause a warning to be printed and their "last_lc"
        term will be the error value.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        int
        """
        raise NotImplementedError

    def get_acc_controller(self, veh_id, error=None):
        """Return the acceleration controller of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        object
        """
        raise NotImplementedError

    def get_lane_changing_controller(self, veh_id, error=None):
        """Return the lane changing controller of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        object
        """
        raise NotImplementedError

    def get_routing_controller(self, veh_id, error=None):
        """Return the routing controller of the specified vehicle.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        object
        """
        raise NotImplementedError

    def get_lane_headways(self, veh_id, error=list()):
        """Return the lane headways of the specified vehicles.

        This includes the headways between the specified vehicle and the
        vehicle immediately ahead of it in all lanes.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        list of float
        """
        raise NotImplementedError

    def get_lane_leaders(self, veh_id, error=list()):
        """Return the leaders for the specified vehicle in all lanes.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        lis of str
        """
        raise NotImplementedError

    def get_lane_tailways(self, veh_id, error=list()):
        """Return the lane tailways of the specified vehicle.

        This includes the headways between the specified vehicle and the
        vehicle immediately behind it in all lanes.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : any, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        list of float
        """
        raise NotImplementedError

    def get_lane_followers(self, veh_id, error=list()):
        """Return the followers for the specified vehicle in all lanes.

        Parameters
        ----------
        veh_id : str or list of str
            vehicle id, or list of vehicle ids
        error : list, optional
            value that is returned if the vehicle is not found

        Returns
        -------
        list of str
        """
        raise NotImplementedError

    def get_x_by_id(self, veh_id):
        """Provide a 1-D representation of the position of a vehicle.

        Note: These values are only meaningful if the specify_edge_starts
        method in the scenario is set appropriately; otherwise, a value of 0 is
        returned for all vehicles.

        Parameters
        ----------
        veh_id : str
            vehicle identifier

        Returns
        -------
        float
        """
        raise NotImplementedError
