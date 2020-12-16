use std::collections::HashMap;

fn main() {
    part_one();
    part_two();
}

fn part_one() {
    let mut registers: HashMap<u64, u64> = HashMap::new();
    let mut or_mask: u64 = 0;
    let mut and_mask: u64 = 0;

    for l in include_str!("day-14-input.txt").lines() {
        if let Some(mask) = l.strip_prefix("mask = ") {
            or_mask = u64::from_str_radix(&mask.replace("X", "0"), 2).unwrap();
            and_mask = u64::from_str_radix(&mask.replace("X", "1"), 2).unwrap();
        } else {
            let mut split = l.split(" = ");
            let address: String = split.next().unwrap().chars().skip(4).collect();
            let address: u64 = address.strip_suffix("]").unwrap().parse().unwrap();
            let mut value: u64 = split.next().unwrap().parse().unwrap();

            value |= or_mask;
            value &= and_mask;

            registers.insert(address, value);
        }
    }

    let sum: u64 = registers.values().sum();
    println!("Part one = {}", sum);
}

fn part_two() {
    let mut registers: HashMap<u64, u64> = HashMap::new();
    let mut or_mask: u64 = 0;
    let mut fluc_mask: u64 = 0;

    for l in include_str!("day-14-input.txt").lines() {
        if let Some(mask) = l.strip_prefix("mask = ") {
            or_mask = u64::from_str_radix(&mask.replace("X", "0"), 2).unwrap();
            fluc_mask = u64::from_str_radix(&mask.replace("1", "0").replace("X", "1"), 2).unwrap();
        } else {
            let mut split = l.split(" = ");
            let address: String = split.next().unwrap().chars().skip(4).collect();
            let mut address: u64 = address.strip_suffix("]").unwrap().parse().unwrap();
            address |= or_mask;
            let value: u64 = split.next().unwrap().parse().unwrap();

            let addresses = get_addresses(address, fluc_mask);
            for a in addresses {
                registers.insert(a, value);
            }
        }
    }

    let sum: u64 = registers.values().sum();
    println!("Part two = {}", sum);
}

fn get_addresses(target: u64, mut mask: u64) -> Vec<u64> {
    for i in 0..36 {
        if mask & (1 << i) > 0 {
            let a = target | (1 << i);
            let b = target & (std::u64::MAX - (1 << i));
            mask = mask & (std::u64::MAX - (1 << i));

            let mut r = get_addresses(a, mask);
            r.extend(get_addresses(b, mask));

            return r;
        }
    }
    vec![target]
}
