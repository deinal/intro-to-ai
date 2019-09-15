from citymap import CityMap


def main():
    """Implement search method of the CityMap class so that when searching for a route between
    two stops, it returns a route as a linked list where the returned State object points to the destination.

    For example when calling the search method with starting stop "1250429" and destination "1121480"
    it will return a linked list of the following form:

    1130446[GOAL] -> 1130442 -> 1140447 -> 1140436 -> 1140439 -> 1140440 -> 1150431 -> 1150433 -> 1150435[START] -> None

    NOTE: You can use predefined State class or return any object (including str itself) as long as it has
     __str__ method representing answer in the simple format: [time]stop_code(stop_name) -> [time]stop_code(stop_name) -> [time]stop_code(stop_name)
     See test_search.py for examples.
    """
    citymap = CityMap("graph.json", "routes.json")
    start = citymap.get_stop('1150435')
    goal = citymap.get_stop('1130446')
    departure_time = 4

    print(citymap.search(start, goal, departure_time))


if __name__ == '__main__':
    main()
