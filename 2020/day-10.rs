use std::{fs::File, io::BufRead, io::BufReader};

fn main() {
    let f = File::open("src\\day-10-input.txt").unwrap();
    let reader = BufReader::new(f);
    let mut inputs: Vec<i32> = reader
        .lines()
        .map(|l| l.unwrap().parse().unwrap())
        .collect();

    inputs.push(0);
    inputs.sort();

    part_one(&inputs);
    part_two(&inputs);
}

fn part_one(inputs: &Vec<i32>) {
    let one_diffs = inputs.windows(2).filter(|w| (w[1] - w[0]) == 1).count();
    let three_diffs = inputs.windows(2).filter(|w| (w[1] - w[0]) == 3).count() + 1;

    let answer = one_diffs * three_diffs;
    println!("Part one = {}", answer);
}

fn part_two(inputs: &Vec<i32>) {
    let mut routes = vec![1];
    for (i, value) in inputs.iter().enumerate().skip(1) {
        let mut new_routes: i64 = 0;
        for x in i as i32 - 3..i as i32 {
            if x >= 0 {
                let diff = value - inputs[x as usize];
                if diff <= 3 {
                    new_routes = new_routes + routes[x as usize];
                }
            }
        }
        routes.push(new_routes);
    }

    println!("Part two = {}", routes.last().unwrap());
}
