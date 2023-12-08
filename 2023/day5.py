from pathlib import Path
import sys
from utils import read_input_filelines


class MappingRange:

    def __init__(self, destination_start, source_start, length):
        self.destination_start = destination_start
        self.source_start = source_start
        # end of ranges (exclusive)
        self.source_end = source_start + length
        self.destination_end = destination_start + length

    def contains_source(self, source):
        return self.source_start <= source < self.source_end

    def get_destination(self, source):
        from_start = source - self.source_start
        return self.destination_start + from_start
 

class Mapping:

    def __init__(self, name, ranges):
        self.name = name
        self.ranges = sorted(ranges, key=lambda x: x.source_start)

    def source_in_range(self, source):
        for mrange in self.ranges:
            if mrange.contains_source(source):
                return True
        return False
    
    def get_destination(self, source):
        for mrange in self.ranges:
            if mrange.contains_source(source):
                return mrange.get_destination(source)
        return source

def parse_almanac(lines):
    name, seeds = lines[0].split(": ")
    section = [name, [int(seed) for seed in seeds.split()]]
    for line in lines[1:]:
        if line == "":
            yield section
            section = []
        else:
            if line.endswith(":"):
                assert section == []
                section.append(line[:-1])
            else:
                section.append([int(n) for n in line.split()])
    if section:
        yield section


def get_seeds_and_mappings(lines):
    sections = parse_almanac(lines)
    seeds = next(sections)[1]

    mappings = {}
    for name, *ranges in sections:
        mappings[name] = Mapping(name, [MappingRange(*range_vals) for range_vals in ranges])

    return seeds, mappings

def part1(lines):
    seeds, mappings = get_seeds_and_mappings(lines)
    locations = []
    for seed in seeds:
        seed = get_location(mappings, seed)
        locations.append(seed)
    print(min(locations))
    

def get_location(mappings, seed):
    for mapping in mappings.values():
        seed = mapping.get_destination(seed)

    return seed


def get_min_location(mappings, seeds):
    lowest = None
    for i, seed in enumerate(seeds):
        location = get_location(mappings, seed)
        if lowest is None or location < lowest:
            lowest = location
        print(i, location)
    return lowest


def overlaps(seed_range, mapping_range):
    """
    Does this seed range overlap with the mapping range
    seed range is in format [start, end] where end is exclusive
    mapping range has a source_start and source_end where source_end is exclusive

    Example: 
    seeds: 79 14 55 13
    seed_ranges = [[79, 93], [55, 68]] (79 to 92 incl, 55 to 67 incl)

    seed-to-soil map:
    Range(source_start 50, dest start 98, length 2) source end 53
    Range(source_start 52, dest start 50, length 48) source end 100

    source range st 79 end (excl) 93

    range 1: start 50, end 53, doesn't cover source range at all
    range 2: start 52, end 100; does overlap with seed range

            ===============    seed range
    ------------               mapping range overlapping start but not end
                       ------- mapping range overlapping end but not start
                ---------      mapping range within
         --------------------- mapping range covers all

    if m st <= s st then m end must be > s st
    else (mst > s st) mst be before < s end   
    """
    seed_start, seed_end = seed_range
    if mapping_range.source_start <= seed_start:
        return mapping_range.source_end > seed_start
    return mapping_range.source_start < seed_end


def destination_ranges_from_source_range(mapping, source_range):
    split_source_ranges = []

    for mrange in mapping.ranges:
        if overlaps(source_range, mrange):
            if mrange.source_start <= source_range[0]:
                # mapping range overlaps beginning of seed range
                new_source_range = [source_range[0]]
            else:
                # mapping range starts after beginning of seed range
                # ranges are sorted by source start, so any preceding seed range
                # is not covered by this mapping, add it as a split range
                split_source_ranges.append((source_range[0], mrange.source_start))
                # this section starts at the range start
                new_source_range = [mrange.source_start]
            
            if mrange.source_end >= source_range[1]:
                # the range end is on or after the source end; we're done with the
                # entire source range, and this fragment ends with the current source
                # end 
                new_source_range.append(source_range[1])
                # we've exhausted this entire source range
                source_range = []
            else:
                # the range end is before the source end; the current source range
                # ends
                new_source_range.append(mrange.source_end)
                # update the source range for the next iteration (with the next range
                # mapping)
                source_range = (mrange.source_end, source_range[1])

            split_source_ranges.append(tuple(new_source_range))
            if not source_range:
                break

    # if we have some source range remaining, add it to the new ranges
    # This could be the end of the range, if it ends after the end of 
    # all mapping ranges, or it could be the entire range, if it's all 
    # after all ranges
    if source_range:
        split_source_ranges.append(tuple(source_range))

    destination_ranges = []
    for source_range in split_source_ranges:
        dest_start = mapping.get_destination(source_range[0])
        # Since our ends are exclusive, the end destination is the destination
        # for the last one within range, plus 1 NOT the destination for the 
        # out of range end (which could be the start of another mapping range) 
        dest_end = mapping.get_destination(source_range[1] -1) + 1
        destination_ranges.append((dest_start, dest_end))
    return destination_ranges


def part2(lines):
    seeds, mappings = get_seeds_and_mappings(lines)
    
    all_seed_pairs = []
    for i in range(0, len(seeds), 2):
        pair = seeds[i: i+2]
        all_seed_pairs.append((pair[0], pair[0] + pair[1]))

    source_ranges = all_seed_pairs
    for mapping in mappings.values():    
        dest_ranges = sum([
            destination_ranges_from_source_range(mapping, source_range)
            for source_range in source_ranges
        ], [])
        source_ranges = dest_ranges
    print(min(rng[0] for rng in source_ranges))

if __name__ == "__main__":
    part, input = sys.argv[1:]
    day = int(Path(__file__).stem.replace("day", ""))
    lines = read_input_filelines(day, f"{input}.txt")
    if part == "1":
        part1(lines)
    else:
        assert part == "2"
        part2(lines)
