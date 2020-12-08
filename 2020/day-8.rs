use std::{collections::HashSet, fs::File, io::BufRead, io::BufReader};

fn main() {
    let f = File::open("src\\day-8-input.txt").unwrap();
    let reader = BufReader::new(f);
    let instructions: Vec<_> = reader
        .lines()
        .map(|l| {
            let l = l.unwrap();
            let mut split = l.split(" ");
            let op_name = split.next().unwrap();
            let value = split.next().unwrap().parse().unwrap();
            let op = match op_name {
                "nop" => Operation::nop(value),
                "acc" => Operation::acc(value),
                "jmp" => Operation::jmp(value),
                _ => panic!(),
            };
            op
        })
        .collect();

    println!("Part one = {}", execute(&instructions).1);
    part_two(&instructions);
}

fn part_two(instructions: &Vec<Operation>) {
    let mut instructions = (*instructions).clone();
    let mut current: usize = 0;
    while current < instructions.len() {
        flip_ops(&mut instructions, current);

        let (result, acc) = execute(&instructions);
        if result {
            println!("Part two = {}", acc);
            break;
        }

        flip_ops(&mut instructions, current);

        current = current + 1;
    }
}

fn flip_ops(instructions: &mut Vec<Operation>, i: usize) {
    match instructions[i] {
        Operation::nop(val) => instructions[i] = Operation::jmp(val),
        Operation::jmp(val) => instructions[i] = Operation::nop(val),
        _ => (),
    }
}

fn execute(instructions: &Vec<Operation>) -> (bool, i32) {
    let mut acc = 0;
    let mut head: i32 = 0;
    let mut executed = HashSet::new();
    let result = loop {
        if head as usize == instructions.len() {
            break true;
        }
        let instruction = &instructions[head as usize];
        if !executed.insert(head) {
            break false;
        }

        match instruction {
            Operation::nop(_) => head = head + 1,
            Operation::acc(val) => {
                head = head + 1;
                acc = acc + val;
            }
            Operation::jmp(val) => head = head + val,
        }
    };

    (result, acc)
}

#[derive(Debug, Clone)]
enum Operation {
    nop(i32),
    acc(i32),
    jmp(i32),
}
