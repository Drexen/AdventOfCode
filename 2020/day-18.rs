#[derive(Debug)]
enum Node {
    Value(u64),
    Expression(Vec<Node>, Vec<Operation>),
}

#[derive(Debug)]
enum Operation {
    Add,
    Multiply,
}

fn main() {
    let lines = include_str!("day-18-input.txt").replace(" ", "");

    let nodes: Vec<Node> = lines.lines().map(|l| parse_line(l)).collect();

    let total: u64 = nodes.iter().map(|n| process_part_one(&n)).sum();
    println!("Part one = {}", total);

    let total: u64 = nodes.iter().map(|n| process_part_two(&n)).sum();
    println!("Part two = {}", total);
}

fn process_part_one(node: &Node) -> u64 {
    return match node {
        Node::Value(value) => *value,
        Node::Expression(nodes, ops) => {
            let values: Vec<u64> = nodes.iter().map(|n| process_part_one(n)).collect();
            let mut total = values[0];
            for (i, op) in ops.iter().enumerate() {
                match op {
                    Operation::Add => total += values[i + 1],
                    Operation::Multiply => total *= values[i + 1],
                }
            }
            total
        }
    };
}

fn process_part_two(node: &Node) -> u64 {
    return match node {
        Node::Value(value) => *value,
        Node::Expression(nodes, ops) => {
            let mut values: Vec<u64> = nodes.iter().map(|n| process_part_two(n)).collect();
            for (i, op) in ops.iter().enumerate() {
                match op {
                    Operation::Add => {
                        let sum = values[i] + values[i + 1];
                        values[i] = 1;
                        values[i + 1] = sum;
                    }
                    _ => (),
                }
            }
            values.iter().product()
        }
    };
}

fn parse_line(mut line: &str) -> Node {
    let mut nodes: Vec<Node> = vec![];
    let mut operations: Vec<Operation> = vec![];
    while !line.is_empty() {
        let (node, line_sub) = get_next_node(line);
        nodes.push(node);

        let _char = line_sub.chars().next();
        let op: Operation = match _char {
            Some('+') => Operation::Add,
            Some('*') => Operation::Multiply,
            _ => return Node::Expression(nodes, operations),
        };

        operations.push(op);
        line = line_sub.get(1..line_sub.len()).unwrap();
    }
    todo!()
}

fn get_next_node(line: &str) -> (Node, &str) {
    let _char = line.chars().next().unwrap();
    if let Some(digit) = _char.to_digit(10) {
        return (Node::Value(digit as u64), line.get(1..line.len()).unwrap());
    } else if _char == '(' {
        let line_sub = get_enclosed_substring(line);
        let remaining = line.get(line_sub.len() + 2..line.len()).unwrap();
        return (parse_line(line_sub), remaining);
    }
    panic!();
}

fn get_enclosed_substring(line: &str) -> &str {
    let mut parenth_count = 1;
    for (i, _char) in line.chars().enumerate().skip(1) {
        if _char == '(' {
            parenth_count += 1;
        } else if _char == ')' {
            parenth_count -= 1;
        }

        if parenth_count == 0 {
            return line.get(1..i).unwrap();
        }
    }
    panic!();
}
