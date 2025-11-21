import hashlib # sert à créer des hachages SHA-256
import datetime # sert à récupérer la date et l’heure d’un bloc


# Classe Block

class Block:
    def __init__(self, index, data, prev_hash, difficulty):
        self.index = index #numéro du bloc dans la chaîne
        self.timestamp = str(datetime.datetime.now()) #enregistre la date et l’heure
        self.data = data #les données du bloc
        self.prev_hash = prev_hash
        self.nonce = 0 #compteur utilisé pour la preuve de travail
        self.difficulty = difficulty #nombre de zéros exigés
        self.hash = self.mine_block() #lance le minage pour trouver un hash valide

    # Fonction pour recalculer le hash
    def calc_hash(self):
        sha = hashlib.sha256()
        to_hash = (str(self.index) +
                   self.timestamp +
                   self.data +
                   self.prev_hash +
                   str(self.nonce)).encode('utf-8') #transforme tout en bytes
        sha.update(to_hash) #calcul du hash
        return sha.hexdigest() #résultat en chaîne hexadécimale (64 caractères)

    # Preuve de travail
    def mine_block(self):
        prefix = "0" * self.difficulty #Si difficulty = 1, alors prefix = "0" Si difficulty = 3, alors prefix = "000"
        hash_value = self.calc_hash() #calcule un hash

        while not hash_value.startswith(prefix):#Tant que le hash ne commence pas par le nombre de zéros demandé
            self.nonce += 1 #augmenter le nonce
            hash_value = self.calc_hash() #recalculer le hash

        return hash_value #Quand un hash valide est trouvé → on retourne le hash.


# Classe Blockchain

class Blockchain: #Elle représente toute la chaîne.
    def __init__(self, difficulty=1):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    # Créer le bloc de genèse
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0", 1) #Bloc numéro 0, avec données "Genesis Block" Hash précédent = "0" Difficulté = 1

    # Ajouter un bloc
    def add_block(self, data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), data, prev_block.hash, self.difficulty)
        self.chain.append(new_block) #ajoute le bloc à la liste.

    # Vérifier la validité de la blockchain
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # vérifier le hash
            if current.hash != current.calc_hash(): #Si le hash stocké ≠ hash recalculé → chaîne corrompue
                return False

            # vérifier le previous_hash
            if current.prev_hash != previous.hash: #Si le previous_hash ne correspond pas → falsification
                return False

            # vérifier la difficulté
            if not current.hash.startswith("0" * self.difficulty): #Si le hash ne respecte pas la difficulté → bloc invalide
                return False

        return True



# Test du programme

blockchain = Blockchain(difficulty=1)  # tu peux mettre difficulté=2 ou 3

blockchain.add_block("Premier bloc")
blockchain.add_block("Deuxième bloc")

# Affichage
for block in blockchain.chain:
    print("Index :", block.index)
    print("Hash :", block.hash)
    print("Prev :", block.prev_hash)
    print("Nonce :", block.nonce)
    print("-" * 50)

print("Blockchain valide ? ", blockchain.is_chain_valid())
