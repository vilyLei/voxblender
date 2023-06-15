import subprocess

blender_command = "D:\programs\\blender\\blender.exe -b -P .\\renderingModelFile.py"
process = subprocess.Popen(blender_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

for line in iter(process.stdout.readline, ""):
    print(line, end="")
    if "Fra:" in line:
        print("## line info: ", line)
        # progress_info = line.split()
        # current_frame = int(progress_info[1])
        # total_frames = int(progress_info[3])
        # render_percentage = (current_frame / total_frames) * 100
        # print(f"Render progress: {render_percentage:.2f}%")
        
# process.stdout.close()
process.wait()

print("####### bcRenderCall01 end ...")
# python .\bcRenderCall01.py