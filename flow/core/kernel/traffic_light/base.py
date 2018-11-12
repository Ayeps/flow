

class KernelTrafficLight(object):
    """Base traffic light kernel.

    This kernel sub-class is used to interact with the simulator with regards
    to all traffic light -dependent components. Specifically, this class
    contains methods for:

    * Interacting with the simulator: This consisting specifying the states of
      certain traffic lights at a given time step. This can be done by calling
      the following method:

        >>> from flow.envs.base_env import Env
        >>> env = Env(...)
        >>> node_id = 'test_intersection'  # name of the node
        >>> env.k.traffic_light.set_state(node_id, 'r')

    * State acquisition: This methods contains several methods for acquiring
      state information from specific traffic lights. For example, if you would
      like to get the state ("r", "g", etc.) of a node with a traffic light,
      that can be done by calling:

        >>> tl_state = env.k.traffic_light.get_state(node_id)

    All methods in this class are abstract, and must be filled in by the child
    vehicle kernel of separate simulators.
    """

    def __init__(self, master_kernel, kernel_api):
        """Instantiate the base traffic light kernel.

        Parameters
        ----------
        master_kernel : flow.core.kernel.Kernel
            the higher level kernel (used to call methods from other
            sub-kernels)
        kernel_api : any
            an API that may be used to interact with the simulator
        """
        self.master_kernel = master_kernel
        self.kernel_api = kernel_api

    def update(self, reset):
        """Update the states and phases of the traffic lights.

        This ensures that the traffic light variables match current traffic
        light data.

        Parameters
        ----------
        reset : bool
            specifies whether the simulator was reset in the last simulation
            step
        """
        raise NotImplementedError

    def get_ids(self):
        """Return the names of all nodes with traffic lights."""
        raise NotImplementedError

    def set_state(self, node_id, state, link_index="all"):
        """Set the state of the traffic lights on a specific node.

        Parameters
        ----------
        node_id : str
            name of the node with the controlled traffic lights
        state : str
            desired state(s) for the traffic light
        link_index : int, optional
            index of the link whose traffic light state is meant to be changed.
            If no value is provided, the lights on all links are updated.
        """
        raise NotImplementedError

    def get_state(self, node_id):
        """Return the state of the traffic light(s) at the specified node.

        Parameters
        ----------
        node_id: str
            name of the node

        Returns
        -------
        state : str
            Index = lane index
            Element = state of the traffic light at that node/lane
        """
        raise NotImplementedError
