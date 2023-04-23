import os


def write_build_report(target_dir, name, data):
    filename = name + '_builds.txt'
    script_file = os.path.join(target_dir, filename)
    f = open(script_file, "a")
    f.write("-----------------------------------------------------------\n")
    f.write(f"  Build for: {name}\n")
    f.write(f"    When:    {data['datetime']}\n")
    f.write(f"    Branch:  {data['branch']}\n")
    f.write(f"    Commit:  {data['sha']}\n")
    f.write(f"    Dirty:   {data['dirty']}\n")
    f.close()

