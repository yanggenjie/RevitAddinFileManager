import os
import datetime
import shutil
import re
import subprocess
from multiprocessing.dummy import Pool as ThreadPool

# 配置环境路径,需要修改成自己电脑的路径，配置好之后，打开终端，输入：  python buildInstaller.py 运行脚本就行
# 注意是带双引号的，因为有些路径有空格，所以要用""限制一下，改双引号内的路径就行
# 编译工具的路径
devenvPath = r'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.com'
confuseExCli = r'D:\Programs\Windows\02Code\ConfuserEx\Confuser.CLI.exe'

# 基本配置，一般不用修改

# 要编译的解决方案，默认是在:  ../source/RevitGISApp.sln
slnName = "AddinFileManager.sln"

def DevBuildSln(slnPath, config="Release|Any CPU"):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(slnPath):
        print('sln文件不存在')
        return
    cmd = ['devenv.com', slnPath,
           "/Rebuild",  config]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)
    
def ConfuseExCli(crproj):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(crproj):
        print('sln文件不存在')
        return
    cmd = ['Confuser.CLI.exe',"-n", crproj]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)
def UpdateAssemblyVersion(srcDir):
    # 获得Assembly 文件
    # [assembly: AssemblyVersion("1.0.0.0")]
    # [assembly: AssemblyFileVersion("1.0.0.0")]

    assemblyInfoFiles = []
    for root, dirs, files in os.walk(srcDir):
        for f in files:
            if (f == "AssemblyInfo.cs"):
                fPath = os.path.join(root, f)
                assemblyInfoFiles.append(fPath)
    # 读取版本号那一行
    for f in assemblyInfoFiles:
        fContent = open(f, 'r', encoding='utf-8')
        lines = fContent.readlines()
        fContent.close()
        for i, curLine in enumerate(lines):
            if ((curLine.__contains__("AssemblyVersion") or (curLine.__contains__("AssemblyFileVersion"))) and not curLine.startswith("//")):
                mathchStr = "\"(.+?)\""
                # 获得版本号
                oldVersion = re.findall(mathchStr, curLine)
                numList = oldVersion[0].split(".")
                # 最后1位加1
                lastNum = int(numList[-1])+1
                numList[-1] = str(lastNum)
                # 重新合并成字符串
                newVersion = '"'+'.'.join(numList)+'"'
                # 替换原先的版本号
                curLine = re.sub(mathchStr, newVersion, curLine,
                                 count=0, flags=re.IGNORECASE)
                lines[i] = curLine
                print("oldVersion:"+oldVersion[0].removesuffix('\n'))
                print("newVersion:"+newVersion+"\n")
        # 重新写入文件
        fReWrite = open(f, "w", encoding='utf-8')
        for line in lines:
            fReWrite.write(line)
        fReWrite.close()

    # 修改增加版本号

    # 重新写入文件
    print("update Assembly Version")


if __name__ == '__main__':
    # 设置环境变量
    devenvPath = os.path.dirname(devenvPath)

    confuseExCli = os.path.dirname(confuseExCli)
    os.environ['PATH'] += os.pathsep + devenvPath + confuseExCli

    scriptsDir = os.path.dirname(__file__)
    rootDir = os.path.dirname(scriptsDir)
    sourceDir = os.path.join(rootDir, "source")

    # 更新Dll版本号
    UpdateAssemblyVersion(sourceDir)
    
    # 编译sln
    slnPath = os.path.join(sourceDir, slnName)
    DevBuildSln(slnPath)
    
    # 加密
    crproj=os.path.join(scriptsDir,"ob.crproj")
    ConfuseExCli(crproj)