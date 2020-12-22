from typing import List, Optional, Tuple, Set

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


class Tile:
    def __init__(self, id: int, image: List[str]):
        self.id = id
        self.image = Tile.parse_image(image)

        # table of borders for faster look up
        self.borders = [self.image[0].copy(),
                        [row[-1] for row in self.image],
                        self.image[-1].copy(),
                        [row[0] for row in self.image]]
        self.borders[2].reverse()
        self.borders[3].reverse()

        # table of flipped borders for faster look up
        self.flipped_borders = [self.borders[i].copy() for i in [0, 3, 2, 1]]
        for b in self.flipped_borders:
            b.reverse()

        self.rotation = 0   # rotation
        self.flip = False   # flipped tile (horizontal, aplied before rotating)

    @staticmethod
    def parse_image(image: List[str]) -> List[List[bool]]:
        # convert input matrix of dots and hashes to matrix of bools
        img: List[List[bool]] = []
        for row in image:
            img.append([])
            for char in row:
                img[-1].append(char == '#')
        return img

    def get_border(self, border: int) -> List[bool]:
        # returns border according to current 'flip' and rotation
        index = (border - self.rotation) % 4
        if self.flip:
            return self.flipped_borders[index]
        return self.borders[index]

    def which_border(self, border: List[bool]) -> Optional[Tuple[int, bool]]:
        # looks up, if this tile contains provided border
        # if yes, then returns orientation - 'TOP', 'RIGHT', ...
        # and if the border is flipped
        if border in self.borders:
            return self.borders.index(border), False
        elif border in self.flipped_borders:
            return self.flipped_borders.index(border), True
        return None

    def borders_with(self, where: int, other: 'Tile') \
            -> Optional[Tuple[int, bool]]:
        # if this tiles borders with the other on 'where' side,
        # returns where is the bordering border on the other tile
        # else returns None
        b = self.get_border(where)
        return other.which_border(b)

    def get(self, row: int, col: int) -> bool:
        # returns content at [row, col] after aplying flip and rotation
        if self.flip:
            col = self.size() - col - 1

        if self.rotation == 1:
            row, col = col, row
            if self.flip:
                col = self.size() - col - 1
            else:
                row = self.size() - row - 1
        elif self.rotation == 2:
            col = self.size() - col - 1
            row = self.size() - row - 1
        elif self.rotation == 3:
            row, col = col, row
            if self.flip:
                row = self.size() - row - 1
            else:
                col = self.size() - col - 1

        return self.image[row][col]

    def print(self) -> None:
        for row in range(len(self.image)):
            self.print_row(row,)

    def print_row(self, r: int, end: str = '\n') -> None:
        for col in range(self.size()):
            print('#' if self.get(r, col) else '.', end='')
        print(end, end='')

    def info(self) -> str:
        return f'R:{self.rotation}, F:' + ('T' if self.flip else 'F')

    def size(self) -> int:
        return len(self.image)

    def get_img(self) -> List[str]:
        # returns image without borders in correct orientation
        img = []
        for row in range(1, self.size() - 1):
            img.append('')
            for col in range(1, self.size() - 1):
                img[-1] += '#' if self.get(row, col) else '.'
        return img


class Image:
    def __init__(self, tiles: List[Tile]):
        self.tiles = Image.assemble_tiles(tiles)
        self.img = Image.get_image(self.tiles)

    @staticmethod
    def assemble_tiles(tiles: List[Tile]) -> List[List[Tile]]:
        img = [Image.assemble_tile_line(tiles, tiles.pop())]  # seed line

        # add lines abowe
        neighbour = Image.find_neighbour(img[0][0], TOP, tiles)
        while neighbour is not None:
            tiles.remove(neighbour)
            new_line = Image.assemble_tile_line(tiles, neighbour)
            img.insert(0, new_line)
            neighbour = Image.find_neighbour(img[0][0], TOP, tiles)

        # add lines bellow
        neighbour = Image.find_neighbour(img[-1][0], BOTTOM, tiles)
        while neighbour is not None:
            tiles.remove(neighbour)
            new_line = Image.assemble_tile_line(tiles, neighbour)
            img.append(new_line)
            neighbour = Image.find_neighbour(img[-1][0], BOTTOM, tiles)

        return img

    @staticmethod
    def assemble_tile_line(tiles: List[Tile], seed: Tile) -> List[Tile]:
        line = [seed]  # strat with a seed tile

        # add tiles to the left, until none is found
        neighbour = Image.find_neighbour(line[0], LEFT, tiles)
        while neighbour is not None:
            tiles.remove(neighbour)
            line.insert(0, neighbour)
            neighbour = Image.find_neighbour(line[0], LEFT, tiles)

        # add tiles to the right, until none is found
        neighbour = Image.find_neighbour(line[-1], RIGHT, tiles)
        while neighbour is not None:
            tiles.remove(neighbour)
            line.append(neighbour)
            neighbour = Image.find_neighbour(line[-1], RIGHT, tiles)

        return line

    @staticmethod
    def find_neighbour(tile: Tile, where: int, tiles: List[Tile]) \
            -> Optional[Tile]:
        for t in tiles:
            neigbour = tile.borders_with(where, t)
            if neigbour is not None:
                # set rotation to neighbour
                t.flip = not neigbour[1]
                t.rotation = (neigbour[0] + where - 2) % 4
                return t
        return None

    def print_tiles(self, tile_info: bool = False, tile_id: bool = False) -> None:
        tile_size = self.tiles[0][0].size()

        # for each row of tiles
        for tile_row in self.tiles:
            # print line of tile IDs
            if tile_id:
                for tile in tile_row:
                    print(f'Tile {tile.id}:'.ljust(tile_size), end=' ')
                print()

            # print rotation info of tiles
            if tile_info:
                for tile in tile_row:
                    print(tile.info().ljust(tile_size), end=' ')
                print()

            # print tiles row by row
            for row in range(tile_size):
                for tile in tile_row:
                    tile.print_row(row, end=' ')
                print()
            print()

    @staticmethod
    def get_image(tiles: List[List[Tile]]) -> List[str]:
        img = []
        tile_img_size = tiles[0][0].size() - 2
        for tile_row in tiles:
            tile_imgs = [t.get_img() for t in tile_row]
            for row in range(tile_img_size):
                img.append('')
                for t_img in tile_imgs:
                    img[-1] += t_img[row]
        return img

    def flip(self) -> None:
        for i in range(len(self.img)):
            self.img[i] = self.img[i][::-1]

    def rotate(self) -> None:
        new_img = []
        for col in range(len(self.img)):
            new_img.append('')
            for row in range(len(self.img)):
                new_img[-1] += self.img[row][col]
        new_img.reverse()
        self.img = new_img


class Monster:
    def __init__(self):
        self.img = ['                  # ',
                    '#    ##    ##    ###',
                    ' #  #  #  #  #  #   ']
        self.coords = Monster.get_coords(self.img)

    @staticmethod
    def get_coords(img: List[str]) -> Set[Tuple[int, int]]:
        coords = set()
        for row in range(len(img)):
            for col in range(len(img[row])):
                if img[row][col] == '#':
                    coords.add((row, col))
        return coords

    def find_monsters(self, img: List[str]) -> List[Tuple[int, int]]:
        monsters = []
        for row in range(len(img) - len(self.img)):
            for col in range(len(img) - len(self.img[0])):
                m = True
                for coord in self.coords:
                    if img[row + coord[0]][col + coord[1]] != '#':
                        m = False
                        break
                if m:
                    monsters.append((row, col))
        return monsters

    def water_roughnes(self, img: List[str]) -> Optional[int]:
        monsters = len(self.find_monsters(img))
        if monsters == 0:
            return None
        counter = 0
        for row in img:
            for c in row:
                if c == '#':
                    counter += 1
        counter -= len(self.find_monsters(img)) * len(self.coords)
        return counter


def load_tiles(path: str, tile_size: int) -> List[Tile]:
    tiles = []
    f = open(path)
    lines = f.read().splitlines()
    i = 0
    while i < len(lines):
        tile_id = int(lines[i][5:9])
        tile_image = lines[i + 1: i + tile_size + 1]
        tiles.append(Tile(tile_id, tile_image))
        i += tile_size + 2
    return tiles


def solve(file_path: str, name: str, print_img=False):
    print()
    print(name)
    tiles = load_tiles(file_path, 10)
    img = Image(tiles)
    if print_img:
        img.print_tiles(tile_id=True)
    corner_product = img.tiles[0][0].id * \
        img.tiles[-1][0].id * \
        img.tiles[0][-1].id * \
        img.tiles[-1][-1].id
    print('Corner product:', corner_product)

    monster = Monster()
    water_roughnes = None
    for _ in range(5):
        water_roughnes = monster.water_roughnes(img.img)
        if water_roughnes is not None:
            break
        img.rotate()
    if water_roughnes is None:
        img.flip()
        for _ in range(5):
            water_roughnes = monster.water_roughnes(img.img)
            if water_roughnes is not None:
                break
            img.rotate()
    print('Water roughnes:', water_roughnes)


if __name__ == '__main__':
    solve('20/test_input.txt', 'Test')
    solve('20/input.txt', 'Task')
