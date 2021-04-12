import csv
import sys

from util import Node, StackFrontier, QueueFrontier, ExploredSet

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"../data/{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"../data/{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"../data/{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    initialState = person_id_for_name(input("Name: "))
    if initialState is None:
        sys.exit("Person not found.")

    finalState = person_id_for_name(input("Name: "))

    if finalState is None:
        sys.exit("Person not found.")

    path = shortest_path(initialState, finalState)

    if path is None:
        print("Not connected.")

    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, initialState)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

# My implementation was the function below:

def shortest_path(initialState, finalState):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    node = Node(state = initialState, parent = None, action = None)

    frontier = QueueFrontier()
    frontier.add(node)
    exploredSet = ExploredSet()

    while True:

        if len(frontier.frontier) == 0:
            return []        

        node = frontier.frontier[0]

        """ DEBUG
        person = people[node.state]["name"]
        print("\n---------------------------")
        print(f"Current evaluated node: {person}")
        """

        if node.state == finalState:

            #DEBUG print("\nConnected!\n")
            
            path = []

            while node.parent != None:
                path = [(node.action, node.state)] + path
                node = node.parent

            return path

        neighborhood = neighbors_for_person(node.state)
        parentNode = node
        parentStateName = people[parentNode.state]["name"]

        """ DEBUG
        print("\n\tNEIGHBORHOOOD:\n")
        print("Parent Node: ", end="")
        print(people[node.state]["name"])
        """

        for neighbor in neighborhood:
            
            node = Node(state = neighbor[1], parent = parentNode, action = neighbor[0])
            
            if not exploredSet.contains_state(node.state) and not frontier.contains_state(node.state):
                
                frontier.add(node)
                    
                stateName = people[node.state]["name"]
                #DEBUG print(f"{stateName} is a neighbor of {parentStateName}")
                
            
        if not exploredSet.contains_state(parentNode.state):
            
            exploredSet.add(parentNode)
        
        frontier.remove()


        """ DEBUG
        print("\n\tFRONTIER: \n")

        for j in frontier.frontier:
            print(people[j.state]["name"])
        print("\n")

        print("\tEXPLORED SET:\n")

        for i in exploredSet.set:
            print(people[i.state]["name"])
        print("\n")

        if input("Press \"n\" to continue: ") != 'n':
            return []
        """     



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
