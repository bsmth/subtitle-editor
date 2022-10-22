# Add some cli arguments
import argparse
parser = argparse.ArgumentParser()
# Usage: python3 main.py -subs_file 'subs/example.srt' -millis 200
parser.add_argument("-subs_file", help="the path to the subtitles file")
parser.add_argument(
    "-millis", help="Number of milliseconds to shift. Can be negative integer")
args = parser.parse_args()


subs_file = args.subs_file
millis = args.millis
# a list to hold all the subtitles
subtitles = []

# data structure to hold a subtitle element


class Subtitle:
    def __init__(self, number, start, end, text):
        self.number = number
        self.start = start
        self.end = end
        self.text = text

# The subtitle contents are either a number, a time, or text


def parse_subs(subs_file):
    subs = []
    text = ''
    for line in subs_file:
        if line.strip().isdigit():
            # this is the subtitle number
            number = int(line.strip())
            continue
        if "-->" in line:
            # this is the time
            start_time, end_time = line.strip().split(" --> ")
            continue
        if line.strip() != "":
            #  if it's not an empty line, it's the subtitle text
            text += line
        if line.strip() == "":
            # if it's an empty line, it's the end of the subtitle
            # so we add it to the list
            subs.append(Subtitle(number, start_time, end_time, text))
            text = ''
            continue
    return subs


# read the file and parse the subtitles
subtitles = parse_subs(subs_file)

# shift a time by a given number of milliseconds


def shift_time(time, millis):
    hours, minutes, seconds = time.split(":")
    seconds, milliseconds = seconds.split(",")
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    millis = int(millis)
    seconds += millis // 1000
    milliseconds += millis % 1000
    if milliseconds >= 1000:
        seconds += 1
        milliseconds -= 1000
    return "{:02d}:{:02d}:{:02d},{:03d}".format(
        int(hours), int(minutes), seconds, milliseconds)


#  shift the subtitles by a given number of milliseconds


def shift_subtitles(millis):
    for subtitle in subtitles:
        subtitle.start = shift_time(subtitle.start, millis)
        subtitle.end = shift_time(subtitle.end, millis)

# print by subtitle number


def print_subtitle(number):
    for subtitle in subtitles:
        if subtitle.number == number:
            print(subtitle.text + subtitle.start + " to " + subtitle.end)
            break


def write_subs(subs_file):
    # Add a 'shifted' suffix with millis to the file name, keeping the extension
    new_subs_file = subs_file.name.split(
        ".")[0] + "_shifted_" + millis + "." + subs_file.name.split(".")[1]
    with open(new_subs_file, "w") as f:
        for subtitle in subtitles:
            f.write(str(subtitle.number) + "\n")
            f.write(subtitle.start + " --> " + subtitle.end + "\n")
            f.write(subtitle.text + "\n")
            f.write("\n")
        f.close()


with open(subs_file) as subs_file:
    subtitles = parse_subs(subs_file)
    shift_subtitles(millis)
    write_subs(subs_file)
