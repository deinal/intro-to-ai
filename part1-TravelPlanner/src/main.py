from citymap import CityMap


def main():
    """Implement search method of the CityMap class so that when searching for a route between
    two stops, it returns a route as a linked list where the returned State object points to the destination.

    For example when calling the travelplanner with starting stop "1250429" and destination "1121480"
    it will return a linked list of the following form:

    1121480[GOAL] -> 1121438 -> 1220414 -> 1220416 -> 1220418 -> 1220420 -> 1220426 -> 1173416 ->
    1173423 -> 1250425 -> 1250427 -> 1250429[START] -> null

    NOTE: You can use predefined State class or return any object (including str itself) as long as it has
     __str__ method representing answer in the simple format: stop_code -> stop_code -> stop_code.
    """
    citymap = CityMap("network.json")
    print(citymap.search("1250429", "1121480"))
    #print(citymap.bfs_shortest_path("1250429", "1121480"))

if __name__ == '__main__':
    main()
