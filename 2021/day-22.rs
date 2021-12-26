use regex::Regex;

#[derive(Debug)]
pub struct Instruction {
    pub state: bool,
    pub x: (i32, i32),
    pub y: (i32, i32),
    pub z: (i32, i32),
}

impl Instruction {
    pub fn new(input: &str) -> Self {
        let re = Regex::new(r"([onf]+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
            .unwrap();
        let captures = re.captures(input).unwrap();

        let state = {
            match &captures[1] {
                "on" => true,
                "off" => false,
                _ => panic!(),
            }
        };

        let xmin = i32::from_str_radix(&captures[2], 10).unwrap();
        let xmax = i32::from_str_radix(&captures[3], 10).unwrap() + 1;
        let ymin = i32::from_str_radix(&captures[4], 10).unwrap();
        let ymax = i32::from_str_radix(&captures[5], 10).unwrap() + 1;
        let zmin = i32::from_str_radix(&captures[6], 10).unwrap();
        let zmax = i32::from_str_radix(&captures[7], 10).unwrap() + 1;

        Instruction {
            state,
            x: (xmin, xmax),
            y: (ymin, ymax),
            z: (zmin, zmax),
        }
    }
}

fn main() {
    let lines = include_str!("day-22-input.txt").lines();
    let instructions: Vec<Instruction> = lines.map(|l| Instruction::new(l)).collect();

    println!(
        "Part one = {}",
        run(&instructions, |i| i.x.0 >= -50
            && i.x.1 <= 50
            && i.y.0 >= -50
            && i.y.1 <= 50
            && i.z.0 >= -50
            && i.z.1 <= 50)
    );
    println!("Part two = {}", run(&instructions, |_| true));
}

pub fn run(
    instructions: &Vec<Instruction>,
    instruction_filter: impl Fn(&Instruction) -> bool,
) -> u64 {
    let mut xslices: Vec<i32> = instructions
        .iter()
        .flat_map(|i| vec![i.x.0, i.x.1])
        .collect();
    xslices.sort();
    xslices.dedup();

    let mut yslices: Vec<i32> = instructions
        .iter()
        .flat_map(|i| vec![i.y.0, i.y.1])
        .collect();
    yslices.sort();
    yslices.dedup();

    let mut zslices: Vec<i32> = instructions
        .iter()
        .flat_map(|i| vec![i.z.0, i.z.1])
        .collect();
    zslices.sort();
    zslices.dedup();

    let mut data = vec![vec![vec![false; xslices.len()]; yslices.len()]; zslices.len()];

    for instruction in instructions {
        if instruction_filter(instruction) == false {
            continue;
        }

        let xi0 = xslices.iter().position(|i| instruction.x.0 == *i).unwrap();
        let xi1 = xslices.iter().position(|i| instruction.x.1 == *i).unwrap();
        let yi0 = yslices.iter().position(|i| instruction.y.0 == *i).unwrap();
        let yi1 = yslices.iter().position(|i| instruction.y.1 == *i).unwrap();
        let zi0 = zslices.iter().position(|i| instruction.z.0 == *i).unwrap();
        let zi1 = zslices.iter().position(|i| instruction.z.1 == *i).unwrap();

        for z in zi0..zi1 {
            for y in yi0..yi1 {
                for x in xi0..xi1 {
                    data[z][y][x] = instruction.state;
                }
            }
        }
    }

    let mut count: u64 = 0;
    for z in 0..zslices.len() - 1 {
        for y in 0..yslices.len() - 1 {
            for x in 0..xslices.len() - 1 {
                let xvr = (xslices[x + 1] - xslices[x]) as u64;
                let yvr = (yslices[y + 1] - yslices[y]) as u64;
                let zvr = (zslices[z + 1] - zslices[z]) as u64;
                if data[z][y][x] {
                    let num_cells = (xvr + 0) * (yvr + 0) * (zvr + 0);
                    count += num_cells;
                }
            }
        }
    }
    count
}
