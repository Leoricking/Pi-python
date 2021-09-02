using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Security.Cryptography;
using System.Runtime.InteropServices;

namespace AESFile
{
    class Function
    {
        public static string AesKey = "JaNdRgUkXp2s5u8x/A?D(G+KbPeShVmY"; //密鑰
        public static string AesIv = "UkXp2s5v8y/B?E(G"; //密鑰向量

        /// <summary>
        /// AES 加密字串
        /// </summary>
        /// <param name="original">原始字串</param>
        /// <param name="key">自訂金鑰</param>
        /// <param name="iv">自訂向量</param>
        /// <returns></returns>
        public static string AesEncrypt(string original, string key = null, string iv = null)
        {
            key = string.IsNullOrEmpty(key) ? AesKey : key;
            iv = string.IsNullOrEmpty(iv) ? AesIv : iv;

            string encrypt = "";
            try
            {
                AesCryptoServiceProvider aes = new AesCryptoServiceProvider();
                MD5CryptoServiceProvider md5 = new MD5CryptoServiceProvider();
                SHA256CryptoServiceProvider sha256 = new SHA256CryptoServiceProvider();
                byte[] keyData = sha256.ComputeHash(Encoding.UTF8.GetBytes(key));
                byte[] ivData = md5.ComputeHash(Encoding.UTF8.GetBytes(iv));
                byte[] dataByteArray = Encoding.UTF8.GetBytes(original);

                using (MemoryStream ms = new MemoryStream())
                {
                    using (
                        CryptoStream cs = new CryptoStream(ms, aes.CreateEncryptor(keyData, ivData), CryptoStreamMode.Write)
                    )
                    {
                        cs.Write(dataByteArray, 0, dataByteArray.Length);
                        cs.FlushFinalBlock();
                        encrypt = Convert.ToBase64String(ms.ToArray());
                    }
                }
            }
            catch (Exception ex)
            {
                //todo...
            }

            return encrypt;
        }

        /// <summary>
        /// AES 解密字串
        /// </summary>
        /// <param name="hexString">已加密字串</param>
        /// <param name="key">自訂金鑰</param>
        /// <param name="iv">自訂向量</param>
        /// <returns></returns>
        public static string AesDecrypt(string hexString, string key = null, string iv = null)
        {
            key = string.IsNullOrEmpty(key) ? AesKey : key;
            iv = string.IsNullOrEmpty(iv) ? AesIv : iv;

            string decrypt = hexString;
            try
            {
                SymmetricAlgorithm aes = new AesCryptoServiceProvider();
                MD5CryptoServiceProvider md5 = new MD5CryptoServiceProvider();
                SHA256CryptoServiceProvider sha256 = new SHA256CryptoServiceProvider();
                byte[] keyData = sha256.ComputeHash(Encoding.UTF8.GetBytes(key));
                byte[] ivData = md5.ComputeHash(Encoding.UTF8.GetBytes(iv));
                byte[] dataByteArray = Convert.FromBase64String(hexString);

                using (MemoryStream ms = new MemoryStream())
                {
                    using (
                        CryptoStream cs = new CryptoStream(ms, aes.CreateDecryptor(keyData, ivData), CryptoStreamMode.Write)
                    )
                    {
                        cs.Write(dataByteArray, 0, dataByteArray.Length);
                        cs.FlushFinalBlock();
                        decrypt = Encoding.UTF8.GetString(ms.ToArray());
                    }
                }
            }
            catch (Exception ex)
            {
                //todo...
            }

            return decrypt;
        }

        public static bool TryAesDecrypt(string hexString, out string original, string key = null, string iv = null)
        {
            return hexString != (original = AesDecrypt(hexString, key, iv));
        }

        /// <summary>
        /// AES 加密檔案
        /// </summary>
        /// <param name="sourceFile">原始檔案路徑</param>
        /// <param name="encryptFile">加密後檔案路徑</param>
        /// <param name="key">自訂金鑰</param>
        /// <param name="iv">自訂向量</param>
        public static bool AesEncryptFile(string sourceFile, string encryptFile, string key = null, string iv = null)
        {
            key = string.IsNullOrEmpty(key) ? AesKey : key;
            iv = string.IsNullOrEmpty(iv) ? AesIv : iv;

            if (string.IsNullOrEmpty(sourceFile) || string.IsNullOrEmpty(encryptFile) || !File.Exists(sourceFile))
            {
                return false;
            }

            try
            {
                AesCryptoServiceProvider aes = new AesCryptoServiceProvider();
                MD5CryptoServiceProvider md5 = new MD5CryptoServiceProvider();
                SHA256CryptoServiceProvider sha256 = new SHA256CryptoServiceProvider();
                byte[] keyData = sha256.ComputeHash(Encoding.UTF8.GetBytes(key));
                byte[] ivData = md5.ComputeHash(Encoding.UTF8.GetBytes(iv));
                aes.Key = keyData;
                aes.IV = ivData;

                using (FileStream sourceStream = new FileStream(sourceFile, FileMode.Open, FileAccess.Read))
                {
                    using (FileStream encryptStream = new FileStream(encryptFile, FileMode.Create, FileAccess.Write))
                    {
                        //檔案加密
                        byte[] dataByteArray = new byte[sourceStream.Length];
                        sourceStream.Read(dataByteArray, 0, dataByteArray.Length);

                        using (CryptoStream cs = new CryptoStream(encryptStream, aes.CreateEncryptor(), CryptoStreamMode.Write))
                        {
                            cs.Write(dataByteArray, 0, dataByteArray.Length);
                            cs.FlushFinalBlock();
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                //todo...
                return false;
            }

            return true;
        }

        /// <summary>
        /// AES 解密檔案
        /// </summary>
        /// <param name="encryptFile"></param>
        /// <param name="decryptFile"></param>
        /// <param name="key"></param>
        /// <param name="iv"></param>
        /// <returns></returns>
        public static bool AesDecryptFile(string encryptFile, string decryptFile, string key = null, string iv = null)
        {
            key = string.IsNullOrEmpty(key) ? AesKey : key;
            iv = string.IsNullOrEmpty(iv) ? AesIv : iv;

            if (string.IsNullOrEmpty(encryptFile) || string.IsNullOrEmpty(decryptFile) || !File.Exists(encryptFile))
            {
                return false;
            }

            try
            {
                AesCryptoServiceProvider aes = new AesCryptoServiceProvider();
                MD5CryptoServiceProvider md5 = new MD5CryptoServiceProvider();
                SHA256CryptoServiceProvider sha256 = new SHA256CryptoServiceProvider();
                byte[] keyData = sha256.ComputeHash(Encoding.UTF8.GetBytes(key));
                byte[] ivData = md5.ComputeHash(Encoding.UTF8.GetBytes(iv));
                aes.Key = keyData;
                aes.IV = ivData;

                using (FileStream encryptStream = new FileStream(encryptFile, FileMode.Open, FileAccess.Read))
                {
                    using (FileStream decryptStream = new FileStream(decryptFile, FileMode.Create, FileAccess.Write))
                    {
                        byte[] dataByteArray = new byte[encryptStream.Length];
                        encryptStream.Read(dataByteArray, 0, dataByteArray.Length);
                        using (CryptoStream cs = new CryptoStream(decryptStream, aes.CreateDecryptor(), CryptoStreamMode.Write))
                        {
                            cs.Write(dataByteArray, 0, dataByteArray.Length);
                            cs.FlushFinalBlock();
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                //todo...
                return false;
            }

            return true;
        }

        public class AESCBCFile
        {
            public static void AES_EncryptFile(string inputFile, string outputFile)
            {
                string Key = AesKey;
                Byte[] bKey = new Byte[32];
                Array.Copy(Encoding.UTF8.GetBytes(Key.PadRight(bKey.Length)), bKey, bKey.Length);

                string IvKey = AesIv;
                Byte[] bIvKey = new Byte[16];
                Array.Copy(Encoding.UTF8.GetBytes(IvKey.PadRight(bIvKey.Length)), bIvKey, bIvKey.Length);

                byte[] saltBytes = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8 };
                string cryptFile = outputFile;
                FileStream fsCrypt = new FileStream(cryptFile, FileMode.Create);

                RijndaelManaged AES = new RijndaelManaged();

                //var key = new Rfc2898DeriveBytes(passwordBytes, saltBytes, 1000);

                AES.KeySize = 256;
                AES.BlockSize = 128;

                AES.Key = bKey;
                AES.IV = bIvKey;

                //AES.Key = key.GetBytes(AES.KeySize / 8);
                //AES.IV = key.GetBytes(AES.BlockSize / 8);
                AES.Padding = PaddingMode.Zeros;
                //AES.Padding = PaddingMode.PKCS7;//非必須，但加了較安全
                AES.Mode = CipherMode.CBC;

                CryptoStream cs = new CryptoStream(fsCrypt,AES.CreateEncryptor(),CryptoStreamMode.Write);
                FileStream fsIn = new FileStream(inputFile, FileMode.Open);

                int data;
                while ((data = fsIn.ReadByte()) != -1)
                    cs.WriteByte((byte)data);

                fsIn.Close();
                cs.Close();
                fsCrypt.Close();

            }

            public static void AES_DecryptFile(string inputFile, string outputFile)
            {
                string Key = AesKey;
                Byte[] bKey = new Byte[32];
                Array.Copy(Encoding.UTF8.GetBytes(Key.PadRight(bKey.Length)), bKey, bKey.Length);

                string IvKey = AesIv;
                Byte[] bIvKey = new Byte[16];
                Array.Copy(Encoding.UTF8.GetBytes(IvKey.PadRight(bIvKey.Length)), bIvKey, bIvKey.Length);

                //byte[] saltBytes = new byte[] { 1, 2, 3, 4, 5, 6, 7, 8 };
                FileStream fsCrypt = new FileStream(inputFile, FileMode.Open);

                RijndaelManaged AES = new RijndaelManaged();

                AES.KeySize = 256;
                AES.BlockSize = 128;

                AES.Key = bKey;
                AES.IV = bIvKey;

                //var key = new Rfc2898DeriveBytes(passwordBytes, saltBytes, 1000);
                //AES.Key = key.GetBytes(AES.KeySize / 8);
                //AES.IV = key.GetBytes(AES.BlockSize / 8);
                AES.Padding = PaddingMode.Zeros;

                //AES.Padding = PaddingMode.PKCS7;//非必須，但加了較安全
                AES.Mode = CipherMode.CBC;

                CryptoStream cs = new CryptoStream(fsCrypt,AES.CreateDecryptor(),CryptoStreamMode.Read);
                FileStream fsOut = new FileStream(outputFile, FileMode.Create);

                int data;
                while ((data = cs.ReadByte()) != -1)
                    fsOut.WriteByte((byte)data);

                fsOut.Close();
                cs.Close();
                fsCrypt.Close();

            }
        }
    

        class Tracer
        {
            private static readonly int BlockBitSize = 128;
            private static readonly int KeyBitSize = 256;

            internal static byte[] In(byte[] plainBytes, byte[] uid)
            {
                using (var sha = new SHA512Managed())
                {
                    var hash = sha.ComputeHash(uid);
                    return In(plainBytes, hash.Skip(32).Take(32).ToArray(), hash.Take(16).ToArray());
                }
            }

            internal static byte[] In(byte[] plainBytes, byte[] key, byte[] iv)
            {
                if (key == null || key.Length != KeyBitSize / 8)
                    throw new ArgumentException(String.Format("Key needs to be {0} bit!", KeyBitSize), "key");
                if (iv == null || iv.Length != BlockBitSize / 8)
                    throw new ArgumentException(String.Format("IV needs to be {0} bit!", BlockBitSize), "iv");

                using (AesManaged aes = new AesManaged())
                {
                    aes.KeySize = KeyBitSize;
                    aes.BlockSize = BlockBitSize;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.None;

                    using (ICryptoTransform encrypter = aes.CreateEncryptor(key, iv))
                    using (MemoryStream cipherStream = new MemoryStream())
                    {
                        using (CryptoStream cryptoStream = new CryptoStream(cipherStream, encrypter, CryptoStreamMode.Write))
                        {
                            cryptoStream.Write(plainBytes, 0, plainBytes.Length);
                            cryptoStream.FlushFinalBlock();
                        }
                        return cipherStream.ToArray();
                    }
                }
            }

            internal static byte[] Out(byte[] cipherBytes, byte[] uid)
            {
                using (var sha = new SHA512Managed())
                {
                    var hash = sha.ComputeHash(uid);
                    return Out(cipherBytes, hash.Skip(32).Take(32).ToArray(), hash.Take(16).ToArray());
                }
            }

            internal static byte[] Out(byte[] cipherBytes, byte[] key, byte[] iv)
            {
                if (key == null || key.Length != KeyBitSize / 8)
                    throw new ArgumentException(String.Format("Key needs to be {0} bit!", KeyBitSize), "key");
                if (iv == null || iv.Length != BlockBitSize / 8)
                    throw new ArgumentException(String.Format("IV needs to be {0} bit!", BlockBitSize), "iv");

                using (AesManaged aes = new AesManaged())
                {
                    aes.KeySize = KeyBitSize;
                    aes.BlockSize = BlockBitSize;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.None;

                    using (ICryptoTransform decrypter = aes.CreateDecryptor(key, iv))
                    using (MemoryStream plainStream = new MemoryStream())
                    {
                        using (var decrypterStream = new CryptoStream(plainStream, decrypter, CryptoStreamMode.Write))
                        using (var binaryWriter = new BinaryWriter(decrypterStream))
                        {
                            //Decrypt Cipher Text from Message
                            binaryWriter.Write(cipherBytes, 0, cipherBytes.Length);
                        }
                        //Return Plain Text
                        return plainStream.ToArray();
                    }
                }
            }
        }

    }
}
