use std::{collections::HashSet, str::Lines};

#[derive(Debug)]
enum Direction {
    East,
    SouthEast,
    SouthWest,
    West,
    NorthWest,
    NorthEast,
}

fn main() {
    let lines = include_str!("day-24-input.txt").lines();
    let directions = parse_input(lines);
    let mut board = generate_board(&directions);
    println!("Part one = {}", board.len());

    for _ in 0..100 {
        step_board(&mut board);
    }

    println!("Part two = {}", board.len());
}

fn step_board(board: &mut HashSet<(i32, i32)>) {
    let board_pristine = board.clone();

    let bbx_min = board.iter().min_by_key(|(x, _)| x).unwrap().0;
    let bbx_max = board.iter().max_by_key(|(x, _)| x).unwrap().0;
    let bby_min = board.iter().min_by_key(|(_, y)| y).unwrap().1;
    let bby_max = board.iter().max_by_key(|(_, y)| y).unwrap().1;

    for y in bby_min - 1..bby_max + 2 {
        for x in bbx_min - 1..bbx_max + 2 {
            let pos = (x, y);
            let adjacent_positions = get_adjacent_positions(&pos);

            let num_adjacent = adjacent_positions
                .iter()
                .filter(|p| board_pristine.contains(p))
                .count();

            if board_pristine.contains(&pos) {
                // tile is black
                if num_adjacent == 0 || num_adjacent > 2 {
                    board.remove(&pos);
                }
            } else {
                // tile is white
                if num_adjacent == 2 {
                    board.insert(pos);
                }
            }
        }
    }
}

fn get_adjacent_positions(pos: &(i32, i32)) -> Vec<(i32, i32)> {
    [(-1, 1), (0, 1), (-1, 0), (1, 0), (0, -1), (1, -1)]
        .iter()
        .map(|p| (p.0 + pos.0, p.1 + pos.1))
        .collect()
}

fn parse_input(lines: Lines) -> Vec<Vec<Direction>> {
    let mut directions: Vec<Vec<Direction>> = vec![];
    for line in lines {
        let mut direction_list: Vec<Direction> = vec![];
        let mut previous: Option<char> = None;
        for ch in line.chars() {
            match previous {
                Some('s') => {
                    if ch == 'e' {
                        direction_list.push(Direction::SouthEast);
                    } else if ch == 'w' {
                        direction_list.push(Direction::SouthWest);
                    }
                }
                Some('n') => {
                    if ch == 'e' {
                        direction_list.push(Direction::NorthEast);
                    } else if ch == 'w' {
                        direction_list.push(Direction::NorthWest);
                    }
                }
                Some(_) => panic!(),
                None => (),
            }

            if previous.is_some() {
                previous = None;
            } else {
                if ch == 'e' {
                    direction_list.push(Direction::East);
                } else if ch == 'w' {
                    direction_list.push(Direction::West);
                } else if ch == 's' || ch == 'n' {
                    previous = Some(ch);
                } else {
                    panic!()
                }
            }
        }
        assert!(direction_list.len() > 0);
        directions.push(direction_list);
    }
    directions
}

fn generate_board(directions: &Vec<Vec<Direction>>) -> HashSet<(i32, i32)> {
    let mut board = HashSet::new();
    for directions_list in directions {
        let mut pos = (0, 0);
        for direction in directions_list {
            match direction {
                Direction::East => pos.0 += 1,
                Direction::SouthEast => pos = (pos.0 + 1, pos.1 - 1),
                Direction::SouthWest => pos.1 -= 1,
                Direction::West => pos.0 -= 1,
                Direction::NorthWest => pos = (pos.0 - 1, pos.1 + 1),
                Direction::NorthEast => pos.1 += 1,
            }
        }

        if board.contains(&pos) {
            board.remove(&pos);
        } else {
            board.insert(pos);
        }
    }
    board
}
