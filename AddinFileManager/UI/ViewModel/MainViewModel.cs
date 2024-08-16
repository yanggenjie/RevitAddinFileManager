using AddinFileManager.Common;
using AddinFileManager.UI.Model;
using CommunityToolkit.Mvvm.ComponentModel;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AddinFileManager.UI.ViewModel
{
    public partial class MainViewModel : ObservableObject
    {

        private List<string> DefaultAddinFileNames = new()
        {
            "ExportViewSelectorApp",
            "Communicator",
            "FormItConverter",
            "BIM360GlueRevitAddin",
            "BIM360GlueRevit2016Addin",
            "Dynamo",
        };
        [ObservableProperty]
        private string selectedVersion;
        partial void OnSelectedVersionChanged(string value)
        {
            AddinFileItems.Clear();
            var version = value.Split(' ').LastOrDefault();
            var appFolder = @"C:\ProgramData\Autodesk\Revit\Addins";
            GetApplicationAddinInfos(appFolder, version, "全局安装目录");
            // 用户目录
            var userProfileFolder = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            var userFolder = Path.Combine(userProfileFolder, "Autodesk\\Revit\\Addins");
            GetApplicationAddinInfos(userFolder, version, "用户安装目录");
        }

        private void GetApplicationAddinInfos(string addinFolder, string? version, string installLocation)
        {
            if (string.IsNullOrWhiteSpace(version)) return;
            // 全局目录
            var currentVersion = Path.Combine(addinFolder, version);
            if (!Directory.Exists(currentVersion)) return;
            var addinFiles = from f in Directory.GetFiles(currentVersion, "*.*", SearchOption.TopDirectoryOnly)
                             let ext = Path.GetExtension(f)
                             where ext == ".addin" || ext == CommonString.DisableExt
                             let fileName = Path.GetFileNameWithoutExtension(f)
                             where !fileName.StartsWith("Autodesk") && !DefaultAddinFileNames.Contains(fileName)
                             select f;
            foreach (var file in addinFiles)
            {
                var fileName = Path.GetFileName(file);
                var fileExt = Path.GetExtension(file);
                var allLines = File.ReadAllLines(file).Where(x => x.StartsWith("<Name>"));
                if (allLines.Any())
                {
                    foreach (var line in allLines)
                    {
                        var addinName = line.Replace("<Name>", "").Replace("</Name>", "").Replace(" ", "");
                        var addinInfo = new AddinInfoModel()
                        {
                            FileFullPath = file,
                            InstallLocation = installLocation,
                            AddinFileName = addinName,
                            IsOn = true,
                        };
                        AddinFileItems.Add(addinInfo);
                    }
                }
                else
                {
                    var addinInfo = new AddinInfoModel()
                    {
                        FileFullPath = file,
                        InstallLocation = installLocation,
                        AddinFileName = fileName,
                        IsOn = fileExt != CommonString.DisableExt,
                    };
                    AddinFileItems.Add(addinInfo);
                }
            }
        }

        public ObservableCollection<string> RevitVersionItems { get; set; } = new()
        {
            "Autodesk Revit 2015",
            "Autodesk Revit 2016",
            "Autodesk Revit 2017",
            "Autodesk Revit 2018",
            "Autodesk Revit 2019",
            "Autodesk Revit 2020",
            "Autodesk Revit 2021",
            "Autodesk Revit 2022",
            "Autodesk Revit 2023",
            "Autodesk Revit 2024",
            "Autodesk Revit 2025",
        };
        public ObservableCollection<AddinInfoModel> AddinFileItems { get; set; } = new();

        public MainViewModel()
        {

        }
    }
}
