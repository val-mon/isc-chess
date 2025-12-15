#RNBKQBNR/8/3PPPPP/PPP5/6pp/pppppp2/8/rnbkqbnr w - - 0 1
# to
# [['rb' 'nb' 'bb' 'qb' 'kb' 'bb' 'nb' 'rb']
# ['' '' '' '' '' '' '' '']
# ['pb' 'pb' 'pb' 'pb' 'pb' 'pb' 'pb' 'pb']
# ['' '' '' '' '' '' '' '']
# ['' '' '' '' '' '' 'pw' 'pw']
# ['pw' 'pw' 'pw' 'pw' 'pw' 'pw' '' '']
# ['' '' '' '' '' '' '' '']
# ['rw' 'nw' 'bw' 'qw' 'kw' 'bw' 'nw' 'rw']]
import sys

from numpy._core.strings import isnumeric

def main():
    if len(sys.argv) < 2:
        print("must give FEN argument")
        return
    
    arg = sys.argv[1]
    
    splitted = arg.split(' ')[0].split('/')
    final_array = []
    
    for line in splitted:
        final_array.append([])
        for char in list(line):
            if isnumeric(char):
                for i in range(int(char)):
                    final_array[-1].append('')
            else:
                color = "w" if char.lower() != char else "b"
                final_array[-1].append(char.lower() + color)
    
    print(final_array)

if __name__ == '__main__':
    main()
