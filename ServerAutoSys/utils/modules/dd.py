from sh import tail
def process_output(line, stdin, process):
    print(line)
    process.kill()
    return True

p = tail("-f", "/var/log/messages", _out=process_output)
p.wait()
