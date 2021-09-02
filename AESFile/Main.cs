using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.IO;
using System.Windows.Forms;

namespace AESFile
{
    public partial class Main : Form
    {
        OpenFileDialog openfile = new OpenFileDialog();
        OpenFileDialog savefile = new OpenFileDialog();

        public Main()
        {
            InitializeComponent();
            //Form2 frm2 = new Form2();
            initial();
            //frm2.Show();
        }

        private void initial()
        {
            openfile.Filter = "ini files |*.ini";   //存檔類型(此法才不會疊加副檔名)
            openfile.Multiselect = false;
            openfile.RestoreDirectory = true;

            //savefile.Filter = "ini files |*.ini";   //存檔類型(此法才不會疊加副檔名)
            //savefile.Multiselect = false;
            //savefile.RestoreDirectory = true;
        }

        private void button_AES_Decrypt_Click(object sender, EventArgs e)
        {
            if (openfile.ShowDialog(this) == DialogResult.OK)
            {
                //檔案解密
                //Function.AesDecryptFile(openfile.FileName, Application.StartupPath + "_" + "Decrypt" + "_" + DateTime.Now.ToLongTimeString().ToString() + ".ini", Function.AesKey, Function.AesIv);
                //Function.AesDecryptFile(openfile.FileName, Path.GetFileNameWithoutExtension(openfile.FileName) + "_" + "Decrypt" + ".ini", Function.AesKey, Function.AesIv);
                Function.AESCBCFile.AES_DecryptFile(openfile.FileName, Path.GetFileNameWithoutExtension(openfile.FileName) + "_" + "Decrypt" + ".ini");
            }
        }

        private void button_AES_Encrypt_Click(object sender, EventArgs e)
        {
            if (openfile.ShowDialog(this) == DialogResult.OK)
            {
                string xxx = Path.GetFileNameWithoutExtension(openfile.FileName);
                //檔案加密
                //Function.AesEncryptFile(openfile.FileName, Application.StartupPath + "_" + "Encrypt" + "_" + DateTime.Now().ToString("HH_mm_ss") + ".ini", Function.AesKey, Function.AesIv);
                //Function.AesEncryptFile(openfile.FileName, Path.GetFileNameWithoutExtension(openfile.FileName) + "_" + "Encrypt" + ".ini", Function.AesKey, Function.AesIv);
                Function.AESCBCFile.AES_EncryptFile(openfile.FileName, Path.GetFileNameWithoutExtension(openfile.FileName) + "_" + "Encrypt" + ".ini");
            }
        }
    }
}
