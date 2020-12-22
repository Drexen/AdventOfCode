use std::{collections::HashSet, fmt::Debug};

#[derive(Clone)]
struct Tile {
    id: u64,
    data: Vec<Vec<bool>>,
    edges: [Option<Vec<bool>>; 4],
}

enum Edge {
    Top,
    Bottom,
    Left,
    Right,
}

impl Tile {
    pub fn new(id: u64, data: Vec<Vec<bool>>) -> Tile {
        Tile {
            id,
            data,
            edges: [None, None, None, None],
        }
    }

    pub fn cache_edges(&mut self) {
        self.edges[Edge::Top as usize] = Some(self.data[0].clone());
        self.edges[Edge::Bottom as usize] = Some(self.data[self.data.len() - 1].clone());
        self.edges[Edge::Left as usize] = Some(self.data.iter().map(|y| y[0]).collect());
        self.edges[Edge::Right as usize] = Some(self.data.iter().map(|y| y[y.len() - 1]).collect());
    }

    pub fn get_edge(&self, edge: Edge) -> &Vec<bool> {
        match edge {
            Edge::Top => return &self.edges[Edge::Top as usize].as_ref().unwrap(),
            Edge::Bottom => return &self.edges[Edge::Bottom as usize].as_ref().unwrap(),
            Edge::Left => return &self.edges[Edge::Left as usize].as_ref().unwrap(),
            Edge::Right => return &self.edges[Edge::Right as usize].as_ref().unwrap(),
        }
    }
}

impl Debug for Tile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut output = format!("id = {}", self.id);
        self.data.iter().for_each(|l| {
            output += "\n";
            output += l
                .iter()
                .map(|&f| if f { '#' } else { '.' })
                .collect::<String>()
                .as_ref()
        });
        f.write_str(&output)
    }
}

type Board<'a> = Vec<Vec<Option<&'a Tile>>>;

fn main() {
    let tiles: Vec<Tile> = include_str!("day-20-input.txt")
        .split("\r\n\r\n")
        .map(|segment| parse_segment(segment))
        .collect();

    let board_size = (tiles.len() as f32).sqrt() as usize;

    let tile_groups: Vec<Vec<Tile>> = tiles
        .into_iter()
        .map(|t| generate_orientations(t))
        .collect();

    let board: Board = vec![vec![None; board_size]; board_size];
    let used_groups: HashSet<usize> = HashSet::new();
    let pos = (0, 0);

    if let Some(result) = solve_board_step(pos, board, &tile_groups, &used_groups, board_size) {
        let total = result[0][0].as_ref().unwrap().id
            * result[0][board_size - 1].as_ref().unwrap().id
            * result[board_size - 1][0].as_ref().unwrap().id
            * result[board_size - 1][board_size - 1].as_ref().unwrap().id;

        println!("Part one =  {}", total);

        let mut final_image = generate_final_image(result);

        let sea_monster = r"                  # 
#    ##    ##    ###
 #  #  #  #  #  #   ";

        let sea_monster: Vec<Vec<bool>> = sea_monster
            .lines()
            .map(|l| l.chars().map(|c| c == '#').collect())
            .collect();

        let total_waves: usize = final_image
            .iter()
            .map(|row| row.iter().filter(|c| **c).count())
            .sum();

        for _ in 0..4 {
            let water_roughness = calculate_water_roughness(&final_image, &sea_monster);
            if water_roughness != total_waves {
                println!("Part two = {}", water_roughness);
            }

            flip_y_data(&mut final_image);

            let water_roughness = calculate_water_roughness(&final_image, &sea_monster);
            if water_roughness != total_waves {
                println!("Part two = {}", water_roughness);
            }
            flip_y_data(&mut final_image);

            rotate_data(&mut final_image);
        }
    } else {
        unreachable!("No board fit reached")
    }
}

fn calculate_water_roughness(image: &Vec<Vec<bool>>, monster: &Vec<Vec<bool>>) -> usize {
    let monster_size = (monster[0].len(), monster.len());
    let mut working = image.clone();
    for y in 0..image.len() - monster_size.1 + 1 {
        for x in 0..image[y].len() - monster_size.0 + 1 {
            try_fit_monster(image, monster, &mut working, (x, y));
        }
    }
    working
        .iter()
        .map(|row| row.iter().filter(|c| **c).count())
        .sum()
}

fn try_fit_monster(
    image: &Vec<Vec<bool>>,
    monster: &Vec<Vec<bool>>,
    working: &mut Vec<Vec<bool>>,
    pos: (usize, usize),
) {
    for (monster_y, monster_row) in monster.iter().enumerate() {
        for (monster_x, monster_cell) in monster_row.iter().enumerate() {
            let image_pos = (pos.0 + monster_x, pos.1 + monster_y);
            if image_pos.0 == 96 {
                println!("{} {}", pos.0, monster_x);
            }
            if *monster_cell && !image[image_pos.1][image_pos.0] {
                return;
            }
        }
    }

    for (monster_y, monster_row) in monster.iter().enumerate() {
        for (monster_x, monster_cell) in monster_row.iter().enumerate() {
            let image_pos = (pos.0 + monster_x, pos.1 + monster_y);
            if *monster_cell {
                working[image_pos.1][image_pos.0] = false;
            }
        }
    }
}

fn generate_final_image(input: Board) -> Vec<Vec<bool>> {
    let mut output: Vec<Vec<bool>> = vec![vec![false; 96]; 96];

    for (y, row) in input.iter().enumerate() {
        for (x, tile) in row.iter().enumerate() {
            add_tile_to_final_image(&mut output, (x, y), tile.unwrap());
        }
    }
    output
}

fn add_tile_to_final_image(image: &mut Vec<Vec<bool>>, pos: (usize, usize), tile: &Tile) {
    for (y, row) in tile.data.iter().enumerate() {
        if y > 0 && y < tile.data.len() - 1 {
            for (x, cell) in row.iter().enumerate() {
                if x > 0 && x < row.len() - 1 {
                    image[pos.1 * 8 + y - 1][pos.0 * 8 + x - 1] = *cell;
                }
            }
        }
    }
}

fn solve_board_step<'a>(
    pos: (usize, usize),
    board: Board<'a>,
    tile_groups: &'a Vec<Vec<Tile>>,
    used_groups: &HashSet<usize>,
    board_size: usize,
) -> Option<Board<'a>> {
    let possible_tiles = get_possible_tiles(pos, &board, &tile_groups, &used_groups);

    for (i, group) in possible_tiles.iter().enumerate() {
        let mut used_groups_clone = used_groups.clone();
        used_groups_clone.insert(i);

        for tile in group {
            let mut board_clone = board.clone();

            board_clone[pos.1][pos.0] = Some(tile);

            let stepped_pos = step_board_position(pos, board_size);
            if stepped_pos.is_none() {
                return Some(board_clone);
            }

            if let Some(result) = solve_board_step(
                stepped_pos.unwrap(),
                board_clone,
                tile_groups,
                &used_groups_clone,
                board_size,
            ) {
                return Some(result);
            }
        }
    }
    None
}

fn step_board_position(mut pos: (usize, usize), board_size: usize) -> Option<(usize, usize)> {
    pos.0 += 1;
    if pos.0 >= board_size {
        pos.0 %= board_size;
        pos.1 += 1;
        if pos.1 >= board_size {
            return None;
        }
    }
    Some(pos)
}

fn get_possible_tiles<'a>(
    pos: (usize, usize),
    board: &Board,
    tile_groups: &'a Vec<Vec<Tile>>,
    used_groups: &HashSet<usize>,
) -> Vec<Vec<&'a Tile>> {
    //let mut possible_tiles = tile_groups.clone();

    let mut possible_tiles: Vec<Vec<&'a Tile>> = tile_groups
        .iter()
        .map(|group| group.iter().collect())
        .collect();

    for i in used_groups.iter() {
        possible_tiles[*i].clear();
    }

    let mut edge_above: Option<&Vec<bool>> = None;
    if pos.1 as i32 - 1 >= 0 {
        if let Some(tile) = board[pos.1 - 1][pos.0].as_ref() {
            edge_above = Some(tile.get_edge(Edge::Bottom));
        }
    }

    let mut edge_to_left: Option<&Vec<bool>> = None;
    if pos.0 as i32 - 1 >= 0 {
        if let Some(tile) = board[pos.1][pos.0 - 1].as_ref() {
            edge_to_left = Some(tile.get_edge(Edge::Right));
        }
    }

    for group in possible_tiles.iter_mut() {
        let mut i = 0;
        while i < group.len() {
            let tile = &group[i];
            let result = does_tile_fit(tile, edge_above, edge_to_left);
            if !result {
                group.remove(i);
            } else {
                i += 1;
            }
        }
    }

    possible_tiles
}

fn does_tile_fit(
    tile: &Tile,
    edge_above: Option<&Vec<bool>>,
    edge_to_left: Option<&Vec<bool>>,
) -> bool {
    if let Some(edge_to_left) = edge_to_left {
        let this_edge_left = tile.get_edge(Edge::Left);
        if *edge_to_left != *this_edge_left {
            return false;
        }
    }

    if let Some(edge_above) = edge_above {
        let this_edge_above = tile.get_edge(Edge::Top);
        if *edge_above != *this_edge_above {
            return false;
        }
    }

    true
}

fn parse_segment(input: &str) -> Tile {
    let mut tile: Tile = Tile::new(0, vec![]);

    for (i, line) in input.lines().enumerate() {
        if i == 0 {
            tile.id = line.get(5..9).unwrap().parse().unwrap();
        } else {
            let line_data: Vec<bool> = line.chars().map(|c| c == '#').collect();
            tile.data.push(line_data);
        }
    }
    tile
}

fn generate_orientations(mut original: Tile) -> Vec<Tile> {
    let mut output: Vec<Tile> = vec![];

    for _ in 0..4 {
        original.cache_edges();
        output.push(original.clone());
        rotate_data(&mut original.data);
    }

    let flipped = output.clone().into_iter().map(|mut tile| {
        flip_y_data(&mut tile.data);
        tile.cache_edges();
        tile
    });
    output.extend(flipped);

    output
}

fn rotate_data(data: &mut Vec<Vec<bool>>) {
    *data = (0..data.len())
        .map(|n| data.iter().map(|m| m[(m.len() - 1) - n]).collect())
        .collect();
}
fn flip_y_data(data: &mut Vec<Vec<bool>>) {
    data.iter_mut().for_each(|v| (v).reverse());
}
