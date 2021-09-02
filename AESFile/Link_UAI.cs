using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;

namespace LEDtest
{
    class Link_UAI
    {
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerGetDeviceList", CallingConvention = CallingConvention.Cdecl)]
        public unsafe static extern UInt32 UAI_SpectrometerGetDeviceList(ref UInt32 BufferSize, UInt32* VIDPID);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerGetDeviceAmount", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerGetDeviceAmount(UInt32 VID, UInt32 PID,ref uint NumDevices);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerOpen", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerOpen(uint dev, ref IntPtr handle, UInt32 VID, UInt32 PID);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerClose", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerClose(IntPtr handle);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectromoduleGetFrameSize", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectromoduleGetFrameSize(IntPtr handle, ref ushort frame_size);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerWavelengthAcquire", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerWavelengthAcquire(IntPtr handle, float[] buffer);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerDataAcquire", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerDataAcquire(IntPtr handle, uint integration_time_us, float[] buffer, uint average);

        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerDataOneshot", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerDataOneshot(IntPtr handle, uint integration_time_us, float[] buffer, uint average);

        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerFinalDataDataAcquire", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_SpectrometerFinalDataDataAcquire(IntPtr handle, uint integration_time_us, float[] buffer, uint average, uint AcquireType, uint IntensityCalibrationType);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_SpectrometerGetSerialNumber", CallingConvention = CallingConvention.Cdecl)]
        public unsafe static extern UInt32 UAI_SpectrometerGetSerialNumber(IntPtr handle, byte[] SN);

        //For Color
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorInformationAllocation", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorInformationAllocation(ref IntPtr color, uint type, uint observer, uint illuminant, float[] lumbda, float[] intensity_r, float[] intensity_m, uint size);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorInformationFree", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorInformationFree(IntPtr color);

        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorOperation", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorOperation(IntPtr color);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetXYZ", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetXYZ(IntPtr color, double[] xyz);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetxyz", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetxyz(IntPtr color, double[] xyz);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetLuv", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetLuv(IntPtr color, double[] Luv);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGet1976ucs", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGet1976ucs(IntPtr color, double[] uvw);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetDominantWavelength", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetDominantWavelength(IntPtr color, ref double lumbda_d);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetPurity", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetPurity(IntPtr color, ref double purity_e);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetCCT", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetCCT(IntPtr color, ref double CCT);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetColorRenderingIndex", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetColorRenderingIndex(IntPtr color,  double[] cri);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetColorQualityScale", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetColorQualityScale(IntPtr color, double[] cqs);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_ColorGetRadiantPower", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_ColorGetRadiantPower(IntPtr color, ref double RadiantPower);


        //For Calibration
        [DllImport("UserApplication.dll", EntryPoint = "UAI_BackgroundRemove", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_BackgroundRemove(IntPtr handle, uint integration_time_us,float[] intensity);
        [DllImport("UserApplication.dll", EntryPoint = "UAI_BackgroundRemoveWithAVG", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_BackgroundRemoveWithAVG(IntPtr handle, uint integration_time_us, float[] intensity);

        [DllImport("UserApplication.dll", EntryPoint = "UAI_LinearityCorrection", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_LinearityCorrection(IntPtr handle, uint framesize, float[] intensity);

        [DllImport("UserApplication.dll", EntryPoint = "UAI_AbsoluteIntensityCorrection", CallingConvention = CallingConvention.Cdecl)]
        public static extern UInt32 UAI_AbsoluteIntensityCorrection(IntPtr handle, float[] intensity, uint integration_time_us);

        public static int LastIndexOfnumber(byte[] sample)
        {
            int index = sample.Length;
            for (int i = 0; i < sample.Length; i++)
            {
                if (sample[i] == 0)
                    index = i;
            }
            return index;
        }
    }
}
