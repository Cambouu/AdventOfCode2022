import os

def read_file():

    file_day = os.path.splitext(os.path.basename(__file__))[0]
    file_ext = '_test' if test else ''

    with open(os.path.join('.', 'aoc', '{0}{1}.txt'.format(file_day, file_ext)), 'r') as f:
        encryption = [Encrypted_data(i, x) for i, x in enumerate(f.readlines())]

    return encryption


class Encrypted_data():

    def __init__(self, index: int, value: str) -> None:
        # Index is necessary because there exist repeated values in list
        self.index = index
        self.value = int(value)
        self.pivot = True if self.value == 0 else False
    
    def __eq__(self, other_data: object) -> bool:
        if isinstance(other_data, Encrypted_data):
            return (other_data.index == self.index) and (other_data.value == self.value)
        else:
            return False
    
    def __repr__(self) -> str:
        return 'index: {0}, value: {1}'.format(self.index, self.value)


def get_pivot(encryption: list[Encrypted_data]) -> Encrypted_data:
    for encrypted_data in encryption:
        if encrypted_data.pivot:
            return encrypted_data


def mixing(encryption: list[Encrypted_data]) -> list[Encrypted_data]:

    decryption = encryption.copy()
    len_data = len(encryption)

    for i in range(len_data):

        value_search = encryption[i % len_data]
        index_prev = decryption.index(value_search)
        index_new = (index_prev + value_search.value + len_data - 1) % (len_data - 1)
        index_new = len_data if index_new == 0 else index_new

        decryption.remove(value_search)
        decryption.insert(index_new, value_search)
    
    return decryption


def decrypt_mixing(decryption: list[Encrypted_data]) -> int:
    pivot_data = get_pivot(decryption)
    groove_coordinates = 0
    key = 811589153

    for i in [1000, 2000, 3000]:

        index_0 = decryption.index(pivot_data)
        index_grove = (index_0 + i) % len(decryption)
        groove_coordinates += decryption[index_grove].value
    
    return groove_coordinates


if __name__ == '__main__':
    test = False
    encryption = read_file()
    decryption = mixing(encryption)
    groove_coordinates = decrypt_mixing(decryption)

    # print('\nPoint 1')
    print('Grove coordinates: {0}'.format(groove_coordinates))

    # print('\nPoint 2')