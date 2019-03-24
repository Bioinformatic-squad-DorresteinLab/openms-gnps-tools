import os


def parsefolder(path, blacklist=["log"], whitelist=[""]):
    # check if dir exists
    if not os.path.exists(path):
        raise StopIteration

    # traverse dir
    for file in sorted(os.listdir(path)):
        # print(file)
        # print(blacklist[0])
        # print("now",blacklist[0] not in file)
        if file[0] is not '.' and all(bl not in file for bl in blacklist) \
        and whitelist and any(wl in file for wl in whitelist):
            # returns (path, count)
            yield (path+"/"+file, os.path.splitext(file)[0].split('-')[1])


def prevalidation(modulename, outpath, logtype="multiple", output_per_job=1):
    assert logtype in ("single", "multiple")
    assert type(output_per_job) is int

    print("os getcwd()",os.getcwd())
    print("os listdir", os.listdir("."))
    print("listdir featurefindermetabo",os.listdir("featurefindermetabo"))
    output_dir = list(parsefolder(outpath))
    # job num starts at 0
    num_jobs = int(max(output_dir, key=lambda x: x[1])[1]) + 1

    exp_log = 1 if logtype is "single" else num_jobs
    exp_output = output_per_jobs * num_jobs if output_per_job > 0 else 1

    num_log = 0
    num_output = 0
    for path,count in parsefolder(outpath, blacklist=[]):
        # log file
        if "log" in path:
            num_log += 1
            log_file = path
        # output file
        else:
            num_output += 1

    if num_log is 0:
        assert False, modulename.upper()+": Issue with executing module"
        # print .logs file is possible
        for file in os.listdir('.logs'):
            if modulename in file and os.path.splitext(file)[1] is "log":
                with open(".logs/"+file) as f:
                    print(f.read())
                    break
    elif num_output is 0 or num_log is not exp_log or num_output is not exp_output:
        with open(log_file) as f:
            print(f.read())

def postvalidation(modulename, outpath, logtype="multiple", output_per_job=1):
    assert logtype in ("single", "multiple")
    assert type(output_per_job) is int

    print("os getcwd()",os.getcwd())
    print("os listdir", os.listdir("."))
    print("listdir featurefindermetabo",os.listdir("featurefindermetabo"))
    output_dir = list(parsefolder(outpath))
    # job num starts at 0
    num_jobs = int(max(output_dir, key=lambda x: x[1])[1]) + 1
    print("num_jobs",num_jobs)

    exp_log = 1 if logtype is "single" else num_jobs
    exp_output = output_per_job * num_jobs if output_per_job > 0 else 1

    num_log = 0
    num_output = 0
    for path,count in parsefolder(outpath, blacklist=[]):
        # log file
        if "log" in path:
            num_log += 1
            log_file = path
        # output file
        else:
            num_output += 1

    if num_log is 0:
        assert False, modulename.upper()+": Issue with executing module"
        # print .logs file is possible
        for file in os.listdir('.logs'):
            if modulename in file and os.path.splitext(file)[1] is "log":
                with open(".logs/"+file) as f:
                    print(f.read())
                    break
    elif num_output is 0 or num_log is not exp_log or num_output is not exp_output:
        with open(log_file) as f:
            print(f.read())
