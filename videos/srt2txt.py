import sys
import re

def convert_srt2txt(filename):

    input_file_name = filename + '.en.srt'
    output_file_name = filename + '.txt'

    # Output file
    f_out = open(output_file_name, 'w')

    # Process with opening the input file.
    with open(input_file_name) as f_in:
        #!remove blank lines!
        lines = f_in.read()
        prog = re.compile('<[^>]*>')
        lines_temp = prog.split(lines)

        lines = []
        for line in lines_temp:
            lines.extend(line.rstrip().split())

        #remove unnecessary lines and write it to a new file
        for line in lines:                
            # Ignore the numeric ID of each text
            if line.isdigit() and len(line) < 4:
                continue
            # Ignore the time indicator such as '00:00:12,340' 
            if line.startswith('0'):
                continue
            # Ignore some trivial attributes such as '<font>~</font>'
            if line.startswith('font') or line.startswith('/font') or line.startswith('-->'):
                continue
                
            f_out.write(line + '\r\n')

    f_in.close()
    f_out.close()
