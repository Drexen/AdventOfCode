use nom::{
    branch::alt,
    bytes::complete::{tag, take},
    combinator::map,
    multi::{count, many1},
    sequence::tuple,
    IResult, Needed,
};

#[derive(Debug, Clone)]
pub struct Packet {
    pub packet_version: u64,
    pub packet_type: PacketType,
}

#[derive(Debug, Clone)]
pub enum PacketType {
    LiteralValue(u64),
    Operation(OperationType, Vec<Packet>),
}

#[derive(Debug, Copy, Clone)]
pub enum OperationType {
    Sum,
    Product,
    Minimum,
    Maximum,
    GreaterThan,
    LessThan,
    EqualsTo,
}

fn main() {
    let lines: Vec<_> = include_str!("day-16-input.txt").lines().collect();
    let input: Vec<u8> = lines[0]
        .chars()
        .map(|c| u8::from_str_radix(&c.to_string(), 16).unwrap())
        .map(|c| byte_to_4bits_array(c))
        .flatten()
        .collect();

    let packet = parse_packet(&input).unwrap().1;
    println!(
        "Part one = {}",
        get_total_version_number(&vec![packet.clone()])
    );
    println!("Part two = {}", evaluate(&packet));
}

pub fn get_total_version_number(packets: &Vec<Packet>) -> u64 {
    packets
        .iter()
        .map(|p| match &p.packet_type {
            PacketType::LiteralValue(_) => p.packet_version,
            PacketType::Operation(_, sub_packets) => {
                p.packet_version + get_total_version_number(sub_packets)
            }
        })
        .sum()
}

pub fn evaluate(packet: &Packet) -> u64 {
    match &packet.packet_type {
        PacketType::LiteralValue(value) => *value,
        PacketType::Operation(operation_type, sub_packets) => {
            evaluate_operation(&operation_type, &sub_packets)
        }
    }
}

pub fn evaluate_operation(operation_type: &OperationType, sub_packets: &Vec<Packet>) -> u64 {
    let mut p = sub_packets.iter().map(|p| evaluate(p));
    match operation_type {
        OperationType::Sum => p.sum(),
        OperationType::Product => p.fold(1, |a, b| a * b),
        OperationType::Minimum => p.min().unwrap(),
        OperationType::Maximum => p.max().unwrap(),
        OperationType::GreaterThan => {
            if p.next().unwrap() > p.next().unwrap() {
                1
            } else {
                0
            }
        }
        OperationType::LessThan => {
            if p.next().unwrap() < p.next().unwrap() {
                1
            } else {
                0
            }
        }
        OperationType::EqualsTo => {
            if p.next().unwrap() == p.next().unwrap() {
                1
            } else {
                0
            }
        }
    }
}

pub fn byte_to_4bits_array(b: u8) -> Vec<u8> {
    let mut output: Vec<u8> = vec![];
    for n in 0..4 {
        output.push(if b & (1 << (3 - n)) != 0 { 1 } else { 0 });
    }
    output
}

pub fn parse_packet(input: &[u8]) -> IResult<&[u8], Packet> {
    map(
        tuple((parse_version, alt((parse_literal_value, parse_operation)))),
        |(packet_version, packet_type)| Packet {
            packet_version,
            packet_type,
        },
    )(input)
}

pub fn parse_version(input: &[u8]) -> IResult<&[u8], u64> {
    map(take(3usize), |d| combine(d))(input)
}

pub fn parse_operation(input: &[u8]) -> IResult<&[u8], PacketType> {
    let (input, operation_type) = parse_operation_type(input)?;
    let (input, result) = take(1usize)(input)?;
    if result[0] == 0 {
        let (input, subpackets_len) = map(take(15usize), |d| combine(d))(input)?;
        let (subpackets, input) = input.split_at(subpackets_len as usize);

        (map(many1(parse_packet), |d| {
            PacketType::Operation(operation_type, d)
        })(subpackets))
        .map(|(_, b)| (input, b))
    } else {
        let (input, num_of_subpackets) = map(take(11usize), |d| combine(d))(input)?;
        map(count(parse_packet, num_of_subpackets as usize), |d| {
            PacketType::Operation(operation_type, d)
        })(input)
    }
}

pub fn parse_operation_type(input: &[u8]) -> IResult<&[u8], OperationType> {
    let (input, op_code) = map(take(3usize), |d| combine(d))(input)?;
    Ok((
        input,
        match op_code {
            0 => OperationType::Sum,
            1 => OperationType::Product,
            2 => OperationType::Minimum,
            3 => OperationType::Maximum,
            5 => OperationType::GreaterThan,
            6 => OperationType::LessThan,
            7 => OperationType::EqualsTo,
            _ => return Err(nom::Err::Incomplete(Needed::Unknown)),
        },
    ))
}

pub fn parse_literal_value(input: &[u8]) -> IResult<&[u8], PacketType> {
    let (mut input, _) = tag(&[1, 0, 0])(input)?;
    let mut literal: u64 = 0;
    loop {
        let (new_input, should_exit) = map(take(1usize), |d: &[u8]| d[0] == 0)(input)?;
        let (new_input, a) = map(take(4usize), |d| combine(d))(new_input)?;
        input = new_input;
        literal = (literal << 4) + a;
        if should_exit {
            break;
        }
    }
    Ok((input, PacketType::LiteralValue(literal)))
}

pub fn combine(d: &[u8]) -> u64 {
    let mut output: u64 = 0;
    for i in 0..d.len() {
        output += (d[i] as u64) << (d.len() - i - 1);
    }
    output
}
