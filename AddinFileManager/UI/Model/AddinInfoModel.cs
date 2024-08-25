using AddinFileManager.Common;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AddinFileManager.UI.Model
{
    public partial class AddinInfoModel : ObservableObject
    {
        [ObservableProperty]
        private string installLocation;

        [ObservableProperty]
        private string addinFileName;

        [ObservableProperty]
        private string remark;

        [ObservableProperty]
        private bool isOn;

        partial void OnIsOnChanged(bool value)
        {
            if (!File.Exists(FileFullPath)) return;
            var fileExt = Path.GetExtension(FileFullPath);
            var fileName = Path.GetFileName(FileFullPath);
            var folder = Path.GetDirectoryName(FileFullPath);

            if (isOn && fileExt == CommonString.DisableExt)
            {
                fileName = fileName.Replace(CommonString.DisableExt, "");
                var newFile = Path.Combine(folder, fileName);
                File.Move(FileFullPath, newFile);
                FileFullPath = newFile;
                AddinFileName = fileName;
            }
            else if (!isOn && fileExt != CommonString.DisableExt)
            {
                fileName = fileName + CommonString.DisableExt;
                var newFile = Path.Combine(folder, fileName);
                File.Move(FileFullPath, newFile);
                FileFullPath = newFile;
                AddinFileName = fileName;
            }
        }

        public string FileFullPath { get; set; }

        [RelayCommand]
        private void OpenFolder()
        {
            var folder = Path.GetDirectoryName(FileFullPath);
            if (!Directory.Exists(folder)) return;
            var psi = new ProcessStartInfo
            {
                FileName = folder,
                UseShellExecute = true,
            };
            Process.Start(psi);
        }
    }
}