import re
import pandas as pd

def main():
    log_file = get_log_file_path_from_cmd_line()
    regex = r'\bDPT=(\d+)\b'
    filtered_logs, captured_data = filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=True, print_records=True)
    tally_port_traffic(filtered_logs)
    generate_port_traffic_report(log_file, '100')
    generate_port_traffic_report(log_file)
    generate_source_ip_log(log_file, '24.64.208.134')
# TODO: Step 3
def get_log_file_path_from_cmd_line():
    return 'gateway.log'

# TODO: Steps 4-7
def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    logs = []
    captured_data = []
    with open(log_file, 'r') as f:
        for line in f:
            match = re.search(regex, line, re.IGNORECASE if ignore_case else 0)
            if match:
                logs.append(line)
                captured_data.append(match.groups())
    if print_summary:
        print(f"Number of matching records: {len(logs)}")
    if print_records:
        for log in logs:
            print(log)
    return logs, captured_data

# TODO: Step 8
def tally_port_traffic(logs):
    traffic = {}
    for log in logs:
        match = re.search(r'\bDPT=(\d+)\b', log)
        if match:
            port = match.group(1)
            traffic[port] = traffic.get(port, 0) + 1

    return

# TODO: Step 9
def generate_port_traffic_report(log_file, port_number):
    data = []
    with open(log_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        fields = line.split()
        if fields[5] == port_number:
            date = fields[0]
            time = fields[1]
            src_ip = fields[2]
            dest_ip = fields[3]
            src_port = fields[4]
            port_number = fields[5]
            data.append([date, time, src_ip, dest_ip, src_port, port_number])
    filename = 'destination_port_%s_report.csv' % port_number
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Time', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port'])
        writer.writerows(data)
    print('Report successfully generated: %s' % filename)
    return

# TODO: Step 11
def invalid_users_report(log_file):
  infile = open(log_file, 'r')
  outfile = open('invalid_users.csv', 'w')
  outfile.write("Date,Time,Username,IP Address\n")
  for line in infile:
    fields = line.split(',')
    if fields[3] == "invalid":
      outfile.write("{},{},{},{}\n".format(fields[0], fields[1], fields[2], fields[4]))
  infile.close()
  outfile.close()

# TODO: Step 12
def generate_source_ip_log(log_file, ip_address):
    df = pd.read_csv(log_file, delimiter='\s+', header=None, index_col=False,
            names=['timestamp', 'host', 'service', 'message'])
    df_src = df[df['message'].str.contains(ip_address)]
    filename = 'source_ip_' + re.sub('\.', '_', ip_address) + '.log'
    df_src.to_csv(filename, index=False, header=False, sep=' ')
    print("File saved as " + filename)
    return

if __name__ == '__main__':
    main()