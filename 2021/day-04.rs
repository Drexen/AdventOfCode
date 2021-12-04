use core::panic;
use std::{
    fs::File,
    io::{BufRead, BufReader},
};

pub fn main() {
    let file = File::open("src\\day-04-input.txt").unwrap();
    let mut lines = BufReader::new(file).lines();

    let bla = lines.next().unwrap().unwrap();
    let call_list: Vec<i32> = bla.split(",").map(|s| s.parse().unwrap()).collect();

    let mut boards: Vec<Vec<Vec<i32>>> = vec![];

    let mut board: Vec<Vec<i32>> = vec![];
    for line in lines.skip(1) {
        let actual_line = line.unwrap();
        if actual_line.len() == 0 {
            boards.push(board.clone());
            board = vec![];
            continue;
        }
        let board_line = actual_line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        board.push(board_line);
    }

    part_one(call_list.clone(), boards.clone());
    part_two(call_list.clone(), boards.clone());
}

pub fn bingo_matches(board: &Vec<Vec<i32>>) -> bool {
    let horizontal = board.iter().any(|x| x.iter().all(|n| *n == -1));
    let vertical = (0..board.len()).any(|x| board.iter().all(|l| l[x] == -1));
    horizontal || vertical
}

pub fn part_one(call_list: Vec<i32>, mut boards: Vec<Vec<Vec<i32>>>) {
    for called_number in call_list {
        for board in &mut boards {
            check_number_on_board(board, called_number);
            if bingo_matches(board) {
                let sum: i32 = board.iter().flatten().filter(|n| **n != -1).sum();
                let result = called_number * sum;
                println!("Part one = {}", result);
                return;
            }
        }
    }
    panic!()
}

pub fn check_number_on_board(board: &mut Vec<Vec<i32>>, called_number: i32) {
    for line in board.iter_mut() {
        for number in line {
            if *number == called_number {
                *number = -1;
            }
        }
    }
}

pub fn part_two(call_list: Vec<i32>, mut boards: Vec<Vec<Vec<i32>>>) {
    for called_number in call_list {
        let mut boards_to_remove: Vec<usize> = vec![];
        for (board_index, board) in boards.iter_mut().enumerate() {
            for line in board.iter_mut() {
                for number in line {
                    if *number == called_number {
                        *number = -1;
                    }
                }
            }

            if bingo_matches(board) {
                boards_to_remove.push(board_index);
            }
        }

        if boards.len() == 1 && boards_to_remove.len() == 1 {
            let sum: i32 = boards[0].iter().flatten().filter(|n| **n != -1).sum();
            let result = called_number * sum;
            println!("Part two = {}", result);
            return;
        }

        for board_to_remove in boards_to_remove.iter().rev() {
            boards.remove(*board_to_remove);
        }
    }
}
