using AddinFileManager.UI.Model;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AddinFileManager.UI.ViewModel
{
    public class MainViewModel
    {
        public ObservableCollection<AddinInfoModel> AddinFileItems { get; set; } = new()
        {
            new AddinInfoModel()
            {
                InstallLocation="test",
                AddinFileName="test",
                IsOn=true,
            }
        };
        public MainViewModel()
        {

        }
    }
}
