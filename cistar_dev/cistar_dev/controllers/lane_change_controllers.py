import numpy as np
import random
import traci

class StaticLaneChanger:
    # Equivalent to never_change_lanes_controller

    def __init__(self, veh_id):
        self.veh_id = veh_id

    def get_action(self, env):
        return env.vehicles[self.veh_id]['lane']


def never_change_lanes_controller():
    def controller(carID, env):
        return env.vehicles[carID]["lane"]
    return controller



class StochasticLaneChanger:

    def __init__(self, veh_id, speedThreshold = 5, prob = 0.5, dxBack = 0, dxForward = 60, gapBack = 10, gapForward = 5):
        self.veh_id = veh_id
        self.speedThreshold = speedThreshold
        self.prob = prob
        self.dxBack = dxBack
        self.dxForward = dxForward
        self.gapBack = gapBack
        self.gapForward = gapForward

    def get_action(self, env):
        """
        Determines optimal lane
        :param carID: id of the vehicle of interest
        :param env: environment variable
        :return: controller specified velocity for specific car
        """
        num_lanes = env.scenario.lanes
        v = [0] * env.scenario.lanes
        for lane in range(num_lanes):
            # count the cars in this lane
            leadID = env.get_leading_car(self.veh_id, lane)
            trailID = env.get_trailing_car(self.veh_id, lane)

            if not leadID or not trailID:
                # empty lanes are assigned maximum speeds
                v[lane] = env.vehicles[self.veh_id]['max_speed']
                continue

            leadPos = env.get_x_by_id(leadID)
            trailPos = env.get_x_by_id(trailID)

            thisPos = env.get_x_by_id(self.veh_id)

            headway = (leadPos - thisPos) % env.scenario.length  # d_l
            footway = (thisPos - trailPos) % env.scenario.length  # d_f

            if headway < self.gapForward or footway < self.gapBack:
                # if cars are too close together, set lane velocity to 0
                v[lane] = 0
                continue

            # otherwise set v[lane] to the mean velocity of all cars in the region
            other_car_ids = env.get_cars(self.veh_id, dxBack = self.dxBack, dxForward = self.dxForward, lane = lane)
            v[lane] = np.mean([env.vehicles[other_id]["speed"] for other_id in other_car_ids])

        maxv = max(v)  # determine max velocity
        maxl = v.index(maxv)  # lane with max velocity
        myv = v[env.vehicles[self.veh_id]['lane']]  # speed of lane where car with specified self.veh_id is located

        # choosing preferred lane:
        # new lane is chosen with a probability prob
        # if its velocity is sufficiently greater than that of the current lane
        if maxl != env.vehicles[self.veh_id]['lane'] and \
           (maxv - myv) > self.speedThreshold and \
           random.random() < self.prob:
           return maxl
        return env.vehicles[self.veh_id]['lane']        


def stochastic_lane_changer(speedThreshold = 5, prob = 0.5,
                            dxBack = 0, dxForward = 60,
                            gapBack = 10, gapForward = 5):
    """
    Intelligent lane changer
    :param speedThreshold: minimum speed increase required
    :param prob: probability change will be requested if warranted = this * speedFactor
    :param dxBack: Farthest distance back car can see
    :param dxForward: Farthest distance forward car can see
    :param gapBack: Minimum required clearance behind car
    :param gapForward: Minimum required clearance in front car
    :return: carFn to input to a carParams
    """
    def controller(carID, env):
        """
        Determines optimal lane
        :param carID: id of the vehicle of interest
        :param env: environment variable
        :return: controller specified velocity for specific car
        """
        num_lanes = env.scenario.lanes
        v = [0] * env.scenario.lanes
        for lane in range(num_lanes):
            # count the cars in this lane
            leadID = env.get_leading_car(carID, lane)
            trailID = env.get_trailing_car(carID, lane)

            if not leadID or not trailID:
                # empty lanes are assigned maximum speeds
                v[lane] = env.vehicles[carID]['max_speed']
                continue

            leadPos = env.get_x_by_id(leadID)
            trailPos = env.get_x_by_id(trailID)

            thisPos = env.get_x_by_id(carID)

            headway = (leadPos - thisPos) % env.scenario.length  # d_l
            footway = (thisPos - trailPos) % env.scenario.length  # d_f

            if headway < gapForward or footway < gapBack:
                # if cars are too close together, set lane velocity to 0
                v[lane] = 0
                continue

            # otherwise set v[lane] to the mean velocity of all cars in the region
            other_car_ids = env.get_cars(carID, dxBack = dxBack, dxForward = dxForward, lane = lane)
            v[lane] = np.mean([env.vehicles[other_id]["speed"] for other_id in other_car_ids])

        maxv = max(v)  # determine max velocity
        maxl = v.index(maxv)  # lane with max velocity
        myv = v[env.vehicles[carID]['lane']]  # speed of lane where car with specified carID is located

        # choosing preferred lane:
        # new lane is chosen with a probability prob
        # if its velocity is sufficiently greater than that of the current lane
        if maxl != env.vehicles[carID]['lane'] and \
           (maxv - myv) > speedThreshold and \
           random.random() < prob:
           return maxl
        return env.vehicles[carID]['lane']

    return controller
