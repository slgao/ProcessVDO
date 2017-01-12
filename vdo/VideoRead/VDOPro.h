//#ifdef VideoReadDLL_EXPORTS
#if defined(_MSC_VER)
//  Microsoft 
#define EXPORT __declspec(dllexport)
#define IMPORT __declspec(dllimport)
#elif defined(__GNUC__)
//  GCC
#define EXPORT __attribute__((visibility("default")))
#define IMPORT
#endif

//#define EXPORT __declspec(dllexport)
//#else
//#define EXPORT __declspec(dllimport)
//#endif

#define _CPPUNWIND // PYD file generation
#define _CRT_SECURE_NO_DEPRECATE

#include <boost/filesystem.hpp>
#include <boost/filesystem/path.hpp>
#include <boost/progress.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstring>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string>
#include <iomanip>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#if CV_MAJOR_VERSION>2
#include <opencv2/imgcodecs.hpp>
#else
#include <opencv2/highgui/highgui.hpp>
#endif
#include <math.h>

#pragma pack(1)

namespace fs = boost::filesystem;
typedef std::vector<std::string> SVec;

/***************************************************************
* GENERAL DATA
* *************************************************************/

// Video flags
#define PIXEL_16BIT            0x0100
#define IMAGE_COMPRESSED       0x0200
#define PIXEL_24BIT            0x0400

//8Bit images
#define IMAGE_MONO8            0x0001
//16Bit images
#define IMAGE_MONO16           0x0101
#define IMAGE_MONO12           0x0102
//Compressed images
#define IMAGE_JPEG             0x0201
#define IMAGE_GDM_LINEAR_COLOR 514//0x0202 // 514
#define IMAGE_GDM_LINEAR_BW    515//0x0203 // 515
//24 bit
#define IMAGE_RGB24            0x0401

#define MAKE_PORT( A, B, C, D )     ( (((unsigned int)(A)   )<<24) | (((unsigned int)(B)   )<<16) | (((unsigned int)(C)   )<<8) | ((unsigned int)(D)   ) )
#define VIDEO_FIF                   MAKE_PORT('D','v','i','d')     // use for Video frames
#define DECOMPRESS
static bool DecompandSaveIm = false;
static bool NoDecomp = false;
static bool ImgCorr = true;
static bool img_first_show = true;
static unsigned int log2p1_lut[] = {
	1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
	8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
};

typedef struct Format
{
	char N0, N1, N2, N3;
} Format;

typedef struct infelHd_ss
{
	unsigned int infid;     // Data type identifier / Format identifier
	int totlen;     // Total length in bytes, including the following data (in Network order)
} infelHd_s;

typedef struct Stamp_ss
{
	int Clock;     // Clock relative to the packet
	int Odom;     // Odometer relative to the packet
} Stamp_s;

typedef struct Video_d_ss
{
	int32_t  sid;     // station ID of the camera that generated the packet
	Stamp_s  St;     // see above
	uint32_t frameCnt;     // number of the frame
	uint32_t exposition;     // exposition
	uint16_t image_type;     // it can be IMAGE_JPEG (0x0201) for the panocam
							 //           IMAGE_GDM_LINEAR_COLOR (0x0202) for the linear color camera
							 //           IMAGE_GDM_LINEAR_BW (0x0203) for the linear B&W camera
	uint16_t position;     // position
	uint16_t width;     // width of the information sent
	uint16_t w_step;     // width step
	uint16_t w_offset;     // width offset
	uint16_t height;     // height of the information sent
	uint16_t h_step;     // height step
	uint16_t h_offset;     // height offset
	unsigned char px[1];      // pixels data information
							  //std::string px;

} Video_d_s;

typedef struct Video_i_ss
{
	infelHd_s h;     // see above
	Video_d_s d;     // see above
} Video_i_s;

/******************************************************************
* DECOMPRESSION DATA
* ****************************************************************/

#define SUBSAMPLE_SIZE 4

struct yuv_t
{
	unsigned char y;
	signed char   cr;
	signed char   cb;
};

struct yuv_dif_t
{
	signed char   dy;
	signed char   du;
	signed char   dv;
};

struct locogio_bh_s
{
	unsigned int  bsy : 4;
	unsigned int  bsu : 4;
	unsigned int  bsv : 4;
};

struct locogio_s
{
	unsigned int   length;
	int            subsample;
	int            color;
	int            cblock_size;
	int            lenght_bsh;

	yuv_t         *yuv;
	yuv_dif_t     *dif;
	unsigned char *cbuffer;
	unsigned int   cbuffer_ptr;
	int            cbuffer_bit_ptr;
	unsigned int   compress_size;
};

#define INDEXER_VERSION 0x0001

#pragma pack(1)
struct Indexer_s
{
	int      odometer;
	uint64_t byteOffset;
	int      filePart;

	Indexer_s(int a_Odometer, uint64_t a_Offset, int a_Part)
	{
		odometer = a_Odometer;
		byteOffset = a_Offset;
		filePart = a_Part;
	}

	Indexer_s(void)
	{
		odometer = 0;
		byteOffset = 0;
		filePart = 0;
	}

	static Indexer_s * IndexFactory(unsigned short a_Version, const void *a_Buffer)
	{
		switch (a_Version)
		{
		case INDEXER_VERSION:
		{
			return new Indexer_s(*(Indexer_s *)a_Buffer);
			break;
		}
		default:
		{
			printf("[Indexer] Unrecognized indexer version %X\n", a_Version);
			return NULL;
		}
		}
	}
};
#pragma pack()

extern "C"
{

	double DeterGamma(std::string CamID);

	void ShowUsage1();

	void ShowUsage2();

	void ShowUsage3();

	int CheckFolderExists_CreateFolder(std::string Folder);

	void ConstructFCatalog(std::vector<SVec> * FCatalog);

	void CheckEndian(int *Endianness);

	bool GetFileInDir(std::string InputDir, SVec *FileList);

	bool GetFileandDir(std::string InputDir, SVec *FileList, SVec *dirs);

	void elimVerboseF(SVec *Filelist, std::string CamID);

	void elimVDOs(SVec *Filelist);

	void GetIdxFilefromNonVdoFile(SVec *Filelist, std::string CamID);

	int countAsterisk(std::string inString);

	bool existAsterisk(std::string inString);

	//EXPORT SVec Clear1Asterisk(std::string inString);

	//EXPORT SVec Clear2Asterisk(std::string inString);

	void CatalogFile(std::vector<SVec> *FCatalog, SVec Filelist);

	void SortCatalog(std::vector<SVec> *FCatalog);

    int getFilelist(std::string dir, std::string CamID, std::string &directory, SVec &Filelist);
    
	EXPORT int getOdoRange(std::string dir, std::string CamID, long int &odo_min, long int &odo_max);

	EXPORT int ImOutVDORange(long int Start, long int End, SVec *VDOFIles, std::string directory, bool pano_all_export, double Uncertainty);

	/******************************************************************
	* DECOMPRESSION
	******************************************************************/

	static unsigned char CLAMP(short a_X);

	bool locogio_init(locogio_s *a_Loco, int a_Length, int a_Color, int a_Bsize = 8, int a_Subsample = 1);

	//int locogio_decompress_line_meta(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize,
	//	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType,
	//	std::vector<std::vector<char>> *VideoData, int OutputOption);

	cv::Mat locogio_decompress_line(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize, cv::Mat &image,
		std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType);

	static unsigned char read_bits(struct locogio_s *a_Loco, int l_Bits, bool l_SignExt);

	static void read_bsh(struct locogio_s *a_Loco, struct locogio_bh_s &a_Bsh);

	static void decompress(locogio_s *a_Loco, int a_LengthBits);

	/******************************************************************
	* COMPRESSION
	******************************************************************/

	int locogio_compress_line(locogio_s *a_Loco, unsigned char *a_Line, unsigned char *l_Out);

	static void push_bits(locogio_s *l_Loco, unsigned char *l_Value, int l_Bits);

	static void push_bsh(locogio_s *l_Loco, locogio_bh_s &l_Bsh);

	static int log2p1c(short a_Value);

	static int compress(locogio_s *l_Loco);

	void ImgCorrection(cv::Mat &InImg, double gamma, cv::Mat &OutImg);

	void SaveJPEG_fb(bool Jdir_created, std::string CamID, std::string log_path,
		int NumFrame, Video_d_s *l_Video, size_t l_VideoDataSize, int Odo);

	void SaveJPEGS_fb(bool Jdir_created, std::string CamID, std::string log_path, std::vector<std::vector<int>> *VideoData, int Odo);
	// inline void WriteVDO(std::ofstream VDOWriter, infelHd_s *l_Header, char * l_HeaderData, char * l_VideoData, 
	// 					 unsigned int length, size_t l_HeaderSize, std::string Folder);
	// 
	int SaveJPEG_LCam(bool Jdir_created, std::string CamID, std::string log_path, std::string ImgName,
		std::vector<std::vector<int>> VideoData);

	void Vec2Mat(std::vector<std::vector<int>> VideoData, cv::Mat &Img, std::string CamID);

	//void LinearCamDecompMeta(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
	//	unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen, std::string CamID, std::string log_path,
	//	int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, std::vector<std::vector<char>> *VideoData, int OutputOption);

	unsigned int LinearCamDecompression(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
		unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen, cv::Mat &image,
		std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, bool ImgCorr);

	int ArgtoVal(std::string InputArg, long int *StartIntern, long int *EndIntern, std::string *SID);

	// "extern "C" makes sure that the function name in the exported dll file is the same as the one in source code"
	/*extern "C"
	{
	_declspec(dllexport) int VideoReadDLLcess(int argc, QString indir, QString outdir);
	}*/

	EXPORT int VDORPW(std::string indir, std::string outdir);


	bool copyDir(
		boost::filesystem::path const & source,
		boost::filesystem::path const & destination
		);

	EXPORT int GetMetadataFromIntCnt(std::string dir, std::string saverange,
		std::vector<Video_d_s> *RangeVideoData, std::vector<infelHd_s> *RangeHeaderData, std::vector<std::vector<char>> *VideoData,
		int OutputOption, bool save_pano_img, bool save_csv_info, double Uncertainty);

	Indexer_s *get_indexer_from_given_odo(int Odometer, std::string idx_file, bool l_odo_boundary);

	void ReadVDObyBlock(const char *input_dir, const char *CamID, int odo_start, int odo_end,
		signed char **VD, int *odos, int *row, int *col);

	void ReadVDOInit(const char *input_dir, const char *CamID, long int &odo_min, long int &odo_max);
    
	int OutputExtCnt_FNumfromVDO(std::string VDOFiles);

	int ReadVDO(std::string input_dir, std::string CamID, int Odometer);

	int locogio_decompress_line_imshow(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize,
		std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType,
		cv::Mat &img_show, int OutputOption, int &jump_line, int Odometer);

	int LinearCamDecompImgShow(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
		unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen,
		std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created,
		bool DecompandSaveIm, cv::Mat &img_show, int OutputOption, int &jump_line, int Odometer);

	void ShowFB(bool Jdir_created, std::string CamID, std::string log_path,
		int NumFrame, Video_d_s *l_Video, size_t l_VideoDataSize, int Odo);

	void WriteTextOnImg(cv::Mat &Image, std::string Text);

	int FillDisWin(std::vector<std::vector<int>> &dis_img, cv::Mat &img,
		size_t height, std::vector<std::vector<int>> &VideoData, std::string CamID, bool &init);
}
