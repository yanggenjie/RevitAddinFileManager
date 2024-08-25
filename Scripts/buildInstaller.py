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
# 混淆加密软件的路径
ezirizPath = r'C:\Users\workstation01\A_Programs\Windows\02Code\Eziriz\.NET Reactor\dotNET_Reactor.exe'
# inno setup安装包制作工具的路径
innoSetupPath = r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
dotnetExe = r'C:\Program Files\dotnet\dotnet.exe'

obfuscarPath = r'C:\Users\workstation01\A_DataBases\Source\nuget\obfuscar\Obfuscar.2.2.39\tools\Obfuscar.Console.exe'

# 基本配置，一般不用修改
# 安装包文件名，默认会在当前目录搜索，填文件名就行
issFileName = "installer.iss"
# 要编译的解决方案，默认是在:  ../source/RevitGISApp.sln
slnName = "AddinFileManager.sln"
# 要编译的配置名称：这里编译的是离线版本的
buildConfig = "Release"
# 要加密的dll前缀，根据前缀去匹配所有dll，只要以RevitGIS开头的dll，都会被加密混淆
dllPrefix = "AddinFileManager"


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


def MsBuildSln(slnPath, config="Release"):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(slnPath):
        print('sln文件不存在')
        return
    cmd = ['Msbuild.exe', slnPath, "-r",
           "/t:rebuild",  f"/p:Configuration={config}"]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)
    

def DotnetPublish(slnPath, config="Release"):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(slnPath):
        print('sln文件不存在')
        return
    cmd = ['dotnet.exe', 'publish', slnPath, "-p:PublishProfile=FolderProfile"]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)


def BuildIss(issProfile):
    if not os.path.exists(issProfile):
        print('sln文件不存在')
        return
    cmd = ['ISCC.exe', issProfile]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)

def ObfuscarEncryptDll():
    obfuscar = r'Obfuscar.Console.exe'
    cmd = obfuscar + " " + 'obfuscar.xml'
    subprocess.run(cmd, shell=False, capture_output=False, text=False)

def EncryptDll(obfFileFullPaths):
    """
    加密dll
    """
    dotNetReactor = r'dotNET_Reactor.exe'
    # 拼接加密参数
    para1 = '-showloadingscreen 0'.split(' ')
    para4 = '-necrobit 1 -necrobit_comp 1 -suppressildasm 0 -obfuscation 0 -mapping_file 0 -antitamp 0 -stringencryption 1 -resourceencryption 1 -control_flow_obfuscation 1 -flow_level 9'.split(
        ' ')

    encryptCmds = []
    encryptCmds.clear()
    for f in obfFileFullPaths:
        # 加密前的dll和加密后的dll为相同路径
        # 即加密后，直接覆盖原先的dll
        if not os.path.exists(f):
            continue
        beforeObf = f
        afterObf = f
        para2 = ['-file', beforeObf]
        para3 = ['-targetfile', afterObf]
        para = para1+para2+para3+para4
        cmd = [dotNetReactor]+para
        encryptCmds.append(cmd)

    # for cmd in encryptCmds:
    #     ExcuteEncryptCmd(cmd)
    pool = ThreadPool()
    pool.map(ExcuteEncryptCmd, encryptCmds)
    pool.close()
    pool.join()


def ExcuteEncryptCmd(cmd):
    ret = subprocess.run(cmd, shell=False, capture_output=True, text=True)
    if ret.stdout.__contains__('Successfully'):
        print('加密: '+cmd[4].split('\\')[-1])
        print(ret.stdout)
    elif len(ret.stdout) == 0:
        print("已加密"+cmd[4].split('\\')[-1])
    else:
        print("加密失败"+cmd[4].split('\\')[-1])


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
    innoSetupPath = os.path.dirname(innoSetupPath)
    ezirizPath = os.path.dirname(ezirizPath)
    dotnetPath = os.path.dirname(dotnetExe)
    obfuscarPath = os.path.dirname(obfuscarPath)
    os.environ['PATH'] += os.pathsep + devenvPath + \
        innoSetupPath + ezirizPath + dotnetPath + obfuscarPath

    scriptsDir = os.path.dirname(__file__)
    rootDir = os.path.dirname(scriptsDir)
    sourceDir = os.path.join(rootDir, "source")

    # 更新Dll版本号
    # UpdateAssemblyVersion(sourceDir)
    # 更新安装包版本号
    # issFilePath = os.path.join(scriptsDir, issFileName)
    # with open(file=issFilePath, mode='r', encoding='utf-8') as issFile:
    #     issContent = issFile.readlines()
    #     for index, value in enumerate(issContent):
    #         if value.startswith('#define MyAppVersion'):
    #             dot = value.rfind('.')+1
    #             num = int(value[dot:-2]) + 1
    #             value = value[:dot]+str(num)+value[-2:]
    #             # value = value.replace(value[dot:-2], str(num))
    #             issContent[index] = value
    #         elif value.startswith('OutputBaseFilename='):
    #             # today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #             today = datetime.datetime.now().strftime('%Y%m%d')
    #             lastDate = value[value.index('(') + 1:value.index('-')]
    #             dot = value.rfind('.')+1
    #             num = int(value[dot:-2]) + 1
    #             value = value[:dot]+str(num)+value[-2:]
    #             issContent[index] = value.replace(lastDate, today)
    # with open(file=issFilePath, mode='w', encoding='utf-8') as issFile:
    #     issFile.writelines(issContent)

    # 清理bin目录
    binDir = os.path.join(sourceDir, "bin\\publish\\win-x64")
    shutil.rmtree(binDir, ignore_errors=True)
    # 编译sln
    slnPath = os.path.join(sourceDir, slnName)
    DotnetPublish(slnPath, buildConfig)

    # 混淆代码
    # obfiles = []
    # for root, dirs, files in os.walk(binDir):
    #     for f in files:
    #         fPath = os.path.join(root, f)
    #         if f.startswith(dllPrefix) and f.endswith('.dll'):
    #             obfiles.append(fPath)
    ObfuscarEncryptDll()
    # 清理无用文件
    for root, dirs, files in os.walk(binDir):
        for f in files:
            fPath = os.path.join(root, f)
            if f.startswith(dllPrefix) and f.endswith('.config'):
                os.remove(fPath)
            if f.endswith('.pdb') or f.endswith('.hash'):
                os.remove(fPath)
    # 编译安装包
    issProj = os.path.join(scriptsDir, issFileName)
    BuildIss(issProj)
