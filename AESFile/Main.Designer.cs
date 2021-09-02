namespace AESFile
{
    partial class Main
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.button_AES_Decrypt = new System.Windows.Forms.Button();
            this.button_AES_Encrypt = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(65, 71);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(98, 18);
            this.label1.TabIndex = 4;
            this.label1.Text = "欲加密檔案";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(65, 145);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(98, 18);
            this.label2.TabIndex = 5;
            this.label2.Text = "欲解密檔案";
            // 
            // button_AES_Decrypt
            // 
            this.button_AES_Decrypt.Location = new System.Drawing.Point(205, 137);
            this.button_AES_Decrypt.Margin = new System.Windows.Forms.Padding(4);
            this.button_AES_Decrypt.Name = "button_AES_Decrypt";
            this.button_AES_Decrypt.Size = new System.Drawing.Size(112, 34);
            this.button_AES_Decrypt.TabIndex = 6;
            this.button_AES_Decrypt.Text = "AES Decrypt";
            this.button_AES_Decrypt.UseVisualStyleBackColor = true;
            this.button_AES_Decrypt.Click += new System.EventHandler(this.button_AES_Decrypt_Click);
            // 
            // button_AES_Encrypt
            // 
            this.button_AES_Encrypt.Location = new System.Drawing.Point(205, 63);
            this.button_AES_Encrypt.Margin = new System.Windows.Forms.Padding(4);
            this.button_AES_Encrypt.Name = "button_AES_Encrypt";
            this.button_AES_Encrypt.Size = new System.Drawing.Size(112, 34);
            this.button_AES_Encrypt.TabIndex = 7;
            this.button_AES_Encrypt.Text = "AES Encrypt";
            this.button_AES_Encrypt.UseVisualStyleBackColor = true;
            this.button_AES_Encrypt.Click += new System.EventHandler(this.button_AES_Encrypt_Click);
            // 
            // Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 18F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(406, 233);
            this.Controls.Add(this.button_AES_Encrypt);
            this.Controls.Add(this.button_AES_Decrypt);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "Main";
            this.Text = "加密ini";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button button_AES_Decrypt;
        private System.Windows.Forms.Button button_AES_Encrypt;
    }
}

