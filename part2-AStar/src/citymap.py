import json
import os
import queue as Q

from math import sqrt

MAX_TRAM_SPEED = 260.0
HUGE_NUMBER = 1000000


def dist(p1, p2):
    """ Distance between two points, format: (x, y) """
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def time_to_string(time):
    result = ""
    if time >= 60:
        result += str(int(time // 60)) + 'h'
    result += str(time % 60) + 'm'

    return result


def load_data(source_file):
    """Reading JSON from a file and deserializing it
    :param source_file: JSON object (str)
    :return: obj (array)
    """
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, '..', source_file)) as file:
            return json.load(file)
    except:
        print('Could not read %s file' % source_file)
        exit()


class State:
    """ State class lets you trace back the route from the last stop
    :attr stop: Stop (obj)
    :attr previous: Previous state of the route (State)
    :attr current_time: The time in minutes from the beginning of the trip (int)

    :static attr goal: The goal stop (obj)
    """

    goal = None

    def __init__(self, stop, time=0, previous=None):
        self.stop = stop
        self.current_time = time
        self.previous = previous

    def __str__(self):
        """ Returns route as a string from the last stop to the beginning.
            Format: [12m]1140439(Töölön halli) -> [10m]1140440(Kansaneläkelaitos) -> [8m]1150431(Töölön tulli)
        """
        result = '[' + time_to_string(self.current_time) + ']' + self.stop['code'] + '(' + self.stop[
            'name'] + ')'
        state = self.previous
        while state is not None:
            result += " -> " + '[' + time_to_string(state.current_time) + ']' + state.stop['code'] + '(' + \
                      state.stop['name'] + ')'
            state = state.previous

        return result

    def get_stop_code(self):
        return self.stop['code']

    def get_stop(self):
        return self.stop

    def get_previous(self):
        return self.previous

    def get_time(self):
        return self.current_time

    def __lt__(self, other):
        """ State comparator
        Note: current goal stop is stored in State.goal
        :param other:
        :return: Boolean
        """
        # Implement me
        return self.get_time() + self.heuristic() < other.get_time() + other.heuristic()

    def heuristic(self):
        """ Heuristic to evaluate lower bound on the time required to reach the destination from the stop
        Note: current goal stop is stored in State.goal
        :return: float
        """
        # Implement me
        p1 = (self.get_stop()["x"], self.get_stop()["y"])
        p2 = (State.goal["x"], State.goal["x"])
        return dist(p1, p2)/MAX_TRAM_SPEED
        


class CityMap:
    """Storage of the tram network
    :attr graph_data: (obj)
    :attr routes_data: (obj)
    :attr stops: dictionary {stop_code: stop}
    :attr routes: dictionary {route_code: route}
    """

    def __init__(self, stops_source_file, routes_source_file):
        self.graph_data = load_data(stops_source_file)
        self.routes_data = load_data(routes_source_file)
        self.stops = {}
        self.routes = {}
        for stop in self.graph_data:
            self.stops[stop["code"]] = stop
        for route in self.routes_data:
            self.routes[route["code"]] = route

    def get_stop(self, code):
        return self.stops[code]

    def get_neighbors(self, stop_code):
        """Returns dictionary containing all neighbor stops """
        return self.stops.get(stop_code)["neighbors"]

    def get_neighbors_codes(self, stop_code):
        """Returns codes of all neighbor stops """
        return list(self.stops.get(stop_code)["neighbors"].keys())

    def fastest_transition(self, from_code, dest_code, current_time):
        """Returns the fastest transition time between two stops in a direction from_code -> dest_code
           Also counts the waiting time.
        """
        neighbors = self.get_neighbors(from_code)
        transition_time = HUGE_NUMBER

        if dest_code not in neighbors:
            print('There is no railway to this stop! ')
            exit()
        else:
            routes_codes = neighbors[dest_code]
            for rc in routes_codes:
                route = self.routes.get(rc)
                i = route['stopCodes'].index(from_code)
                wait_time = (route['stopTimes'][i] % 10) - (current_time % 10)
                wait_time = (wait_time + 10) if (wait_time < 0) else wait_time
                travel_time = route['stopTimes'][i + 1] - route['stopTimes'][i]
                if transition_time > (wait_time + travel_time):
                    transition_time = wait_time + travel_time

        return transition_time

    def search(self, start, goal, time_of_beginning):
        """Implement A* search. Return the answer as a linked list of States
        where the first node contains the goal stop, time of travel and each node is linked to the previous node in the path.
        The last node in the list is the starting stop and its previous node is None.

        :param start: Initial stop (obj)
        :param goal: Last stop (obj)
        :param time_of_beginning: Time when the trip started (int < 10)

        :returns (obj)
        """
        # Specify goal for correct heuristic and comparator methods
        State.goal = goal

        to_visit = Q.PriorityQueue()
        to_visit.put(State(start, time_of_beginning))

        # Implement me
        visited = []
        while to_visit:
            node = to_visit.get()
            if node not in visited:
                visited.append(node)
                if node.get_stop() == goal:
                    return node
                current_code = node.get_stop_code()
                current_time = node.get_time()
                for neighbor in self.get_neighbors_codes(current_code):
                    time = current_time + self.fastest_transition(current_code, neighbor, current_time)
                    to_visit.put(State(self.get_stop(neighbor), time, node))
        return None
