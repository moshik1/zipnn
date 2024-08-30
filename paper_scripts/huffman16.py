import heapq
import struct

class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    priority_queue = [Node(symbol, freq) for symbol, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(root, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if root is not None:
        if root.symbol is not None:
            codebook[root.symbol] = prefix
        generate_huffman_codes(root.left, prefix + '0', codebook)
        generate_huffman_codes(root.right, prefix + '1', codebook)
    return codebook

def read_file_and_calculate_frequencies(filename):
    freq_dict = {}
    try:
        with open(filename, 'rb') as file:
            while byte := file.read(2):
                if len(byte) < 2:
                    continue  # Skip the last byte if file size is not even
                symbol = struct.unpack('>H', byte)[0]
                if symbol in freq_dict:
                    freq_dict[symbol] += 1
                else:
                    freq_dict[symbol] = 1
    except IOError:
        print("File could not be opened.")
    return freq_dict

def encode_data(data, codebook):
    encoded_output = []
    for symbol in data:
        encoded_output.append(codebook[symbol])
    return ''.join(encoded_output)

def calculate_compression_ratio(original_size, encoded_size):
    return (original_size * 16) / encoded_size  # original size in bits

def main(filename):
    freq_dict = read_file_and_calculate_frequencies(filename)
    original_size = sum(freq_dict.values())

    huffman_tree_root = build_huffman_tree(freq_dict)
    huffman_codes = generate_huffman_codes(huffman_tree_root)

    # Re-read the file to simulate encoding process
    encoded_data = ''
    try:
        with open(filename, 'rb') as file:
            while byte := file.read(2):
                if len(byte) < 2:
                    continue  # Skip if the size is not even
                symbol = struct.unpack('>H', byte)[0]
                encoded_data += huffman_codes[symbol]
    except IOError:
        print("Error reading file for encoding.")

    encoded_size = len(encoded_data)  # Length of encoded data in bits
    compression_ratio = calculate_compression_ratio(original_size, encoded_size)

    print("Compression Ratio:", compression_ratio)
    print("Huffman Codes (sample):", {k: huffman_codes[k] for k in list(huffman_codes)[:10]})

if __name__ == "__main__":
    main('input_file.bin')

