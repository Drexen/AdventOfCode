#[derive(Debug)]
enum Instruction {
    Inp(usize),
    Add(usize, ValueType),
    Mul(usize, ValueType),
    Div(usize, ValueType),
    Mod(usize, i64),
    Eql(usize, ValueType),
}

impl Instruction {
    pub fn parse(input: &str) -> Instruction {
        let mut split = input.split(" ");
        let instruction_type = split.next().unwrap();
        let left_register = to_register(split.next().unwrap());
        let right = split.next();

        match instruction_type {
            "inp" => Instruction::Inp(left_register),
            "add" => Instruction::Add(left_register, ValueType::parse(right.unwrap())),
            "mul" => Instruction::Mul(left_register, ValueType::parse(right.unwrap())),
            "div" => Instruction::Div(left_register, ValueType::parse(right.unwrap())),
            "mod" => Instruction::Mod(left_register, right.unwrap().parse::<i64>().unwrap()),
            "eql" => Instruction::Eql(left_register, ValueType::parse(right.unwrap())),
            _ => panic!(),
        }
    }
}

#[derive(Debug)]
enum ValueType {
    Value(i64),
    Register(usize),
}

impl ValueType {
    pub fn parse(input: &str) -> ValueType {
        input
            .parse::<i64>()
            .map(|v| ValueType::Value(v))
            .unwrap_or_else(|_| ValueType::Register(to_register(input)))
    }

    pub fn get_value(&self, registers: &[i64]) -> i64 {
        match self {
            ValueType::Value(v) => *v,
            ValueType::Register(r) => registers[*r],
        }
    }
}

fn to_register(r: &str) -> usize {
    match r {
        "w" => 0,
        "x" => 1,
        "y" => 2,
        "z" => 3,
        _ => panic!(),
    }
}

fn main() {
    let lines = include_str!("day-24-input.txt").lines();
    let mut instructions: Vec<Instruction> = lines.map(|l| Instruction::parse(l)).collect();

    let output = check_model_number_alt(&instructions, 92969593497992);
    println!("{}", output);

    println!("Done");
}

fn is_valid_model_number(model_number: i64) -> bool {
    let model_number = model_number.to_string();
    model_number.chars().any(|c| c == '0') == false
}

fn check_model_number(instructions: &Vec<Instruction>, model_number: i64) -> i64 {
    let model_number_str = model_number.to_string();
    let model_number_input = model_number_str
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i64);
    execute(instructions, model_number, model_number_input)
}

fn check_model_number_alt(instructions: &Vec<Instruction>, model_number: i64) -> i64 {
    let model_number_str = model_number.to_string();
    let model_number_input = model_number_str
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i64);
    execute_alt(instructions, model_number, model_number_input)
}

fn execute(
    instructions: &Vec<Instruction>,
    model_number: i64,
    mut input: impl Iterator<Item = i64>,
) -> i64 {
    let mut registers = [0; 4];
    for instruction in instructions {
        match instruction {
            Instruction::Inp(l) => registers[*l] = input.next().unwrap(),
            Instruction::Add(l, r) => registers[*l] += r.get_value(&registers),
            Instruction::Mul(l, r) => registers[*l] *= r.get_value(&registers),
            Instruction::Div(l, r) => registers[*l] /= r.get_value(&registers),
            Instruction::Mod(l, r) => registers[*l] %= r,
            Instruction::Eql(l, r) => {
                registers[*l] = if registers[*l] == r.get_value(&registers) {
                    1
                } else {
                    0
                }
            }
        }
    }
    registers[3]
}

fn execute_alt(
    instructions: &Vec<Instruction>,
    model_number: i64,
    mut input: impl Iterator<Item = i64>,
) -> i64 {
    let registers = [0; 4];
    let mut z = 0;
    for r in 0..14 {
        let a = match &instructions[r * 18 + 4] {
            Instruction::Div(_, v) => v.get_value(&registers),
            _ => panic!(),
        };
        let b = match &instructions[r * 18 + 5] {
            Instruction::Add(_, v) => v.get_value(&registers),
            _ => panic!(),
        };
        let c = match &instructions[r * 18 + 15] {
            Instruction::Add(_, v) => v.get_value(&registers),
            _ => panic!(),
        };
        z = manual_solve(z, input.next().unwrap(), a, b, c);
    }
    z
}

fn manual_solve(z: i64, i: i64, a: i64, b: i64, c: i64) -> i64 {
    let x = if ((z % 26) + b) == i { 0 } else { 1 };
    if x == 1 {
        let z = z / a * 26;
        let y = i + c;
        return z + y;
    } else {
        assert!(a == 26);
        let z = z / 26;
        return z;
    }
}
