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
    # O diretório acessado para obter os dados depende do argumento dado na CLI
    # No caso de omissão, ele acessa diretamento o diretório large/. Caso queiramos
    # Acessar os dados de small/ devemos especificar através do argv.
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    # Entrada do ator inicial (Estado inicial).
    initialState = person_id_for_name(input("Name: "))
    if initialState is None:
        sys.exit("Person not found.")
    # Entrada do ator final (Estado final).
    finalState = person_id_for_name(input("Name: "))
    if finalState is None:
        sys.exit("Person not found.")

    # Função que vou implementar com o algoritmo BFS.
    # Ela tem que receber uma lista de nós
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


# Chamar por frontier retorna um objeto da classe QueueFrontier.
# Chamar por frontier.frontier retorna uma lista contendo os nós na fronteira.


def shortest_path(initialState, finalState):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Resposta: Tenho que trabalhar dentro da função path com nós, pois os métodos
    # da fronteira tratam nós. Preciso dos nós também por que eles contém a informação
    # do próprio pai, que usarei depois para rastrear o caminho de volta para o inicio,
    # criando a estrutura de dados path.

    node = Node(state = initialState, parent = None, action = None)

    frontier = QueueFrontier()
    frontier.add(node)
    exploredSet = ExploredSet()

    while True:

        node = frontier.frontier[0]
        person = people[node.state]["name"]
        print(f"Evaluated Node: {person}")

        if node.state == finalState:
            print("\nConnected!\n")
            
            path = []

            while node.parent != None:
                path = [(node.action, node.state)] + path
                node = node.parent;
            
            print(path)

            return path

        neighborhood = neighbors_for_person(node.state)
        parentNode = node
        parentStateName = people[parentNode.state]["name"]

        print("PARENT NODE:")
        print(people[node.state]["name"])

        for neighbor in neighborhood:
            
            node = Node(state = neighbor[1], parent = parentNode, action = neighbor[0])
            
            if not exploredSet.contains_state(node.state) and not frontier.contains_state(node.state):
                
                frontier.add(node)
                    
                stateName = people[node.state]["name"]
                print(f"{stateName} is a neighbor of {parentStateName}")
                
            
        if not exploredSet.contains_state(parentNode.state):
            
            exploredSet.add(parentNode)
        
        frontier.remove()
        
        print("\n FRONTIER: \n")

        for j in frontier.frontier:
            print(people[j.state]["name"])
        print("\n")

        print("\n EXPLORED SET: \n")

        for i in exploredSet.set:
            print(people[i.state]["name"])
        print("\n")

        if input("Aperta \"a\": ") != 'a':
            return []



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
