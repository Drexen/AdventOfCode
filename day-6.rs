use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn main() -> () {
    let f = File::open("src\\day-6-input.txt").unwrap();
    let f = BufReader::new(f);

    let mut input_vec = Vec::new();

    for line in f.lines() {
        let s = line.unwrap();
        input_vec.push(s.clone());
    }

    let split: Vec<Vec<_>> = input_vec.iter().map(|x| x.split(')').collect()).collect();
    let mut nodes: Vec<_> = split.iter().flat_map(|x| x.clone()).collect();
    nodes.sort();
    nodes.dedup();

    let nodes_and_parents: Vec<_> = nodes
        .iter()
        .map(|x| {
            for split_entry in split.iter() {
                if split_entry[1] == *x {
                    let parent_idx = nodes.iter().position(|y| *y == split_entry[0]).unwrap();
                    return (String::from(*x), Some(parent_idx));
                }
            }
            (String::from(*x), None)
        })
        .collect();

    {
        let mut steps = 0;
        for entry in nodes_and_parents.iter() {
            let mut current_node = entry;
            while current_node.1 != None {
                steps += 1;
                current_node = &nodes_and_parents[current_node.1.unwrap()];
            }
        }
        println!("{:?}", steps);
    }

    {
        let you_path = get_path(&nodes_and_parents, "YOU");
        let san_path = get_path(&nodes_and_parents, "SAN");

        let mut result = 0;
        for (i, item_you) in you_path.iter().enumerate() {
            for (j, item_san) in san_path.iter().enumerate() {
                if item_you == item_san {
                    result = i + j;
                    break;
                }
            }

            if result != 0 {
                break;
            }
        }

        println!("{:?}", result);
    }
}

fn get_path(
    nodes_and_parents: &Vec<(String, Option<usize>)>,
    start_node: &str,
) -> Vec<(String, Option<usize>)> {
    let mut node = nodes_and_parents
        .iter()
        .find(|x| start_node == x.0)
        .unwrap();
    let mut path = vec![];
    while node.1 != None {
        path.push(nodes_and_parents[node.1.unwrap()].clone());
        node = &nodes_and_parents[node.1.unwrap()];
    }
    path
}
