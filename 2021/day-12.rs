use std::collections::HashMap;

pub fn main() {
    let lines: Vec<_> = include_str!("day-12-input.txt").lines().collect();
    let mut connections: HashMap<String, Vec<String>> = HashMap::new();
    for line in lines {
        let mut split = line.split("-");
        let left = split.next().unwrap();
        let right = split.next().unwrap();
        connections
            .entry(left.to_owned())
            .or_default()
            .push(right.to_owned());
        connections
            .entry(right.to_owned())
            .or_default()
            .push(left.to_owned());
    }

    let num_paths = step(
        "start".to_owned(),
        &connections,
        vec!["start".to_owned()],
        true,
    );

    println!("Part one = {}", num_paths);

    let num_paths = step(
        "start".to_owned(),
        &connections,
        vec!["start".to_owned()],
        false,
    );

    println!("Part two = {}", num_paths);
}

pub fn step(
    current: String,
    connections: &HashMap<String, Vec<String>>,
    path: Vec<String>,
    visited_small_cave: bool,
) -> u32 {
    connections
        .get(&current)
        .unwrap()
        .iter()
        .filter(|c| {
            path.contains(*c) == false
                || **c == c.to_uppercase()
                || (visited_small_cave == false && *c != "start")
        })
        .map(|c| {
            if c == "end" {
                return 1;
            }
            let mut visited_small_cave = visited_small_cave;
            visited_small_cave |= path.contains(&c) && *c == c.to_lowercase() && c != "start";
            let mut new_path = path.clone();
            new_path.push(c.to_owned());
            step(c.to_owned(), connections, new_path, visited_small_cave)
        })
        .sum()
}
