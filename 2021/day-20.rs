use std::collections::HashSet;

fn main() {
    let mut lines = include_str!("day-20-input.txt").lines();

    let algorithm: Vec<bool> = lines.next().unwrap().chars().map(|c| c == '#').collect();

    let mut points_original: HashSet<(i32, i32)> = HashSet::new();
    for (y, l) in lines.skip(1).enumerate() {
        for (x, c) in l.chars().enumerate() {
            if c == '#' {
                points_original.insert((x as i32, y as i32));
            }
        }
    }

    let mut fallback_state = false;
    let mut points = points_original.clone();
    for _ in 0..2 {
        points = enhance(&points, &algorithm, &mut fallback_state);
    }
    println!("Part one = {}", points.len());

    let mut fallback_state = false;
    let mut points = points_original.clone();
    for _ in 0..50 {
        points = enhance(&points, &algorithm, &mut fallback_state);
    }
    println!("Part two = {}", points.len());
}

pub fn enhance(
    points: &HashSet<(i32, i32)>,
    algorithm: &Vec<bool>,
    fallback_state: &mut bool,
) -> HashSet<(i32, i32)> {
    let mut new_points = HashSet::new();
    let bounds = get_bounds(&points);
    let (xmin, xmax, ymin, ymax) = bounds;
    for x in xmin - 1..xmax + 2 {
        for y in ymin - 1..ymax + 2 {
            let output_pixel =
                calculate_output_pixel(x, y, points, algorithm, bounds, *fallback_state);
            if output_pixel == true {
                new_points.insert((x as i32, y as i32));
            }
        }
    }
    *fallback_state = !*fallback_state;
    new_points
}

pub fn calculate_output_pixel(
    o_x: i32,
    o_y: i32,
    points: &HashSet<(i32, i32)>,
    algorithm: &Vec<bool>,
    bounds: (i32, i32, i32, i32),
    fallback_state: bool,
) -> bool {
    let mut a = vec![];
    for y in o_y - 1..o_y + 2 {
        for x in o_x - 1..o_x + 2 {
            let in_bounds = is_in_bounds(x, y, bounds);
            a.push(points.contains(&(x, y)) || (!in_bounds && fallback_state));
        }
    }

    let index = calculate_index(&a);
    algorithm[index]
}

pub fn is_in_bounds(x: i32, y: i32, bounds: (i32, i32, i32, i32)) -> bool {
    let (xmin, xmax, ymin, ymax) = bounds;
    x >= xmin && x <= xmax && y >= ymin && y <= ymax
}

pub fn calculate_index(data: &Vec<bool>) -> usize {
    let mut output = 0;
    for (i, d) in data.iter().rev().enumerate() {
        if *d == true {
            output += 1 << i;
        }
    }
    output
}

pub fn get_bounds(points: &HashSet<(i32, i32)>) -> (i32, i32, i32, i32) {
    let mut xmin = i32::MAX;
    let mut xmax = i32::MIN;
    let mut ymin = i32::MAX;
    let mut ymax = i32::MIN;

    for p in points {
        xmin = i32::min(p.0, xmin);
        xmax = i32::max(p.0, xmax);
        ymin = i32::min(p.1, ymin);
        ymax = i32::max(p.1, ymax);
    }
    (xmin, xmax, ymin, ymax)
}
