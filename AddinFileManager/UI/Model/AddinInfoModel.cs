using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AddinFileManager.UI.Model
{
    public class AddinInfoModel : ModelBase
    {
        private string m_InstallLocation;
        public string InstallLocation
        {
            get
            {
                return m_InstallLocation;
            }
            set
            {
                if (value != m_InstallLocation)
                {
                    m_InstallLocation = value;
                    RaisePropertyChanged(nameof(InstallLocation));
                }
            }
        }

        private string m_AddinFileName;
        public string AddinFileName
        {
            get
            {
                return m_AddinFileName;
            }
            set
            {
                if (value != m_AddinFileName)
                {
                    m_AddinFileName = value;
                    RaisePropertyChanged(nameof(AddinFileName));
                }
            }
        }

        private string m_Remark;
        public string Remark
        {
            get
            {
                return m_Remark;
            }
            set
            {
                if (value != m_Remark)
                {
                    m_Remark = value;
                    RaisePropertyChanged(nameof(Remark));
                }
            }
        }

        private bool m_IsOn;
        public bool IsOn
        {
            get
            {
                return m_IsOn;
            }
            set
            {
                if (value != m_IsOn)
                {
                    m_IsOn = value;
                    RaisePropertyChanged(nameof(IsOn));
                }
            }
        }
    }
}