import sys

def main():
    filename = sys.argv[1]

    num_list = []
    with open(filename, 'r') as f:
        for line in f:
            num =  line.strip()
            num_list += [int(num)]

    avg = sum(num_list)/len(num_list)
    print(f"Average of numbers in {filename}: {avg}")

if __name__ == '__main__':
    main()
