import os

def read_file() -> list:

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
        # Only to get value 0
        self.is_pivot = True if self.value == 0 else False
    
    def __eq__(self, other_data: object) -> bool:
        if isinstance(other_data, Encrypted_data):
            return (other_data.index == self.index) and (other_data.value == self.value)
        else:
            return False
    
    def __repr__(self) -> str:
        return 'index: {0}, value: {1}'.format(self.index, self.value)
    
    def __mul__(self, other: object):
        if isinstance(other, int):
            self.value *= other
            return self
        else:
            raise TypeError("Multiplication only for int")


def get_pivot(encryption: list[Encrypted_data]) -> Encrypted_data:
    """
    Get value 0 position out of the full encrypted list
    """
    for encrypted_data in encryption:
        if encrypted_data.is_pivot:
            return encrypted_data


def mixing(encryption: list[Encrypted_data], part=1) -> list[Encrypted_data]:
    """
    Perform mixing of encrypted data
    Loops the original list and based on the data extracted performs the shifts
    on the decryption list.
    The cyclical shifts will be handled as the modulo of the shift respect to the size
    """
    if part == 2:
        key = 811589153
        encryption = [data * key for data in encryption]
        mixing_cycles = 10
    else:
        mixing_cycles = 1
    
    decryption = encryption.copy()
    len_data = len(encryption)

    for i in range(len_data * mixing_cycles):

        value_search = encryption[i % len_data]
        index_prev = decryption.index(value_search)
        # New index must reduce len size by 1 because insertion occurs 
        # after removing the data at the previous position
        index_new = (index_prev + value_search.value + len_data - 1) % (len_data - 1)
        index_new = len_data if index_new == 0 else index_new

        decryption.remove(value_search)
        decryption.insert(index_new, value_search)
    
    return decryption


def decrypt_mixing(decryption: list[Encrypted_data]) -> int:
    """
    Perform phasing of decryption code in a cyclical way
    Cycle is handled as modulo with respect to the size of the array
    """
    pivot_data = get_pivot(decryption)
    groove_coordinates = 0

    for i in [1000, 2000, 3000]:

        index_0 = decryption.index(pivot_data)
        index_grove = (index_0 + i) % len(decryption)
        groove_coordinates += decryption[index_grove].value
    
    return groove_coordinates


if __name__ == '__main__':
    test = False
    encryption = read_file()

    print('\nPoint 1')
    decryption = mixing(encryption, 1)
    groove_coordinates = decrypt_mixing(decryption)
    print('Grove coordinates: {0}'.format(groove_coordinates))

    print('\nPoint 2')
    decryption = mixing(encryption, 2)
    groove_coordinates = decrypt_mixing(decryption)
    print('Grove coordinates: {0}'.format(groove_coordinates))