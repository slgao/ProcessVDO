#include "VDOPro.h"

double DeterGamma(std::string CamID)
{
	if (CamID.compare("60") == 0 || CamID.compare("70") == 0 || CamID.compare("62") == 0 || CamID.compare("72") == 0)
		return 1.2; //3.0
	else if (CamID.compare("64") == 0 || CamID.compare("74") == 0)
		return 1.3; //3.5
	else
		return 1.2; // 2.5
}

void ShowUsage1()
{
	printf("Parameters accepted by VDORPW\n");
	printf("-First parameter:\tDirectory to open VDO files or \"help\" to show helping info\n");
	printf("-Second parameter:\tDirectory to write VDO files\n");
}

void ShowUsage2()
{
	printf("Parameters accepted by GetMetadataFromIntCnt\n");
	printf("-First parameter:\tFile to open or \"help\" to show helping info\n");
	printf("-Second parameter:\tStationId to save [OPTIONAL]\n");
	printf("-Third parameter:\tstd::vector<Video_d_s> *RangeVideoData\n");
	printf("-Fourth parameter:\tstd::vector<infelHd_s> *RangeHeaderData\n");
	printf("-Fifth parameter:\tstd::vector<std::vector<int>> *VideoData\n");
	printf("-Sixth parameter:\tint OutputOption -- (0: Compressed binary data; 1: RGB data; 2: YUV data)");
	//
	printf("_First parameter can be in the form of:\n");
	printf("[DIRECTORY]\\ or\n");
	printf("[DIRECTORY]\\[FILENAME] or\n");
	printf("[DIRECTORY]\\*[SOMETHING] or\n");
	printf("[DIRECTORY]\\[SOMETHING]*[SOMETHING] or\n");
	printf("[DIRECTORY]\\*[SOMETHING]*[SOMETHING]\n");

	printf("_Second parameter can be in the form of:\n");
	printf("[CamID]");
	printf("{CamID[Cnt, Cnt]}");
}

void ShowUsage3()
{
	printf("Parameters accepted by OutputExtCnt_FNumfromVDO\n");
	printf("-Parameter:\tFile to open or \"help\" to show helping info\n");
	//
	printf("Parameter can be in the form of:\n");
	printf("[DIRECTORY]\\ or\n");
	printf("[DIRECTORY]\\[FILENAME] or\n");
	printf("[DIRECTORY]\\*[SOMETHING] or\n");
	printf("[DIRECTORY]\\[SOMETHING]*[SOMETHING] or\n");
	printf("[DIRECTORY]\\*[SOMETHING]*[SOMETHING]\n");
}

int CheckFolderExists_CreateFolder(std::string Folder)
{
	if (!fs::exists(Folder))
	{
		fs::path F(Folder);
		fs::create_directories(F);
		return 0;
	}
	else
		return 1;
}

void ConstructFCatalog(std::vector<SVec> * FCatalog)
{
	SVec Cam60, Cam62, Cam70, Cam72,
		Cam64, Cam65, Cam74, Cam75,
		Cam61, Cam71, Camc50, Camc51;
	FCatalog->push_back(Cam60);
	FCatalog->push_back(Cam61);
	FCatalog->push_back(Cam62);
	FCatalog->push_back(Cam64);
	FCatalog->push_back(Cam65);
	FCatalog->push_back(Cam70);
	FCatalog->push_back(Cam71);
	FCatalog->push_back(Cam72);
	FCatalog->push_back(Cam74);
	FCatalog->push_back(Cam75);
	FCatalog->push_back(Camc50);
	FCatalog->push_back(Camc51);
}

// 0 is little Endian, 1 is big Endian
void CheckEndian(int *Endianness)
{
	int TestNum = 1;
	if (*(char *)&TestNum == 1)
		*Endianness = 0;
	else
		*Endianness = 1;
}

bool GetFileInDir(std::string InputDir, SVec *FileList)
{
	fs::path full_path(fs::initial_path<fs::path>());
	full_path = fs::system_complete(fs::path(InputDir));

	SVec dirs, others;
	unsigned long file_count = 0;
	unsigned long dir_count = 0;
	unsigned long other_count = 0;
	unsigned long err_count = 0;

	// Directory error
	if (!fs::exists(full_path))
	{
		//std::cout << "\nNot found: " << full_path.string() << std::endl;
		return false;
	}

	else if (fs::is_directory(full_path))
	{
		/*std::cout << "\nIn directory: "
			<< full_path.string() << "\n\n";*/
		fs::directory_iterator end_iter;
		for (fs::directory_iterator dir_itr(full_path);
		dir_itr != end_iter;
			++dir_itr)
		{
			try
			{
				if (fs::is_directory(dir_itr->status()))
				{
					++dir_count;
					//std::cout << dir_itr->path().filename() << " [directory]\n";
					dirs.push_back(dir_itr->path().filename().string());
				}
				else if (fs::is_regular_file(dir_itr->status()))
				{
					++file_count;
					//std::cout << dir_itr->path().filename() << "\n";
					(*FileList).push_back(dir_itr->path().filename().string());
				}
				else
				{
					++other_count;
					//std::cout << dir_itr->path().filename() << " [other]\n";
					others.push_back(dir_itr->path().filename().string());
				}

			}
			catch (const std::exception & ex)
			{
				++err_count;
				//std::cout << dir_itr->path().filename() << " " << ex.what() << std::endl;
			}
		}
		/*std::cout << "\n" << file_count << " files\n"
			<< dir_count << " directories\n"
			<< other_count << " others\n"
			<< err_count << " errors\n";*/
		return true;
	}
}

bool GetFileandDir(std::string InputDir, SVec *FileList, SVec *dirs)
{
	fs::path full_path(fs::initial_path<fs::path>());
	full_path = fs::system_complete(fs::path(InputDir));

	SVec others;
	unsigned long file_count = 0;
	unsigned long dir_count = 0;
	unsigned long other_count = 0;
	unsigned long err_count = 0;

	// Directory error
	if (!fs::exists(full_path))
	{
		std::cout << "\nNot found: " << full_path.string() << std::endl;
		return false;
	}

	else if (fs::is_directory(full_path))
	{
		std::cout << "\nIn directory: "
			<< full_path.string() << "\n\n";
		fs::directory_iterator end_iter;
		for (fs::directory_iterator dir_itr(full_path);
		dir_itr != end_iter;
			++dir_itr)
		{
			try
			{
				if (fs::is_directory(dir_itr->status()))
				{
					++dir_count;
					//std::cout << dir_itr->path().filename() << " [directory]\n";
					(*dirs).push_back(dir_itr->path().filename().string());
				}
				else if (fs::is_regular_file(dir_itr->status()))
				{
					++file_count;
					//std::cout << dir_itr->path().filename() << "\n";
					(*FileList).push_back(dir_itr->path().filename().string());
				}
				else
				{
					++other_count;
					//std::cout << dir_itr->path().filename() << " [other]\n";
					others.push_back(dir_itr->path().filename().string());
				}

			}
			catch (const std::exception & ex)
			{
				++err_count;
				std::cout << dir_itr->path().filename() << " " << ex.what() << std::endl;
			}
		}
		/*std::cout << "\n" << file_count << " files\n"
			<< dir_count << " directories\n"
			<< other_count << " others\n"
			<< err_count << " errors\n";*/
		return true;
	}
}

void elimVerboseF(SVec *Filelist, std::string CamID)
{
	std::vector<size_t> eraseIdx;
	size_t idx = 0;
	size_t first_dot, second_dot, third_dot;

	for (auto it = Filelist->begin(); it != Filelist->end(); ++it)
	{
		first_dot = it->find_first_of('.');
		second_dot = it->find_first_of('.', first_dot + 1);
		third_dot = it->find_first_of('.', second_dot + 1);
		if (first_dot != std::string::npos && second_dot != std::string::npos && third_dot != std::string::npos)
		{
			if (CamID != "")
			{
				if ((CamID == "c50" || CamID == "c51") && third_dot - second_dot == 4)
					break;
				else if (CamID != "c50" && CamID != "c51" && third_dot - second_dot == 3)
					break;
			}
			else
				break;
		}
	}

	// Search for vdo extension and eliminate file with idx string
	for (auto it = Filelist->begin(); it != Filelist->end(); ++it)
	{
		if (CamID != "")
		{
			if ((it->find("vdo") == std::string::npos) || (it->find("vdo") != std::string::npos && it->find("idx") != std::string::npos) ||
				it->substr(second_dot + 1, third_dot - second_dot - 1) != CamID)
				eraseIdx.push_back(idx);
		}
		else
		{
			if ((it->find("vdo") == std::string::npos) || (it->find("vdo") != std::string::npos && it->find("idx") != std::string::npos))
				eraseIdx.push_back(idx);
		}
		idx++;
	}
	idx = 0;
	for (auto it = eraseIdx.begin(); it != eraseIdx.end(); ++it)
	{
		size_t n = *it - idx;
		Filelist->erase(Filelist->begin() + n);
		idx++;
	}

}


void elimVDOs(SVec *Filelist)
{
	std::vector<size_t> eraseIdx;
	size_t idx = 0;

	// Eliminate files with vdo extension
	for (auto it = Filelist->begin(); it != Filelist->end(); ++it)
	{
		if ((it->find("vdo") != std::string::npos && it->find("idx") == std::string::npos))
			eraseIdx.push_back(idx);
		idx++;
	}
	idx = 0;
	for (auto it = eraseIdx.begin(); it != eraseIdx.end(); ++it)
	{
		size_t n = *it - idx;
		Filelist->erase(Filelist->begin() + n);
		idx++;
	}
}

void GetIdxFilefromNonVdoFile(SVec *Filelist, std::string CamID)
{
	std::vector<size_t> eraseIdx;
	size_t idx = 0;
	size_t first_dot, second_dot, third_dot;

	for (auto it = Filelist->begin(); it != Filelist->end(); ++it)
	{
		first_dot = it->find_first_of('.');
		second_dot = it->find_first_of('.', first_dot + 1);
		third_dot = it->find_first_of('.', second_dot + 1);
		if (first_dot != std::string::npos && second_dot != std::string::npos && third_dot != std::string::npos)
		{
			if ((CamID == "c50" || CamID == "c51") && third_dot - second_dot == 4)
				break;
			else if (CamID != "c50" && CamID != "c51" && third_dot - second_dot == 3)
				break;
		}
	}

	// Eliminate files without CamID
	for (auto it = Filelist->begin(); it != Filelist->end(); ++it)
	{
		if ((it->find("idx") == std::string::npos) || it->substr(second_dot + 1, third_dot - second_dot - 1) != CamID)
			eraseIdx.push_back(idx);
		idx++;
	}
	idx = 0;
	for (auto it = eraseIdx.begin(); it != eraseIdx.end(); ++it)
	{
		size_t n = *it - idx;
		Filelist->erase(Filelist->begin() + n);
		idx++;
	}

}
int countAsterisk(std::string inString)
{
	int n = (int)std::count(inString.begin(), inString.end(), '*');
	return n;
}

bool existAsterisk(std::string inString)
{
	std::size_t found = inString.find('*');
	if (found != std::string::npos)
		return true;
	else
		return false;
}

SVec Clear1Asterisk(std::string inString)
{
	SVec subStrings;
	if (inString.find_first_of('*') == 0)
		subStrings.push_back(inString.substr(1, std::string::npos));
	else
	{
		size_t n = inString.find_first_of('*');
		subStrings.push_back(inString.substr(0, n));
		subStrings.push_back(inString.substr(n + 1, inString.size() - n - 1));
	}
	return subStrings;
}

// For two *, we assume that the first char is *
SVec Clear2Asterisk(std::string inString)
{
	SVec subStrings;
	std::string sub1, sub2;
	size_t firstA = inString.find_first_of('*');
	size_t secondA = inString.find_last_of('*');
	sub1 = inString.substr(firstA + 1, secondA - firstA - 1);
	sub2 = inString.substr(secondA + 1, inString.size() - sub1.size() - 2);
	subStrings.push_back(sub1);
	subStrings.push_back(sub2);
	return subStrings;
}

void CatalogFile(std::vector<SVec> *FCatalog, SVec Filelist)
{
	for (auto it = Filelist.begin(); it != Filelist.end(); ++it)
	{
		size_t Ssize = it->size();
		if ((*it).substr(Ssize - 6, 2).compare("60") == 0)
			FCatalog->at(0).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("61") == 0)
			FCatalog->at(1).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("62") == 0)
			FCatalog->at(2).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("64") == 0)
			FCatalog->at(3).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("65") == 0)
			FCatalog->at(4).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("70") == 0)
			FCatalog->at(5).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("71") == 0)
			FCatalog->at(6).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("72") == 0)
			FCatalog->at(7).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("74") == 0)
			FCatalog->at(8).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("75") == 0)
			FCatalog->at(9).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("50") == 0)
			FCatalog->at(10).push_back(*it);
		else if ((*it).substr(Ssize - 6, 2).compare("51") == 0)
			FCatalog->at(11).push_back(*it);
	}
}

bool copyDir(
	boost::filesystem::path const & source,
	boost::filesystem::path const & destination
	)
{
	try
	{
		// Check whether the function call is valid
		if (
			!fs::exists(source) ||
			!fs::is_directory(source)
			)
		{
			std::cerr << "Source directory " << source.string()
				<< " does not exist or is not a directory." << '\n'
				;
			return false;
		}
		if (fs::exists(destination))
		{
			std::cerr << "Destination directory " << destination.string()
				<< " already exists." << '\n'
				;
			return false;
		}
		// Create the destination directory
		if (!fs::create_directory(destination))
		{
			std::cerr << "Unable to create destination directory"
				<< destination.string() << '\n'
				;
			return false;
		}
	}
	catch (fs::filesystem_error const & e)
	{
		std::cerr << e.what() << '\n';
		return false;
	}
	// Iterate through the source directory
	for (
		fs::directory_iterator file(source);
		file != fs::directory_iterator(); ++file
		)
	{
		try
		{
			fs::path current(file->path());
			if (fs::is_directory(current))
			{
				// Found directory: Recursion
				if (
					!copyDir(
						current,
						destination / current.filename()
						)
					)
				{
					return false;
				}
			}
			else
			{
				// Found file: Copy
				fs::copy_file(
					current,
					destination / current.filename()
					);
			}
		}
		catch (fs::filesystem_error const & e)
		{
			std::cerr << e.what() << '\n';
		}
	}
	return true;
}

void SortCatalog(std::vector<SVec> *FCatalog)
{
	for (auto it = FCatalog->begin(); it != FCatalog->end(); ++it)
	{
		if (it->size() != 0)
			std::sort(it->begin(), it->end());
	}
}

int getFilelist(std::string dir, std::string CamID, std::string &directory, SVec &Filelist)
{
	int numAsterisk, tag;
	SVec DirplusFile;
	std::string f;
	std::vector<size_t> eraseIdx;
	fs::path full_path(fs::initial_path<fs::path>());
	full_path = fs::system_complete(fs::path(dir));

	// If the given command argument is not an existing path
	if (!fs::exists(full_path))
	{
		// Command argument is directory + file name
		const size_t last_slash_idx = dir.find_last_of("\\/");
		if (std::string::npos != last_slash_idx)
		{
			directory = dir.substr(0, last_slash_idx + 1); // Get the directory
			f = dir.substr(last_slash_idx + 1, dir.size() - last_slash_idx - 1); // Get the file name
																				 //filename.erase(0, last_slash_idx + 1); // Get the file name
		}
		else
			directory = dir; // Get the directory
							 // Search file in the given directory
		bool Getfile = GetFileInDir(directory, &Filelist);
		if (!Getfile)
		{
			std::cout << "Directory or file does not exist!" << std::endl;
			//system("PAUSE");
			return 0;
		}

		// Check * existance
		if (existAsterisk(f) && Filelist.size() != 0)
		{
			numAsterisk = countAsterisk(f);
			if (numAsterisk == 1)
			{
				SVec subStrings = Clear1Asterisk(f);
				tag = 0;
				for (auto itF = Filelist.begin(); itF != Filelist.end(); ++itF)
				{
					for (auto i = subStrings.begin(); i != subStrings.end(); ++i)
					{
						if ((*itF).find((*i)) == std::string::npos) // subString not found
						{
							eraseIdx.push_back(tag);
							break;
						}
					}
					tag++;
				}
				tag = 0;
				for (auto it = eraseIdx.begin(); it != eraseIdx.end(); ++it)
				{
					size_t n = *it - tag;
					Filelist.erase(Filelist.begin() + n);
					tag++;
				}
			}
			else if (numAsterisk == 2)
			{
				SVec subStrings = Clear2Asterisk(f);
				tag = 0;
				for (auto itF = Filelist.begin(); itF != Filelist.end(); ++itF)
				{
					for (auto i = subStrings.begin(); i != subStrings.end(); ++i)
					{
						if ((*itF).find((*i)) == std::string::npos) // subString not found
						{
							eraseIdx.push_back(tag);
							break;
						}
					}
					tag++;
				}
				tag = 0;
				for (auto it = eraseIdx.begin(); it != eraseIdx.end(); ++it)
				{
					size_t n = *it - tag;
					Filelist.erase(Filelist.begin() + n);
					tag++;
				}
			}
			elimVerboseF(&Filelist, CamID);
			for (size_t it = 0; it < Filelist.size(); ++it)
				DirplusFile.push_back(directory + Filelist.at(it));
		}
		else if (!existAsterisk(f) || Filelist.size() == 0)
		{
			std::cout << "\nNot found: " << dir << std::endl;
			return 0;
		}
	}

	// If the given command argument is a directory
	else if (fs::is_directory(full_path))
	{
		// Search for files in the directory, only keep the ones with vdo extension and without idx in the file name
		GetFileInDir(dir, &Filelist);
		elimVerboseF(&Filelist, CamID);
		directory = dir;
		for (size_t it = 0; it < Filelist.size(); ++it)
			DirplusFile.push_back(directory + Filelist.at(it));
		if (Filelist.size() == 0)
		{
			std::cout << "No vdo files exist in the directory!" << std::endl;
			return 0;
		}
	}

	// Must be a file
	else
	{
		// Command argument is directory + file name
		const size_t last_slash_idx = full_path.string().find_last_of("\\/");
		if (std::string::npos != last_slash_idx)
		{
			directory = full_path.string().substr(0, last_slash_idx + 1); // Get the directory
			f = full_path.string().substr(last_slash_idx + 1, full_path.string().size() - last_slash_idx - 1); // Get the file name
																											   //filename.erase(0, last_slash_idx + 1); // Get the file name
		}
		Filelist.push_back(f);
		DirplusFile.push_back(full_path.string());
	}
}

int getOdoRange(std::string dir, std::string CamID, long int &odo_min, long int &odo_max)
{
	std::string directory;
	SVec VDOFiles, idx_file_list;
	long int odo_limit_max = std::numeric_limits<long>::max(), odo_min_temp;
	Indexer_s *indexer_end = NULL;
	fs::path idx_file;
	getFilelist(dir, CamID, directory, VDOFiles);
	std::sort(VDOFiles.begin(), VDOFiles.end());

	int l_totlen;
	FILE * VideoFile = NULL;
	size_t l_HeaderSize = sizeof(infelHd_s);
	size_t l_VideoDataSize = 0;
	size_t l_DataReadSize = 0;

	char *l_HeaderData = (char*)malloc(l_HeaderSize);
	char *l_VideoData = (char*)malloc(0x400000); //about 4MB

	infelHd_s * l_Header = NULL;
	Video_d_s *l_Video = NULL;


	// Begin to read the first and last VDO file
	// Open the first vdo file
	VideoFile = fopen((directory + '\\' + VDOFiles.at(0)).c_str(), "rb");
	for (int i = 0; i < 2; ++i)
	{
		l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, VideoFile);
        // if the vdo data is empty
		if (l_DataReadSize < l_HeaderSize)
		{
			odo_min = odo_max = 0;
			return 1;
		}
		l_Header = (infelHd_s *)l_HeaderData;
		l_totlen = l_Header->totlen;
		l_VideoDataSize = l_totlen - l_HeaderSize;

		l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, VideoFile);
		l_Video = (Video_d_s *)l_VideoData;
		if (l_Header->infid == VIDEO_FIF)
		{
			if (i == 0)
				odo_min_temp = l_Video->St.Odom;
			if ((odo_min_temp - l_Video->St.Odom) > 50)
				odo_min = l_Video->St.Odom;
			else
				odo_min = odo_min_temp;
			//std::cout << "Odometer of 1. file, first value: " << odo_min << std::endl;
		}
	}
	fclose(VideoFile);


	GetFileInDir(dir, &idx_file_list);
	elimVDOs(&idx_file_list);
	GetIdxFilefromNonVdoFile(&idx_file_list, CamID);
	if (idx_file_list.size() == 1)
	{
		fs::path d(dir), idx_f(idx_file_list.at(0));
		idx_file = d / idx_f;
	}
	else
	{
		std::cout << "number of idx file exceeds 1!" << std::endl;
		return -1;
	}
	// read idx file
	indexer_end = get_indexer_from_given_odo(odo_limit_max, idx_file.string(), 0);

	// Open the last vdo file
	VideoFile = fopen((directory + '\\' + VDOFiles.at(VDOFiles.size() - 1)).c_str(), "rb");
	// in case certain vdo files missing at the end
	if (VDOFiles.size() == indexer_end->filePart + 1)
		fseek(VideoFile, indexer_end->byteOffset, SEEK_CUR);

	while (feof(VideoFile) == 0)
	{
		while (1)
		{
			unsigned char c;
			while ((c = std::fgetc(VideoFile)) != 'd' && feof(VideoFile) == 0) {}
			if (feof(VideoFile) != 0)
				break;
			fseek(VideoFile, -1, SEEK_CUR);
			l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, VideoFile);
			l_Header = (infelHd_s *)l_HeaderData;
			if (l_Header->infid != VIDEO_FIF)
				continue;
			else
				break;
		}
		l_totlen = l_Header->totlen;
		l_VideoDataSize = l_totlen - l_HeaderSize;
		l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, VideoFile);
		l_Video = (Video_d_s *)l_VideoData;
	}
	if (l_Header->infid == VIDEO_FIF)
	{
		odo_max = l_Video->St.Odom;
		//std::cout << "Odometer of " << VDOFiles.size() << ". file, first value: " << odo_max << std::endl;
	}
	fclose(VideoFile);
	// Close the last VDO file

	free(l_HeaderData);
	free(l_VideoData);
	free(indexer_end);
	return 1;

}

int ImOutVDORange(long int Start, long int End, SVec *VDOFIles, std::string directory, bool pano_all_export, double Uncertainty)
{
	// Get the internal counter at the beginning of the first and last vdo file
	int IntFirstVDO, IntLastVDO;
	double FirstVDOIdx, LastVDOIdx;
	int NumIntPFile;
	int l_totlen;
	SVec Temp;
	FILE * VideoFile = NULL;
	size_t l_HeaderSize = sizeof(infelHd_s);
	size_t l_VideoDataSize = 0;
	size_t l_DataReadSize = 0;

	char *l_HeaderData = (char*)malloc(l_HeaderSize);
	char *l_VideoData = (char*)malloc(0x400000); //about 4MB

	infelHd_s * l_Header = NULL;
	Video_d_s *l_Video = NULL;
	Format *F = NULL;

	// There is only one VDO file
	if (VDOFIles->size() == 1)
	{
		Temp.push_back(VDOFIles->at(0));
		VDOFIles->clear();
		*VDOFIles = Temp;
	}

	else if (VDOFIles->size() > 1 && pano_all_export)
	{
	}
	// There is more than one VDO file
	else if (VDOFIles->size() > 1 && !pano_all_export)
	{
		// Begin to read the first and last VDO file
		// Open the first vdo file
		VideoFile = fopen((directory + '\\' + VDOFIles->at(0)).c_str(), "rb");
		l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, VideoFile);
		l_Header = (infelHd_s *)l_HeaderData;
		l_totlen = l_Header->totlen;
		l_VideoDataSize = l_totlen - l_HeaderSize;

		l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, VideoFile);
		l_Video = (Video_d_s *)l_VideoData;
		IntFirstVDO = l_Video->St.Odom;
		std::cout << "Odometer of 1. file, first value: " << IntFirstVDO << std::endl;
		fclose(VideoFile);
		// Open the last vdo file
		VideoFile = fopen((directory + '\\' + VDOFIles->at(VDOFIles->size() - 1)).c_str(), "rb");
		while (1)
		{
			unsigned char c; // note: int, not char, required to handle EOF
			while ((c = std::fgetc(VideoFile)) != 'd' && feof(VideoFile) == 0) {}
			if (feof(VideoFile) != 0)
				break;
			fseek(VideoFile, -1, SEEK_CUR);
			l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, VideoFile);
			l_Header = (infelHd_s *)l_HeaderData;
			if (l_Header->infid != VIDEO_FIF)
				continue;
			else
				break;
		}
		l_totlen = l_Header->totlen;
		l_VideoDataSize = l_totlen - l_HeaderSize;
		l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, VideoFile);
		l_Video = (Video_d_s *)l_VideoData;
		IntLastVDO = l_Video->St.Odom;
		std::cout << "Odometer of " << VDOFIles->size() << ". file, first value: " << IntLastVDO << std::endl;
		fclose(VideoFile);
		// Close the last VDO file

		NumIntPFile = (IntLastVDO - IntFirstVDO) / (int)(VDOFIles->size() - 1);
		if (Start >= IntFirstVDO && Start < IntLastVDO)
		{
			FirstVDOIdx = (double)(Start - IntFirstVDO) / (double)NumIntPFile;
			// 0.8 Uncertainty
			if ((int)(FirstVDOIdx - Uncertainty) < int(FirstVDOIdx))
				FirstVDOIdx = (int)FirstVDOIdx - 1;
			else
				FirstVDOIdx = (int)FirstVDOIdx;
		}
		else if (Start >= IntLastVDO)
		{
			/*// We use 1.2 to make sure that the Start internal counter is in or out
			if (Start - IntLastVDO > 1.2 * NumIntPFile)
			return 0;
			else
			FirstVDOIdx = (double)VDOFIles->size() - 1;*/
			FirstVDOIdx = (double)VDOFIles->size() - 1;
		}
		else if (Start < IntFirstVDO)
			return 0;


		if (End >= IntFirstVDO && End < IntLastVDO)
		{
			LastVDOIdx = (double)(End - IntFirstVDO) / (double)NumIntPFile;
			if ((int)(LastVDOIdx + Uncertainty) > int(LastVDOIdx))
				LastVDOIdx = (int)LastVDOIdx + 1;
			else
				LastVDOIdx = (int)LastVDOIdx;
		}
		else if (End >= IntLastVDO)
		{
			/*// We use 1.2 to make sure that the End internal counter is in or out
			if (End - IntLastVDO > 1.2 * NumIntPFile)
			return 0;
			else
			LastVDOIdx = (double)VDOFIles->size() - 1;*/
			LastVDOIdx = (double)VDOFIles->size() - 1;
		}
		else if (End < IntFirstVDO)
			return 0;

		// Determine VDO files range for output images
		if (FirstVDOIdx != LastVDOIdx)
		{
			std::cout << "Using files: ";
			for (int it = (int)FirstVDOIdx; it < LastVDOIdx + 1; ++it)
			{
				Temp.push_back(VDOFIles->at(it));
				std::cout << VDOFIles->at(it) << ", ";
			}
			std::cout << std::endl;
		}
		else
		{
			Temp.push_back(VDOFIles->at((int)FirstVDOIdx));
			std::cout << "Using file: " << VDOFIles->at((int)FirstVDOIdx) << std::endl;
		}
		VDOFIles->clear();
		*VDOFIles = Temp;
	}

	free(l_HeaderData);
	free(l_VideoData);
	return 1;

}

/******************************************************************
* DECOMPRESSION
******************************************************************/

static  unsigned char CLAMP(short a_X) { return  ((a_X > 255) ? 255 : (a_X < 0) ? 0 : a_X); }

bool locogio_init(locogio_s *a_Loco, int a_Length, int a_Color, int a_Bsize, int a_Subsample)
{
	if (!a_Loco) return false;

	a_Loco->length = a_Length;
	if (a_Subsample == -1)
	{
		if (a_Color)
		{
			a_Subsample = 1;
		}
		else
		{
			a_Subsample = 0;
		}
	}
	else
	{
		a_Loco->subsample = a_Subsample;
	}
	a_Loco->color = a_Color;
	a_Loco->cblock_size = a_Bsize;
	a_Loco->dif = (yuv_dif_t*)malloc(2 * a_Length*sizeof(yuv_dif_t));
	a_Loco->yuv = (yuv_t*)malloc(2 * a_Length*sizeof(yuv_t));
	//loco->cbuffer = (unsigned char*)malloc(length*6);

	if (a_Color) {
		a_Loco->lenght_bsh = 12;
	}
	else {
		a_Loco->lenght_bsh = 4;
	}

	if (a_Loco->dif == NULL) {
		return false;
	}
	if (a_Loco->yuv == NULL) {
		return false;
	}

	return true;
}

template <typename T> int locogio_decompress_line_meta(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType,
	std::vector<std::vector<T>> *VideoData, int OutputOption)
{
	int l_Y, l_Cr, l_Cb;
	int l_Yo = 0, l_Cro = 0, l_Cbo = 0;
	a_Loco->cbuffer = a_Cline;
	a_Loco->compress_size = a_CompressSize;
	a_Loco->cbuffer_bit_ptr = 0;
	a_Loco->cbuffer_ptr = 0;
	// DECOMPRESSION
	decompress(a_Loco, a_CompressSize);

	// Restore diffs
	for (unsigned int x = 0; x<a_Loco->length; x++)
	{
		l_Y = a_Loco->dif[x].dy + l_Yo;
		l_Cr = a_Loco->dif[x].du + l_Cro;
		l_Cb = a_Loco->dif[x].dv + l_Cbo;

		l_Yo = l_Y;
		l_Cro = l_Cr;
		l_Cbo = l_Cb;

		a_Loco->yuv[x].y = l_Y;
		a_Loco->yuv[x].cr = l_Cr;
		a_Loco->yuv[x].cb = l_Cb;
	}

	// Output a_Out array as YUV(decompressed)
	std::vector<T> Frametemp;
	if (a_Loco->color && OutputOption == 2)
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			Frametemp.push_back((T)a_Loco->yuv[x].y);
			Frametemp.push_back((T)a_Loco->yuv[x].cr);
			Frametemp.push_back((T)a_Loco->yuv[x].cb);
		}
		(*VideoData).push_back(Frametemp);
	}
	else if (!a_Loco->color && OutputOption == 2)
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			Frametemp.push_back((T)a_Loco->yuv[x].y);
		}
		(*VideoData).push_back(Frametemp);
	}

	// YUV to RGB
	if (a_Loco->color)
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			int l_Y, l_Cr, l_Cb;
			int l_R, l_G, l_B;

			l_Y = a_Loco->yuv[x].y;
			l_Cr = a_Loco->yuv[x].cr;
			l_Cb = a_Loco->yuv[x].cb;

			l_G = l_Y - (77 * l_Cr + 25 * l_Cb) / 256;
			l_R = (l_Y + l_Cr);
			l_B = (l_Y + l_Cb);

			a_Out[x * 3] = CLAMP(l_R);
			if (a_Loco->color)
			{
				a_Out[x * 3 + 1] = CLAMP(l_G);
				a_Out[x * 3 + 2] = CLAMP(l_B);
			}

		}

		// Output a_Out array as RGB(decompressed)
		if (OutputOption == 1)
			(*VideoData).push_back(std::vector<T>(a_Out, a_Out + 3 * a_Loco->length));

	}

	else
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			a_Out[x] = CLAMP(a_Loco->yuv[x].y);
			/*image1.at<unsigned char>(0, x) = a_Out[x];*/
		}
		// Output a_Out array as RGB(decompressed)
		if (OutputOption == 1)
			(*VideoData).push_back(std::vector<T>(a_Out, a_Out + a_Loco->length));
	}

	return 0;
}

cv::Mat locogio_decompress_line(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize, cv::Mat &image,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType)
{
	int l_Y, l_Cr, l_Cb;
	int l_Yo = 0, l_Cro = 0, l_Cbo = 0;
	cv::Mat image1;
	if (ImType == IMAGE_GDM_LINEAR_COLOR)
		image1.create(1, a_Loco->length, CV_8UC3);
	else if (ImType == IMAGE_GDM_LINEAR_BW)
		image1.create(1, a_Loco->length, CV_8UC1);
	a_Loco->cbuffer = a_Cline;
	a_Loco->compress_size = a_CompressSize;
	a_Loco->cbuffer_bit_ptr = 0;
	a_Loco->cbuffer_ptr = 0;
	// DECOMPRESSION
	decompress(a_Loco, a_CompressSize);

	// Restore diffs

	for (unsigned int x = 0; x<a_Loco->length; x++)
	{
		l_Y = a_Loco->dif[x].dy + l_Yo;
		l_Cr = a_Loco->dif[x].du + l_Cro;
		l_Cb = a_Loco->dif[x].dv + l_Cbo;

		l_Yo = l_Y;
		l_Cro = l_Cr;
		l_Cbo = l_Cb;

		a_Loco->yuv[x].y = l_Y;
		a_Loco->yuv[x].cr = l_Cr;
		a_Loco->yuv[x].cb = l_Cb;
	}

	// YUV to RGB
	if (a_Loco->color)
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			int l_Y, l_Cr, l_Cb;
			int l_R, l_G, l_B;

			l_Y = a_Loco->yuv[x].y;
			l_Cr = a_Loco->yuv[x].cr;
			l_Cb = a_Loco->yuv[x].cb;

			l_G = l_Y - (77 * l_Cr + 25 * l_Cb) / 256;
			l_R = (l_Y + l_Cr);
			l_B = (l_Y + l_Cb);

			a_Out[x * 3] = CLAMP(l_R);
			if (a_Loco->color)
			{
				a_Out[x * 3 + 1] = CLAMP(l_G);
				a_Out[x * 3 + 2] = CLAMP(l_B);
			}
			// Write RGB values to CV Mat BGR
			image1.at<cv::Vec3b>(0, x)[0] = a_Out[x * 3 + 2];
			image1.at<cv::Vec3b>(0, x)[1] = a_Out[x * 3 + 1];
			image1.at<cv::Vec3b>(0, x)[2] = a_Out[x * 3];
		}

		if (DecompandSaveIm)
		{
			std::ostringstream jname;
			if (fs::is_directory(log_path + '/' + CamID))
				Jdir_created = true;
			if (!Jdir_created)
			{
				fs::path jpegdir(log_path + '/' + CamID);
				fs::create_directories(jpegdir);
				Jdir_created = true;
			}
			jname << log_path << '/' << CamID << '/' << NumBlocks << ".jpg";
			image.push_back(image1);
		}
	}

	else
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			a_Out[x] = CLAMP(a_Loco->yuv[x].y);
			image1.at<unsigned char>(0, x) = a_Out[x];
		}
		if (DecompandSaveIm)
		{
			std::ostringstream jname;
			if (fs::is_directory(log_path + '/' + CamID))
				Jdir_created = true;
			if (!Jdir_created)
			{
				fs::path jpegdir(log_path + '/' + CamID);
				fs::create_directories(jpegdir);
				Jdir_created = true;
			}
			jname << log_path << '/' << CamID << '/' << NumBlocks << ".jpg";
			image.push_back(image1);
		}
	}

	return image1;
}

static unsigned char read_bits(struct locogio_s *a_Loco, int l_Bits, bool l_SignExt)
{
	unsigned char l_Tmp = 0;
	unsigned char l_Byte;
	unsigned char l_Bit;
	bool l_SignIsNegative = false;

	for (int i = 0; i < l_Bits; i++)
	{
		int mask = 0x1 << a_Loco->cbuffer_bit_ptr;

		l_Tmp <<= 1;

		l_Byte = *(a_Loco->cbuffer + a_Loco->cbuffer_ptr);
		if (l_Byte & mask)
		{
			l_Bit = 1;
			if (i == 0)
				l_SignIsNegative = true;
		}
		else
			l_Bit = 0;

		a_Loco->cbuffer_bit_ptr -= 1;
		if (a_Loco->cbuffer_bit_ptr == -1)
		{
			a_Loco->cbuffer_bit_ptr = 7;
			a_Loco->cbuffer_ptr++;
		}

		l_Tmp |= l_Bit;
	}

	if (l_SignIsNegative && l_SignExt)
	{
		int mask = 0x80;
		for (int i = 7; i > 0; i--)
		{
			if (l_Tmp & mask)
				break;
			else
				l_Tmp |= mask;

			mask >>= 1;
		}
	}

	return l_Tmp;
}


static void read_bsh(struct locogio_s *a_Loco, struct locogio_bh_s &a_Bsh)
{
	a_Bsh.bsy = read_bits(a_Loco, 4, false);
	if (a_Loco->color)
	{
		a_Bsh.bsu = read_bits(a_Loco, 4, false);
		a_Bsh.bsv = read_bits(a_Loco, 4, false);
	}
}

static void decompress(locogio_s *a_Loco, int a_LengthBits)
{
	struct locogio_bh_s l_Bsh;
	yuv_dif_t           l_Value;
	yuv_dif_t          *l_YdimgPtr;
	unsigned int        l_Pixcnt = 0;

	a_Loco->cbuffer_bit_ptr = 7;
	a_Loco->cbuffer_ptr = 0;
	a_Loco->compress_size = a_LengthBits;

	l_YdimgPtr = a_Loco->dif;
	while (1)
	{
		if (a_LengthBits < a_Loco->lenght_bsh)
			break;

		read_bsh(a_Loco, l_Bsh);
		a_LengthBits -= a_Loco->lenght_bsh;

		for (int i = 0; i < a_Loco->cblock_size; i++)
		{
			if (l_Bsh.bsy)
			{
				l_Value.dy = read_bits(a_Loco, l_Bsh.bsy, true);
				a_LengthBits -= l_Bsh.bsy;
			}
			else
				l_Value.dy = 0;

			l_YdimgPtr[i].dy = l_Value.dy;

			if (a_Loco->color)
			{
				if (a_Loco->subsample == 0)
				{
					if (l_Bsh.bsu)
					{
						l_Value.du = read_bits(a_Loco, l_Bsh.bsu, true);
						a_LengthBits -= l_Bsh.bsu;
					}
					else
						l_Value.du = 0;

					l_YdimgPtr[i].du = l_Value.du;

					if (l_Bsh.bsv)
					{
						l_Value.dv = read_bits(a_Loco, l_Bsh.bsv, true);
						a_LengthBits -= l_Bsh.bsv;
					}
					else
						l_Value.dv = 0;

					l_YdimgPtr[i].dv = l_Value.dv;
				}
				else
				{
					if (i%SUBSAMPLE_SIZE == 0)
					{
						if (l_Bsh.bsu)
						{
							l_Value.du = read_bits(a_Loco, l_Bsh.bsu, true);
							a_LengthBits -= l_Bsh.bsu;
						}
						else
							l_Value.du = 0;

						l_YdimgPtr[i].du = l_Value.du;

						if (l_Bsh.bsv)
						{
							l_Value.dv = read_bits(a_Loco, l_Bsh.bsv, true);
							a_LengthBits -= l_Bsh.bsv;
						}
						else
							l_Value.dv = 0;

						l_YdimgPtr[i].dv = l_Value.dv;
					}
					else
					{
						l_YdimgPtr[i].du = 0;
						l_YdimgPtr[i].dv = 0;
					}
				}
			}
			else
			{
				l_YdimgPtr[i].du = 0;
				l_YdimgPtr[i].dv = 0;
			}
		}
		l_Pixcnt += a_Loco->cblock_size;
		l_YdimgPtr += a_Loco->cblock_size;
	}
}


/******************************************************************
* COMPRESSION
******************************************************************/

int locogio_compress_line(locogio_s *a_Loco, unsigned char *a_Line, unsigned char *l_Out)
{
	a_Loco->cbuffer = l_Out;
	a_Loco->cbuffer_bit_ptr = 0;
	a_Loco->cbuffer_ptr = 0;

	// RGB to YUV conversion
	if (a_Loco->color)
	{
		for (unsigned int i = 0; i<a_Loco->length; i++)
		{
			short l_R, l_G, l_B;
			short l_Y, l_U, l_V;

			l_R = ((short)a_Line[i * 3]) & 0xFF;
			l_G = ((short)a_Line[i * 3 + 1]) & 0xFF;
			l_B = ((short)a_Line[i * 3 + 2]) & 0xFF;

			l_Y = (55 * l_R + 183 * l_G + 18 * l_B) / 256;
			l_U = l_R - l_Y;
			l_V = l_B - l_Y;

			if (l_U > 127)
			{
				l_U = 127;
			}
			if (l_U < -126)
			{
				l_U = -126;
			}
			if (l_V < -126)
			{
				l_V = -126;
			}

			a_Loco->yuv[i].y = l_Y;
			a_Loco->yuv[i].cr = l_U;
			a_Loco->yuv[i].cb = l_V;
		}

		if (a_Loco->subsample)
		{
			// sub-sampling 4:1:1
			for (unsigned int i = 0; i<a_Loco->length; i += 4)
			{
				int l_MeanCR = 0;
				int l_MeanCB = 0;
				for (int j = 0; j<4; j++)
				{
					l_MeanCR += a_Loco->yuv[i + j].cr;
					l_MeanCB += a_Loco->yuv[i + j].cb;
				}
				for (int j = 0; j<4; j++)
				{
					a_Loco->yuv[i + j].cr = l_MeanCR / 4;
					a_Loco->yuv[i + j].cb = l_MeanCB / 4;
				}
			}
		}
	}
	else
	{
		for (unsigned int i = 0; i<a_Loco->length; i++)
		{
			a_Loco->yuv[i].y = a_Line[i];
			a_Loco->yuv[i].cb = 0;
			a_Loco->yuv[i].cr = 0;
		}
	}

	// Calculate diffs
	{
		int l_Y, l_CR, l_CB;
		int l_Y0 = 0, l_CR0 = 0, l_CB0 = 0;

		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			l_Y = a_Loco->yuv[x].y;
			l_CR = a_Loco->yuv[x].cr;
			l_CB = a_Loco->yuv[x].cb;

			a_Loco->dif[x].dy = l_Y - l_Y0;
			a_Loco->dif[x].du = l_CR - l_CR0;
			a_Loco->dif[x].dv = l_CB - l_CB0;

			l_Y0 = l_Y;
			l_CR0 = l_CR;
			l_CB0 = l_CB;
		}
	}

	// compression
	int l_Length;
	l_Length = compress(a_Loco);

	return l_Length;
}

static void push_bits(locogio_s *l_Loco, unsigned char *l_Value, int l_Bits)
{
	unsigned int l_Mask;

	l_Mask = (0x1 << (l_Bits - 1));
	for (int i = 0; i < l_Bits; i++)
	{
		int l_Bit;
		if (*l_Value&l_Mask)
		{
			l_Bit = 1;
		}
		else {
			l_Bit = 0;
		}

		l_Bit <<= l_Loco->cbuffer_bit_ptr;
		*(l_Loco->cbuffer + l_Loco->cbuffer_ptr) |= l_Bit;

		l_Loco->cbuffer_bit_ptr--;
		if (l_Loco->cbuffer_bit_ptr == -1)
		{
			l_Loco->cbuffer_bit_ptr = 7;
			l_Loco->cbuffer_ptr++;

			*(l_Loco->cbuffer + l_Loco->cbuffer_ptr) = 0;
		}

		l_Mask >>= 1;
	}

	l_Loco->compress_size += l_Bits;
}

static void push_bsh(locogio_s *l_Loco, locogio_bh_s &l_Bsh)
{
	unsigned char l_Tmp;

	l_Tmp = l_Bsh.bsy;
	push_bits(l_Loco, &l_Tmp, 4);
	if (l_Loco->color)
	{
		l_Tmp = l_Bsh.bsu;
		push_bits(l_Loco, &l_Tmp, 4);
		l_Tmp = l_Bsh.bsv;
		push_bits(l_Loco, &l_Tmp, 4);
	}
}

static int log2p1c(short a_Value)
{
	if (a_Value < 0)
	{
		a_Value = -a_Value;
	}

	int val = log2p1_lut[a_Value];

	return val;
}

static int compress(locogio_s *l_Loco)
{
	yuv_dif_t *l_YDimgB;
	locogio_bh_s l_Bsh;
	unsigned int l_DescCount = 0;

	l_Loco->compress_size = 0;
	l_Loco->cbuffer_bit_ptr = 7;
	l_Loco->cbuffer_ptr = 0;

	l_Loco->cbuffer[0] = 0;

	for (unsigned int x = 0; x<l_Loco->length; x += l_Loco->cblock_size)
	{
		int l_MaxBitsY = -1;
		int l_MaxBitsU = -1;
		int l_MaxBitsV = -1;

		l_YDimgB = l_Loco->dif + x;


		if (l_Loco->subsample == 0)
		{
			// find min bits size for each block
			for (int j = 0; j<l_Loco->cblock_size; j++)
			{
				int l_Log;

				if (l_YDimgB[j].dy == 0)
				{
					l_Log = 0; //fake value;
				}
				else {
					l_Log = log2p1c(l_YDimgB[j].dy);
				}
				if (l_Log > l_MaxBitsY)
				{
					l_MaxBitsY = l_Log;
				}

				if (l_YDimgB[j].du == 0)
				{
					l_Log = 0; //fake value;
				}
				else {
					l_Log = log2p1c(l_YDimgB[j].du);
				}
				if (l_Log > l_MaxBitsU)
				{
					l_MaxBitsU = l_Log;
				}

				if (l_YDimgB[j].dv == 0)
				{
					l_Log = 0; //fake value;
				}
				else {
					l_Log = log2p1c(l_YDimgB[j].dv);
				}
				if (l_Log > l_MaxBitsV)
				{
					l_MaxBitsV = l_Log;
				}
			}
		}
		else
		{
			//SUBSAMPLE 4:1:1
			// find min bits size for each block
			for (int j = 0; j<l_Loco->cblock_size; j++)
			{
				int log;

				if (l_YDimgB[j].dy == 0)
				{
					log = 0; //fake value;
				}
				else
				{
					log = log2p1c(l_YDimgB[j].dy);
				}
				if (log > l_MaxBitsY)
				{
					l_MaxBitsY = log;
				}
			}

			for (int j = 0; j<l_Loco->cblock_size; j += SUBSAMPLE_SIZE)
			{
				int log;
				if (l_YDimgB[j].du == 0)
				{
					log = 0; //fake value;
				}
				else
				{
					log = log2p1c(l_YDimgB[j].du);
				}
				if (log > l_MaxBitsU)
				{
					l_MaxBitsU = log;
				}

				if (l_YDimgB[j].dv == 0)
				{
					log = 0; //fake value;
				}
				else
				{
					log = log2p1c(l_YDimgB[j].dv);
				}
				if (log > l_MaxBitsV)
				{
					l_MaxBitsV = log;
				}
			}
		}

		// push block header
		l_Bsh.bsy = l_MaxBitsY;
		l_Bsh.bsu = l_MaxBitsU;
		l_Bsh.bsv = l_MaxBitsV;
		push_bsh(l_Loco, l_Bsh);
		l_DescCount++;

		// push values
		for (int j = 0; j<l_Loco->cblock_size; j++)
		{
			if (l_Bsh.bsy != 0)
			{
				push_bits(l_Loco, (unsigned char*)&l_YDimgB[j].dy, l_Bsh.bsy);
			}

			if (l_Loco->color)
			{
				if (l_Loco->subsample == 0)
				{
					if (l_Bsh.bsu != 0)
					{
						push_bits(l_Loco, (unsigned char*)&l_YDimgB[j].du, l_Bsh.bsu);
					}
					if (l_Bsh.bsv != 0)
					{
						push_bits(l_Loco, (unsigned char*)&l_YDimgB[j].dv, l_Bsh.bsv);
					}
				}
				else
				{
					if (j%SUBSAMPLE_SIZE == 0)
					{
						if (l_Bsh.bsu != 0)
						{
							push_bits(l_Loco, (unsigned char*)&l_YDimgB[j].du, l_Bsh.bsu);
						}
						if (l_Bsh.bsv != 0)
						{
							push_bits(l_Loco, (unsigned char*)&l_YDimgB[j].dv, l_Bsh.bsv);
						}
					}
				}
			}
		}
	}

	return l_Loco->compress_size;
}

void ImgCorrection(cv::Mat &InImg, std::string CamID, cv::Mat &OutImg)
{
	// Get gamma for image correction
	double gamma = DeterGamma(CamID);
	double inverse_gamma = 1.0 / gamma;
	//cv::Mat LabImg;
	cv::cvtColor(InImg, OutImg, CV_BGR2Lab);
	// Extract the L channel
	std::vector<cv::Mat> LabPlane(3);
	// Do the gamma correction
	for (int y = 0; y < OutImg.rows; ++y)
		for (int x = 0; x < OutImg.cols; ++x)
			OutImg.at<cv::Vec3b>(y, x)[0] = 255.0 * pow(OutImg.at<cv::Vec3b>(y, x)[0] / 255.0, inverse_gamma);
	cv::split(OutImg, LabPlane);
	// Apply the CLAHE algorithm to the L channel
	cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE();
	clahe->setClipLimit(1.0);
	clahe->setTilesGridSize(cv::Size(5, 1));
	cv::Mat dst;
	clahe->apply(LabPlane[0], dst);

	// Merge the the color planes back into an Lab image
	dst.copyTo(LabPlane[0]);
	cv::merge(LabPlane, OutImg);

	// convert back to RGB
	cv::cvtColor(OutImg, OutImg, CV_Lab2BGR);
}

void SaveJPEGS_fb(bool Jdir_created, std::string CamID, std::string log_path,
	std::vector<std::vector<int>> *VideoData, int Odo)
{
	char *l_VideoData = NULL;
	Video_d_s *l_Video = NULL;
	size_t NumFrame = 0, l_VideoDataSize;
	l_VideoData = (char*)malloc(0x400000); //about 4MB
	l_Video = (Video_d_s *)l_VideoData;
	for (int i = 0; i < VideoData->size(); ++i)
	{
		l_VideoDataSize = VideoData->at(i).size();
		for (int j = 0; j < l_VideoDataSize; ++j)
		{
			*(l_Video->px + j) = (unsigned char)VideoData->at(i).at(j);
		}
		SaveJPEG_fb(Jdir_created, CamID, log_path, NumFrame, l_Video, l_VideoDataSize, Odo);
		NumFrame++;
	}
}

void SaveJPEG_fb(bool Jdir_created, std::string CamID, std::string log_path,
	int NumFrame, Video_d_s *l_Video, size_t l_VideoDataSize, int Odo)
{
	// save jpeg images for front & back cameras
	std::ostringstream jname;
	/*if (fs::is_directory(log_path + '/' + CamID))
	Jdir_created = true;  -- can be written outside of this function */
	if (!Jdir_created)
	{
		fs::path jpegdir(log_path + '/' + CamID);
		fs::create_directories(jpegdir);
		Jdir_created = true;
	}
	if (CamID == "c50") // front camera
		jname << log_path << '/' << CamID << '/' << std::setfill('0') << std::setw(6) << NumFrame << "_Frame[" << l_Video->frameCnt << "]_IntCnt[" << Odo << "]_1.jpg";
	else // rear camera
		jname << log_path << '/' << CamID << '/' << std::setfill('0') << std::setw(6) << NumFrame << "_Frame[" << l_Video->frameCnt << "]_IntCnt[" << Odo << "]_2.jpg";
	std::ofstream jpeg(jname.str(), std::ios::out | std::ios::binary);//l_VideoDataSize - sizeof(Video_d_ss) + 1
    jpeg.write((const char *)l_Video->px, l_VideoDataSize - sizeof(Video_d_s));
    /*
	jpeg.write((const char *)l_Video->px, 2); // Omit 4 Bytes after FF D8
	jpeg.write((const char *)l_Video->px + 6, l_VideoDataSize - sizeof(Video_d_ss) - 5);
    */
	jpeg.close();
}

int SaveJPEG_LCam(bool Jdir_created, std::string CamID, std::string log_path, std::string ImgName,
	std::vector<std::vector<int>> VideoData)
{
	// Save jpeg images for linear cameras
	cv::Mat Img;
	std::ostringstream jname;
	jname << log_path << '/' << CamID << '/' << ImgName << ".jpg";
	if (!Jdir_created)
	{
		fs::path jpegdir(log_path + '/' + CamID);
		fs::create_directories(jpegdir);
		Jdir_created = true;
	}
	Vec2Mat(VideoData, Img, CamID);
	cv::imwrite(jname.str(), Img);
	return 0;
}


void Vec2Mat(std::vector<std::vector<int>> VideoData, cv::Mat &Img, std::string CamID)
{

	if (CamID == "61" || CamID == "71")
	{
		Img.create(VideoData.size(), VideoData.at(0).size(), CV_8U);
	}
	else
		Img.create(VideoData.size(), VideoData.at(0).size() / 3, CV_8UC3);
	for (int j = 0; j < VideoData.size(); ++j)
	{
		if (CamID == "61" || CamID == "71")
		{
			for (int i = 0; i < VideoData.at(0).size(); ++i)
			{
				Img.at<uchar>(j, i) = VideoData.at(j).at(i);
			}
		}
		else
		{
			for (int i = 0; i < VideoData.at(0).size() / 3; ++i)
			{
				Img.at<cv::Vec3b>(j, i)[0] = VideoData.at(j).at(i * 3 + 2);
				Img.at<cv::Vec3b>(j, i)[1] = VideoData.at(j).at(i * 3 + 1);
				Img.at<cv::Vec3b>(j, i)[2] = VideoData.at(j).at(i * 3);
			}
		}

	}
}
// inline void WriteVDO(std::ofstream VDOWriter, infelHd_s *l_Header, char * l_HeaderData, char * l_VideoData, 
// 					 unsigned int length, size_t l_HeaderSize, std::string Folder)
// {
// 	l_Header->totlen = sizeof(Video_d_s) - 1 + length + l_HeaderSize;
// 	VDOWriter.write((const char *)l_HeaderData, l_HeaderSize);
// 	VDOWriter.write((const char *)l_VideoData, sizeof(Video_d_s) - 1 + length);
// 	//VDOWriter.close();
// }
// 

template <typename T> void LinearCamDecompMeta(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
	unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created,
	bool DecompandSaveIm, std::vector<std::vector<T>> *VideoData, int OutputOption)
{
	if (!*l_Initialized)
	{
		*l_Initialized =
			locogio_init(l_CompressionConfig, ImWidth, ImType == IMAGE_GDM_LINEAR_COLOR);
	}

	if (*l_Initialized)
	{
		//l_VideoBuffer = ( (unsigned char *)l_VideoData + sizeof(Video_d_s) - 1);
		//l_VideoBuffer_out = (unsigned char *)malloc(0x400000);
		locogio_decompress_line_meta(l_CompressionConfig, l_VideoBuffer, l_VideoBuffer, (l_totlen - sizeof(Video_i_s)) * 8,
			CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImType, VideoData, OutputOption);

	}
}

unsigned int LinearCamDecompression(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
	unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen, cv::Mat &image,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, bool ImgCorr)
{
	if (!*l_Initialized)
	{
		*l_Initialized =
			locogio_init(l_CompressionConfig, ImWidth, ImType == IMAGE_GDM_LINEAR_COLOR);
	}

	if (*l_Initialized)
	{
		l_VideoBuffer = ((unsigned char *)l_VideoData + sizeof(Video_d_s) - 1);
		// Get the line image as the format of cv::Mat
		cv::Mat LineImg = locogio_decompress_line(l_CompressionConfig, l_VideoBuffer, l_VideoBuffer, (l_totlen - sizeof(Video_i_s)) * 8, image,
			CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImType);
		if (ImgCorr)
		{
			cv::Mat OutImg;
			// Do image correction
			ImgCorrection(LineImg, CamID, OutImg);
			// Overwrite corrected values back to l_VideoBuffer
			for (int x = 0; x < l_CompressionConfig->length; ++x)
			{
				l_VideoBuffer[x * 3 + 2] = OutImg.at<cv::Vec3b>(0, x)[0];
				l_VideoBuffer[x * 3 + 1] = OutImg.at<cv::Vec3b>(0, x)[1];
				l_VideoBuffer[x * 3] = OutImg.at<cv::Vec3b>(0, x)[2];
			}
		}

		locogio_compress_line(l_CompressionConfig, l_VideoBuffer, l_VideoBuffer);
		unsigned int length = l_CompressionConfig->cbuffer_ptr;
		return length;
		/*locogio_decompress_line( l_CompressionConfig, l_VideoBuffer, l_VideoBuffer, (l_totlen-sizeof(Video_i_s))*8, image,
		CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImType);*/
	}
}

int ArgtoVal(std::string InputArg, long int *StartIntern, long int *EndIntern, std::string *SID)
{
	InputArg.erase(remove_if(InputArg.begin(), InputArg.end(), isspace), InputArg.end()); // Remove spaces
	size_t found = InputArg.find_first_of("[{(");
	if (found == std::string::npos)
		return 0; // There is no "[{("

				  // There exists "[{("
	*SID = InputArg.substr(0, found);
	*StartIntern = std::stol(&InputArg[found + 1]);
	found = InputArg.find_first_of(", ");
	*EndIntern = std::stol(&InputArg[found + 1]);
	return 1; // There exists "[{("
}

// Read vdo files, do image correction and then write back to vdo files
int VDORPW(std::string indir, std::string outdir)
{
	int num_elements = 50;
	int num_elements_sub = 3;
	char * l_HeaderData = NULL;
	char * l_HDataTem = NULL;
	char * l_VDataTem = NULL; // Save video data at the end of the file and concatenate the next file
	char * l_VideoData = NULL;
	FILE * l_VideoFile = NULL;
	infelHd_s * l_HeaderTem = NULL;
	char * l_HeaderTemData = NULL;
	size_t l_HeaderSize = sizeof(infelHd_s);
	int frameIdx;
	int l_VRSize;
	int l_totlen; // l_Header->totlen in the previous vdo file
	int l_HRSize; // Size of read header in previous vdo file
	bool BreakinHeader = false; // to check whether a break in header for different vdo files
	bool BreakinData = false;
	size_t l_HSizeTem = sizeof(infelHd_ss);

	l_HeaderTemData = (char*)calloc(l_HeaderSize, sizeof(char));
	l_HeaderTem = (infelHd_s *)l_HeaderTemData;
	l_HDataTem = (char*)calloc(l_HSizeTem, sizeof(char));
	l_VDataTem = (char*)calloc(0x400000, sizeof(char)); // about 4 Mb
	bool HDataTemused;
	// The start and end of internal counter, range to save the images
	long int StartInern, EndIntern;

	SVec Filelist;
	std::ofstream VdoDscr, LogFile;
	std::string SID;
	std::string directory;
	std::string TargetFolder; // Target folder for new vdo files

	SID = outdir;
	TargetFolder = outdir;

	CheckFolderExists_CreateFolder(outdir);
	
    std::string CamID = "";
    getFilelist(indir, CamID, directory, Filelist);

	// Put files in Filelist into different catalogs
	// Select different camera IDs and put them into the corresponding catalog
	std::vector<SVec> FCatalog;
	bool Dir_created = false;
	std::string dir_path, log_path;
	ConstructFCatalog(&FCatalog);
	CatalogFile(&FCatalog, Filelist);
	SortCatalog(&FCatalog);

	// Log file output and create directory

	//std::ostringstream LogFileName;
	if (Filelist.size() != 0)
	{
		const size_t first_dot = Filelist.at(0).find_first_of('.');
		log_path = Filelist.at(0).substr(0, first_dot);
	}
	else
	{
		return 0;
	}

	// Iterate over vdo files by camera stations
	for (auto itt = FCatalog.begin(); itt != FCatalog.end(); ++itt)
	{
		int totsize = 0;
		size_t LastBlen = 0, LastBtotlen = 0;
		std::ostringstream OutFileName, Out;
		bool OutVideoDscr = false; // Switch to turn on writing csv file
		bool l_Initialized(false);
		locogio_s l_CompressionConfig;
		unsigned char * l_VideoBuffer;
		l_VideoBuffer = NULL;
		static int ImType, ImWidth; bool ImaproGet = false;
		cv::Mat image;
		static int NumBlocks = 0;
		bool Jdir_created = false; // JPEG directory creation tag
		bool ImSaveFinished = false; // Tag to show whether image has been saved
		bool ImSplit = false;
		std::string CamID;

		// Whether decompress and save linear camera images or not
		if (!NoDecomp)
		{
			if (1) // Hard coded to make the program reads starting from the first vdo file
				   //if (ImOutVDORange(StartInern, EndIntern, &(*itt), directory))
				OutVideoDscr = false;
			else
			{
				std::cout << "Internal Counter range does not exist!" << std::endl;
				system("PAUSE");
				return 0;
			}
		}

		if (itt->size() != 0)
		{
			// Get camera ID
			size_t first_dot = itt->at(0).find_first_of('.');
			size_t second_dot = itt->at(0).find_first_of('.', first_dot + 1);
			size_t third_dot = itt->at(0).find_first_of('.', second_dot + 1);
			CamID = itt->at(0).substr(second_dot + 1, third_dot - second_dot - 1);
			// Do not execute camera 61 71 c50 and c51, just copy them
			if (CamID == "61" || CamID == "71" || CamID == "c50" || CamID == "c51")
			{
				for (size_t i = 0; i < itt->size(); ++i)
				{
					std::string SrcFile = directory + itt->at(i);
					std::string TargetFile = TargetFolder + "/" + itt->at(i);
					fs::copy_file(SrcFile, TargetFile);
				}
				continue;
			}
			OutFileName << "VdoDscr_" << itt->at(0) << ".csv";
			if (OutVideoDscr)
			{
				if (!Dir_created)
				{
					const size_t first_dot = itt->at(0).find_first_of('.');
					dir_path = itt->at(0).substr(0, first_dot);
					fs::path dir(dir_path);
					if (fs::create_directories(dir))
						Dir_created = true;
				}
				Out << log_path << "/" << OutFileName.str();
				//VdoDscr.open(Out.str().c_str(), std::ofstream::out);
				//VdoDscr << "sep=," << std::endl; // Open with excel with columns
				//VdoDscr << "Odometer:" << ',' << "FrameNum:" << std::endl;
			}
		}
		else
			OutVideoDscr = false;

		// Iterate over vdo files for the same camera station
		for (size_t it = 0; it < itt->size(); ++it)
		{
			// Check wether a file is empty
			fs::path fchecked(directory + itt->at(it));
			if (fs::is_empty(fchecked))
				continue;
			// Get vdo file index for a certain camera station ID
			size_t first_dot = itt->at(it).find_first_of('.');
			size_t second_dot = itt->at(it).find_first_of('.', first_dot + 1);
			std::string VDOidx = itt->at(it).substr(first_dot + 1, second_dot - first_dot - 1);

			// Generate VDOWriter
			std::ostringstream vdo;
			vdo << TargetFolder << "/" << log_path << "." << VDOidx << "." << CamID << ".vdo";
			/*if (fs::exists(vdo.str()))
			fs::remove(vdo.str());*/
			std::ofstream VDOWriter(vdo.str(), std::ios::out | std::ios::binary | std::ios::app);//l_VideoDataSize - sizeof(Video_d_ss) + 1

																								 //int Endianness = 0; // Endianness determination
																								 //CheckEndian(&Endianness); // Check Endianness if needed
																								 //int OutLsize = 25; // For aligning output txt file
			size_t l_TotalDataRead = 0;

			l_VideoFile = fopen((directory + '\\' + itt->at(it)).c_str(), "rb");
			if (l_VideoFile == NULL)
			{
				printf("Error opening the entered file, does it exist?\n");
				goto usage;
			}


			{
				size_t l_HeaderSize = sizeof(infelHd_s);
				size_t l_VideoDataSize = 0;
				size_t l_DataReadSize = 0;

				l_HeaderData = (char*)calloc(l_HeaderSize, sizeof(char));
				l_VideoData = (char*)calloc(0x400000, sizeof(char)); //about 4MB

				infelHd_s * l_Header = NULL;
				Video_d_s *l_Video = NULL;
				Format *F = NULL;

				/*if (CamID != SID && argc > 2)
				{
				std::cout << "Camera stations are different for files to read and images to save!" << std::endl;
				break;
				}*/

				if (LastBtotlen - LastBlen != 0)
				{
					if (BreakinData)
					{
						fread(l_VDataTem + l_VRSize, 1, LastBtotlen - LastBlen, l_VideoFile);
						l_Video = (Video_d_s *)l_VDataTem;
						//fseek(l_VideoFile, LastBtotlen - LastBlen, SEEK_CUR);

#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& (CamID == "60" || CamID == "62" || CamID == "64" || CamID == "65" ||
									CamID == "70" || CamID == "72" || CamID == "74" || CamID == "75"))
							{
								unsigned int length = LinearCamDecompression(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VDataTem, l_totlen, image,
									CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImgCorr);
								//WriteVDO(VDOWriter, l_HeaderTem, l_HeaderData, l_VDataTem, length, l_HeaderSize, TargetFolder);
								l_HeaderTem->totlen = sizeof(Video_d_s) - 1 + length + l_HeaderSize;
								VDOWriter.write((const char *)l_HeaderTemData, l_HeaderSize);
								VDOWriter.write((const char *)l_VDataTem, sizeof(Video_d_s) - 1 + length);
							}
						}
#endif
						BreakinData = false;
					}
					// Shift the file handle
					else
						fseek(l_VideoFile, (long)(LastBtotlen - LastBlen), SEEK_SET);
					LastBtotlen = 0; LastBlen = 0; // set back to zero in order not to effect next files
				}

				while (feof(l_VideoFile) == 0)
				{
					//if (NumBlocks == 195698) // for 74, reading error occurs in 002.74.vdo
					//	std::cout << "terminate" << std::endl;
					bool turn = false;
					if (BreakinHeader) // If the header is split in two different vdo files
					{
						HDataTemused = true;
						// Use a temporary buffer to save the header information in the second vdo file
						l_DataReadSize = fread(l_HDataTem + l_HRSize, 1, l_HeaderSize - l_HRSize, l_VideoFile);
					}
					else
					{
						HDataTemused = false;
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
					}
					BreakinHeader = false;
					if (l_DataReadSize != l_HeaderSize)
					{
						if (feof(l_VideoFile) != 0) // If to the end of the file
						{
							l_HRSize = (int)l_DataReadSize;
							// Save part of header information in the first vdo file to a temporary buffer
							memcpy(l_HDataTem, l_HeaderData, l_HRSize);
							BreakinHeader = true;
						}
						if (feof(l_VideoFile) == 0 && l_DataReadSize != l_HeaderSize - l_HRSize)
						{
							printf("Read unexpected amount of data for the header\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_HeaderSize);
							goto exit;
						}
						if (BreakinHeader)
						{
							l_TotalDataRead += l_DataReadSize;
							goto exit;
						}
					}
					l_TotalDataRead += l_DataReadSize;

					if (!HDataTemused)
						l_Header = (infelHd_s *)l_HeaderData;
					else
						l_Header = (infelHd_s *)l_HDataTem;

					// Some notes:
					// If l_Header->infid is not "divD", search till the next "divD" is found and continue processing
					if (l_Header->infid != VIDEO_FIF) // When this condition is satisfied, there probably be something wrong with the data.
					{
						std::cout << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						std::cout << "The previous frame idx is " << frameIdx << std::endl;
						//LogFile << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						//LogFile << "The previous frame idx is " << frameIdx << std::endl;
						int offset = -(int(l_DataReadSize) + l_VRSize);
						int pos1 = ftell(l_VideoFile);
						//fpos_t pos1;
						//fgetpos(l_VideoFile, &pos1);
						if (pos1 < -offset) // Make sure that the file handle is not out of the file boundary
							fseek(l_VideoFile, 0, SEEK_SET);
					}

					// Search for the next "divD" if the header is not correctly stored in l_Header
					while (l_Header->infid != VIDEO_FIF)
					{
						unsigned char c; // note: int, not char, required to handle EOF
						turn = true;
						while ((c = std::fgetc(l_VideoFile)) != 'd' && feof(l_VideoFile) == 0)
						{ // standard C I/O file reading loop
						}
						if (feof(l_VideoFile) != 0)
							break;
						fseek(l_VideoFile, -1, SEEK_CUR);
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
						l_Header = (infelHd_s *)l_HeaderData;
					}
					if (feof(l_VideoFile) != 0)
						break;
					///////////////////////////////////////////////////////

					l_totlen = l_Header->totlen;
					l_VideoDataSize = l_totlen - l_HeaderSize;

					l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, l_VideoFile);
					l_VRSize = int(l_DataReadSize);
					//fseek(l_VideoFile, l_VideoDataSize, SEEK_CUR);
					/*if (ferror (l_VideoFile))
					std::cout << "Error occurred while reading file!" << std::endl;*/
					if (l_DataReadSize != l_VideoDataSize)
					{
						if (feof(l_VideoFile) == 0)
						{
							printf("Read unexpected amount of data for the video packet\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_VideoDataSize);
							goto exit;
						}
						// It means here is the end of the file
						if (l_Header->infid == VIDEO_FIF)
						{
							memcpy(l_VDataTem, l_VideoData, l_VRSize); // Copy the data from the previous file
							BreakinData = true;
							//l_totlen = l_Header->totlen;
							memcpy(l_HeaderTemData, l_HeaderData, l_HeaderSize);
						}
						LastBtotlen = l_VideoDataSize; LastBlen = l_DataReadSize; // Exclude length of header
																				  // Add the read data size when the last block is not complete --Shulin
						l_TotalDataRead += l_DataReadSize;
						goto exit;
					}
					l_TotalDataRead += l_DataReadSize;

					if (l_Header->infid == VIDEO_FIF)
					{
						//l_Video = (Video_d_s *) ::operator new (l_DataReadSize); // Commented out for just output vdo detail
						l_Video = (Video_d_s *)l_VideoData;
						if (!ImaproGet)
						{
							ImType = l_Video->image_type;
							ImWidth = l_Video->width;
							ImaproGet = true;
						}
						frameIdx = l_Video->frameCnt;
						if (turn == true)
						{
							std::cout << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
							//LogFile << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
						}

						//OutVideoDscr = false;

						//perc = l_TotalDataRead / 1080471587.0 * 100;
						//if (perc > 99.99)

						//	std::cout << "Percentage" << perc << "\%" << std::endl; 
						// Decompress

#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							/*if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
							&& CamID != "c50" && l_Video->St.Odom >= StartInern && l_Video->St.Odom <= EndIntern)*/
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& (CamID == "60" || CamID == "62" || CamID == "64" || CamID == "65" ||
									CamID == "70" || CamID == "72" || CamID == "74" || CamID == "75"))
							{
								// Size to be decompressed, processed and recompressed
								totsize += l_Header->totlen;
								unsigned int length = LinearCamDecompression(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VideoData, l_totlen, image,
									CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImgCorr);
								// Write back to vdo file
								if (!HDataTemused)
								{
									//WriteVDO(log_path, VDOidx, CamID, l_Header, l_HeaderData, l_VideoData, length, l_HeaderSize, TargetFolder);
									l_Header->totlen = sizeof(Video_d_s) - 1 + length + l_HeaderSize;
									VDOWriter.write((const char *)l_HeaderData, l_HeaderSize);
									VDOWriter.write((const char *)l_VideoData, sizeof(Video_d_s) - 1 + length);
								}
								else
								{
									//WriteVDO(log_path, VDOidx, CamID, l_Header, l_HDataTem, l_VideoData, length, l_HeaderSize, TargetFolder);
									l_Header->totlen = sizeof(Video_d_s) - 1 + length + l_HeaderSize;
									VDOWriter.write((const char *)l_HDataTem, l_HeaderSize);
									VDOWriter.write((const char *)l_VideoData, sizeof(Video_d_s) - 1 + length);
								}
							}

							// Output image
							/*if (ImSplit || l_Video->St.Odom > EndIntern)
							{
							std::ostringstream jname;
							double dist = (ImEndIntern - StartInern) / 8000.0;
							jname << log_path << '/' << CamID << '/' << dist << "m_(" << StartInern << ", " << ImEndIntern << "].jpg";
							cv::imwrite(jname.str(), image);
							cv::Mat outimg;
							ImgCorrection(image, 3.0, outimg);
							// reset Image
							if (ImSplit)
							image.release();
							ImSplit = false;
							StartInern = ImEndIntern;
							//ImSaveFinished = true;
							if (l_Video->St.Odom > EndIntern)
							{
							// Free memory and return
							if (!BreakinHeader)
							if(l_HeaderData != NULL) free(l_HeaderData);
							if(l_VideoData != NULL) free(l_VideoData);
							if(l_VideoFile != NULL)
							{
							fclose(l_VideoFile);
							printf("File read without problems!\n");
							}
							printf("Read %Iu bytes\n", l_TotalDataRead);
							system("PAUSE");
							return 0;
							}
							}*/
						}
#endif

					}
				}

				goto exit;
			}

		usage:
			ShowUsage1();

		exit:
			if (!BreakinHeader)
				if (l_HeaderData != NULL) free(l_HeaderData);
			if (l_VideoData != NULL) free(l_VideoData);
			if (l_VideoFile != NULL)
			{
				fclose(l_VideoFile);
				//printf("File read without problems!\n");
				//LogFile << "File read without problems!" << std::endl;
			}
			//printf("Read %Iu bytes\n", l_TotalDataRead);
			//LogFile << "Read " << l_TotalDataRead<< " bytes" << std::endl;
			//round ++;
			//system("PAUSE");
		}
		if (OutVideoDscr)
		{
			std::cout << OutFileName.str() << "  generated!" << std::endl;
			//LogFile << OutFileName.str() <<  "  generated!" << std::endl;
		}
		OutVideoDscr = false;
		//VdoDscr.close();
	}

	//if (l_HDataTem != NULL)
	free(l_HDataTem);
	//if (l_VDataTem != NULL)
	free(l_VDataTem);
	//if (l_HeaderTemData != NULL)
	free(l_HeaderTemData);

	//LogFile.close();
	//system("PAUSE");
	return 0;
}

// Get metadata in a certain Internal counter range from VDO files
int GetMetadataFromIntCnt(std::string dir, std::string saverange,
	std::vector<Video_d_s> *RangeVideoData, std::vector<infelHd_s> *RangeHeaderData, std::vector<std::vector<char>> *VideoData,
	int OutputOption, bool save_pano_img, bool save_csv_info, double Uncertainty)
{
	std::string CamID = saverange.substr(0, saverange.find_first_of("[{("));
	fs::path idx_file;
	SVec idx_file_list;
	Indexer_s *indexer_start, *indexer_end;
	char * l_HeaderData = NULL;
	char * l_HDataTem = NULL;
	char * l_VDataTem = NULL; // Save video data at the end of the file and concatenate the next file
	char * l_VideoData = NULL;
	// Save the header data if video data is separated in two vdo files in order to save it back to std vector and then python list
	char * l_HDataTemFBreak = NULL;
	FILE * l_VideoFile = NULL;
	int frameIdx;
	int l_VRSize;
	int l_totlen; // l_Header->totlen in the previous vdo file
	int l_HRSize; // Size of read header in previous vdo file
	bool BreakinHeader = false; // to check whether a break in header for different vdo files
	bool BreakinData = false;
	bool RangeExists = false; // Whether the rail range exists
	size_t l_HSizeTem = sizeof(infelHd_s);
	l_HDataTem = (char*)malloc(l_HSizeTem);
	l_VDataTem = (char*)malloc(0x400000); // about 4 Mb
	l_HDataTemFBreak = (char*)malloc(l_HSizeTem);
	bool HDataTemused;
	// The start and end of internal counter, range to save the images
	long int StartInern, EndIntern;
	bool pano_all_export = false;

	SVec Filelist;

	std::string directory;
	// record the internal counter and frame number of exported pano images
	std::ofstream pano_csv;

	if (saverange != "c50" && saverange != "c51")
	{
		// Get internal counter interval
		if (RangeExists = ArgtoVal(saverange, &StartInern, &EndIntern, &saverange)) { NoDecomp = false; }// There exists "[{("
		else
			NoDecomp = true;
		if (!NoDecomp & (StartInern > EndIntern))
		{
			std::cout << "first counter is greater than second counter, please reput counter!" << std::endl;
			//system("PAUSE");
			return 0;
		}
	}
	else // In case of exporting all panorama images 
	{
		StartInern = std::numeric_limits<long>::min();
		EndIntern = std::numeric_limits<long>::max();
		pano_all_export = true;
	}

	// get indexer if both odo_start and odo_end are not 0
	if (StartInern != 0 && EndIntern != 0)
	{
		GetFileInDir(dir, &idx_file_list);
		elimVDOs(&idx_file_list);
		GetIdxFilefromNonVdoFile(&idx_file_list, CamID);
		if (idx_file_list.size() == 1)
		{
			fs::path d(dir), idx_f(idx_file_list.at(0));
			idx_file = d / idx_f;
		}
		else
		{
			std::cout << "number of idx file exceeds 1!" << std::endl;
			return -1;
		}
		// read idx file
		indexer_start = get_indexer_from_given_odo(StartInern, idx_file.string(), 1);
		indexer_end = get_indexer_from_given_odo(EndIntern, idx_file.string(), 0);
	}
	else
	{
		indexer_start = new Indexer_s();
		indexer_end = new Indexer_s();
	}

	getFilelist(dir, CamID, directory, Filelist);

	// Put files in Filelist into different catalogs
	// Select different camera IDs and put them into the corresponding catalog
	std::vector<SVec> FCatalog;
	bool Dir_created = false;
	std::string dir_path, log_path;
	ConstructFCatalog(&FCatalog);
	CatalogFile(&FCatalog, Filelist);
	SortCatalog(&FCatalog);

	// Log file output and create directory
	if (Filelist.size() != 0)
	{
		const size_t first_dot = Filelist.at(0).find_first_of('.');
		log_path = Filelist.at(0).substr(0, first_dot);
	}
	else
	{
		std::cout << "No vdo files found!" << std::endl;
		return 0;
	}
	//double perc; int round = 1;
	// Iterate over vdo files by camera stations
	for (auto itt = FCatalog.begin(); itt != FCatalog.end(); ++itt)
	{
		size_t LastBlen = 0, LastBtotlen = 0;
		bool l_Initialized(false);
		locogio_s l_CompressionConfig;
		//l_CompressionConfig = (locogio_s*)malloc(sizeof(locogio_s));

		static int ImType, ImWidth; bool ImaproGet = false;
		int NumBlocks = 0;
		bool Jdir_created(false); // JPEG directory creation tag
		bool ImSaveFinished = false; // Tag to show whether image has been saved
		bool ImSplit = false;
		std::string CamID, path_csv;
		int file_part_start, file_part_end;

		if (itt->size() != 0)
		{
			// Get camera ID 
			size_t first_dot = itt->at(0).find_first_of('.');
			size_t second_dot = itt->at(0).find_first_of('.', first_dot + 1);
			size_t third_dot = itt->at(0).find_first_of('.', second_dot + 1);
			CamID = itt->at(0).substr(second_dot + 1, third_dot - second_dot - 1);
			// erase redundant vdo files from the file list
			file_part_start = atoi(itt->front().substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			while (file_part_start < indexer_start->filePart)
			{
				itt->erase(itt->begin());
				file_part_start = atoi(itt->front().substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			}
			file_part_end = atoi(itt->back().substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			while (file_part_end > indexer_end->filePart)
			{
				itt->pop_back();
				file_part_end = atoi(itt->back().substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			}
		}

		if (CamID != saverange)
		{
			//std::cout << "Camera stations are different for files to read and images to save!" << std::endl;
			continue;
		}

		if (CamID == "c50" || CamID == "c51")
		{
			if (!Jdir_created && (save_pano_img || save_csv_info))
			{
				fs::path jpegdir(log_path + '/' + CamID);
				fs::create_directories(jpegdir);
				Jdir_created = true;
			}
			// This file is for GPS exportation
			if (save_csv_info)
			{
				path_csv = log_path + '/' + CamID + '/' + log_path + '_' + CamID + "_IntCntFrNum.csv";
				pano_csv.open(path_csv.c_str(), std::ofstream::out);
				pano_csv << "sep=," << std::endl; // Open with excel with columns
				pano_csv << "Odometer:" << ',' << "FrameNum:" << std::endl;
			}
		}

		// Iterate over vdo files for the same camera station
		for (size_t it = 0; it < itt->size(); ++it)
		{
			//int Endianness = 0; // Endianness determination
			//CheckEndian(&Endianness); // Check Endianness if needed
			//int OutLsize = 25; // For aligning output txt file
			size_t l_TotalDataRead = 0;
			unsigned char * l_VideoBuffer;
			l_VideoBuffer = NULL;
			l_VideoFile = fopen((directory + '\\' + itt->at(it)).c_str(), "rb");
			// shift the FILE pointer by indexer->byteOffset
			if (it == 0)
				fseek(l_VideoFile, indexer_start->byteOffset, SEEK_CUR);
			if (l_VideoFile == NULL)
			{
				printf("Error opening the entered file, does it exist?\n");
				goto usage;
			}


			{
				size_t l_HeaderSize = sizeof(infelHd_s);
				size_t l_VideoDataSize = 0;
				size_t l_DataReadSize = 0;

				l_HeaderData = (char*)malloc(l_HeaderSize);
				l_VideoData = (char*)malloc(0x400000); //about 4MB
				l_VideoBuffer = ((unsigned char *)l_VideoData + sizeof(Video_d_s) - 1);
				infelHd_s * l_Header = NULL;
				Video_d_s *l_Video = NULL;

				if (LastBtotlen - LastBlen != 0)
				{
					if (BreakinData)
					{
						fread(l_VDataTem + l_VRSize, 1, LastBtotlen - LastBlen, l_VideoFile);
						l_Video = (Video_d_s *)l_VDataTem;

						// It seems that BreakinData for c50 does not exist!
						if ((saverange == "c50" && CamID == "c50") || (saverange == "c51" && CamID == "c51"))
						{

							//infelHd_s * l_HeaderTemFBreak = NULL;
							//l_HeaderTemFBreak = (infelHd_s *)l_HDataTemFBreak;
							//(*RangeHeaderData).push_back(*l_HeaderTemFBreak);
							//(*RangeVideoData).push_back(*l_Video);
							size_t l_VDataTemSize = l_VRSize + LastBtotlen - LastBlen;
							//unsigned char *l_VDataTemUchar = NULL;
							//l_VDataTemUchar = (unsigned char *)l_VDataTem;
							//(*VideoData).push_back(std::vector<int>(l_VDataTemUchar + sizeof(Video_d_s) - 1, l_VDataTemUchar + l_VDataTemSize));

							/*// Output Image when processing panorama cameras -- this output all panorama images
							SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VDataTemSize);
							NumBlocks++;*/

							// Output panorama image with internal counter in a certain range -- since the internal counter has been corrected
							if (l_Video->St.Odom >= StartInern && l_Video->St.Odom <= EndIntern)
							{
								if (save_pano_img)
								{
									SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VDataTemSize, l_Video->St.Odom);
									NumBlocks++;
								}
								if (save_csv_info)
									pano_csv << l_Video->St.Odom << ',' << l_Video->frameCnt << std::endl;

							}

						}

#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& CamID != "c50" && CamID == saverange && l_Video->St.Odom >= StartInern && l_Video->St.Odom <= EndIntern)
							{
								// Save l_HeaderData data to std vector and port to python list
								infelHd_s * l_HeaderTemFBreak = NULL;
								l_HeaderTemFBreak = (infelHd_s *)l_HDataTemFBreak;
								(*RangeHeaderData).push_back(*l_HeaderTemFBreak);
								// Save l_VideoData data to std vector and port to python list
								(*RangeVideoData).push_back(*l_Video);
								if (OutputOption == 0)
								{
									size_t l_VDataTemSize = l_VRSize + LastBtotlen - LastBlen;
									// shift one position for unsigned char at the end of struct
									(*VideoData).push_back(std::vector<char>(l_VDataTem + sizeof(Video_d_s) - 1, l_VDataTem + l_VDataTemSize));
								}
								else
								{
									LinearCamDecompMeta(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VDataTem, l_totlen,
										CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, VideoData, OutputOption);
								}
							}
						}
#endif
						BreakinData = false;
					}
					// Shift the file handle
					else
						fseek(l_VideoFile, (long)(LastBtotlen - LastBlen), SEEK_SET);
					LastBtotlen = 0; LastBlen = 0; // set back to zero in order not to effect next files
				}

				while (feof(l_VideoFile) == 0)
				{
					bool turn = false;
					if (BreakinHeader) // If the header is split in two different vdo files
					{
						HDataTemused = true;
						// Use a temporary buffer to save the header information in the second vdo file
						l_DataReadSize = fread(l_HDataTem + l_HRSize, 1, l_HeaderSize - l_HRSize, l_VideoFile);
					}
					else
					{
						HDataTemused = false;
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
					}
					BreakinHeader = false;
					if (l_DataReadSize != l_HeaderSize)
					{
						if (feof(l_VideoFile) != 0) // If to the end of the file
						{
							l_HRSize = (int)l_DataReadSize;
							// Save part of header information in the first vdo file to a temporary buffer
							memcpy(l_HDataTem, l_HeaderData, l_HRSize);
							BreakinHeader = true;
						}
						if (feof(l_VideoFile) == 0 && l_DataReadSize != l_HeaderSize - l_HRSize)
						{
							printf("Read unexpected amount of data for the header\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_HeaderSize);
							goto exit;
						}
						if (BreakinHeader)
						{
							l_TotalDataRead += l_DataReadSize;
							goto exit;
						}
					}
					l_TotalDataRead += l_DataReadSize;

					if (!HDataTemused)
					{
						l_Header = (infelHd_s *)l_HeaderData;
					}
					else
					{
						l_Header = (infelHd_s *)l_HDataTem;
					}
					// Some notes:
					// If l_Header->infid is not "divD", search till the next "divD" is found and continue processing
					if (l_Header->infid != VIDEO_FIF) // When this condition is satisfied, there probably be something wrong with the data.
					{
						std::cout << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						std::cout << "The previous frame idx is " << frameIdx << std::endl;
						int offset = -(int(l_DataReadSize) + l_VRSize);
						//fpos_t pos1;
						//fgetpos(l_VideoFile, &pos1);
						int pos1 = ftell(l_VideoFile);
						if (pos1 < -offset) // Make sure that the file handle is not out of the file boundary
							fseek(l_VideoFile, 0, SEEK_SET);
					}

					// Search for the next "divD" if the header is not correctly stored in l_Header
					while (l_Header->infid != VIDEO_FIF)
					{
						unsigned char c; // note: int, not char, required to handle EOF
						turn = true;
						while ((c = std::fgetc(l_VideoFile)) != 'd' && feof(l_VideoFile) == 0)
						{ // standard C I/O file reading loop
						}
						if (feof(l_VideoFile) != 0)
							break;
						fseek(l_VideoFile, -1, SEEK_CUR);
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
						l_Header = (infelHd_s *)l_HeaderData;
					}
					if (feof(l_VideoFile) != 0)
						break;
					///////////////////////////////////////////////////////

					l_totlen = l_Header->totlen;
					l_VideoDataSize = l_totlen - l_HeaderSize;

					l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, l_VideoFile);
					l_VRSize = int(l_DataReadSize);
					//fseek(l_VideoFile, l_VideoDataSize, SEEK_CUR);
					/*if (ferror (l_VideoFile))
					std::cout << "Error occurred while reading file!" << std::endl;*/
					if (l_DataReadSize != l_VideoDataSize)
					{
						if (feof(l_VideoFile) == 0)
						{
							printf("Read unexpected amount of data for the video packet\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_VideoDataSize);
							goto exit;
						}
						// It means here is the end of the file
						if (l_Header->infid == VIDEO_FIF)
						{
							memcpy(l_VDataTem, l_VideoData, l_VRSize); // Copy the data from the previous file
							BreakinData = true;
							// Copy memory to l_HDataTemFBreak and save to std vector in the next iteration. Header data is complete if video data is split
							memcpy(l_HDataTemFBreak, l_HeaderData, l_HeaderSize);
							l_totlen = l_Header->totlen;
						}
						LastBtotlen = l_VideoDataSize; LastBlen = l_DataReadSize; // Exclude length of header
																				  // Add the read data size when the last block is not complete --Shulin
						l_TotalDataRead += l_DataReadSize;
						goto exit;
					}
					l_TotalDataRead += l_DataReadSize;

					if (l_Header->infid == VIDEO_FIF)
					{
						l_Video = (Video_d_s *)l_VideoData;
						if (!ImaproGet)
						{
							ImType = l_Video->image_type;
							ImWidth = l_Video->width;
							ImaproGet = true;
						}
						frameIdx = l_Video->frameCnt;
						if (turn == true)
						{
							std::cout << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
						}

						// save jpeg files for camera c50
						if ((saverange == "c50" && CamID == "c50") || (saverange == "c51" && CamID == "c51"))
						{
							//(*RangeHeaderData).push_back(*l_Header);
							//(*RangeVideoData).push_back(*l_Video);
							//unsigned char *l_VideoDataUchar = NULL;
							//l_VideoDataUchar = (unsigned char *)l_VideoData;
							//(*VideoData).push_back(std::vector<int>(l_VideoDataUchar + sizeof(Video_d_s) - 1, l_VideoDataUchar + l_VideoDataSize));

							/*// Output Image when processing panorama cameras -- this output all panorama images
							SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
							NumBlocks++;*/

							// Output panorama image with internal counter in a certain range -- since the internal counter has been corrected
							if (l_Video->St.Odom >= StartInern && l_Video->St.Odom <= EndIntern)
							{
								if (save_csv_info)
									pano_csv << l_Video->St.Odom << ',' << l_Video->frameCnt << std::endl;
								if (save_pano_img)
								{
									// Output panorama image
									SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
									NumBlocks++;
								}
								if (!save_csv_info && !save_pano_img)
								{
									(*RangeHeaderData).push_back(*l_Header);
									(*RangeVideoData).push_back(*l_Video);
									(*VideoData).push_back(std::vector<char>(l_VideoData + sizeof(Video_d_s) - 1, l_VideoData + l_VideoDataSize));
								}

							}
						}

						// Decompress					
#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& CamID != "c50" && l_Video->St.Odom >= StartInern && l_Video->St.Odom <= EndIntern)
							{
								// Save l_HeaderData data to std vector and port to python list
								(*RangeHeaderData).push_back(*l_Header);
								// Save l_VideoData data to std vector and port to python list
								(*RangeVideoData).push_back(*l_Video);
								if (OutputOption == 0)
								{
									// shift one position for unsigned char at the end of struct. Output the video frames as raw data (compressed)
									(*VideoData).push_back(std::vector<char>(l_VideoData + sizeof(Video_d_s) - 1, l_VideoData + l_VideoDataSize));
								}
								// Output decompressed video data
								else
								{
									LinearCamDecompMeta(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VideoData, l_totlen,
										CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, VideoData, OutputOption);
								}

							}
						}
#endif

					}
					if (l_Video->St.Odom > EndIntern)
						break;
				}

				goto exit;
			}

		usage:
			ShowUsage2();

		exit:

			if (!HDataTemused)
			{
				if (l_HeaderData != NULL) free(l_HeaderData);
			}
			else
			{
				free(l_HDataTem);
			}
			if (l_VideoData != NULL) free(l_VideoData);
			if (l_VideoFile != NULL)
			{
				fclose(l_VideoFile);
				//printf("File read without problems!\n");
			}

		}

	}

	free(l_VDataTem);
	free(l_HDataTemFBreak);
	return 0;
}

Indexer_s *get_indexer_from_given_odo(int Odometer, std::string idx_file, bool l_odo_boundary)
{
	FILE * IndFile = NULL;
	char * IndData = NULL, *IndVersion = NULL;
	unsigned short * version = NULL;
	Indexer_s *indexer = new Indexer_s(), *Ind = NULL;
	int IndDataSize = sizeof(Indexer_s);
	size_t DataReadSize = 0;
	IndData = (char *)malloc(IndDataSize);
	IndVersion = (char *)malloc(2);
	IndFile = fopen(idx_file.c_str(), "rb");
	fread(IndVersion, 1, 2, IndFile);
	version = (unsigned short *)IndVersion;
	int n = 0;
	while (!feof(IndFile))
	{
		DataReadSize = fread(IndData, sizeof(char), IndDataSize, IndFile);
        // if the idx file is empty
		if (DataReadSize < IndDataSize)
		{
			Ind = new Indexer_s();
			break;
		}
		Ind = indexer->IndexFactory(*version, IndData);
		if (Odometer < Ind->odometer && n != 0)
		{
			if (l_odo_boundary) // for left odo meter boundary, shift file pointer back
			{
				fseek(IndFile, -2 * IndDataSize, SEEK_CUR);
				DataReadSize = fread(IndData, sizeof(char), IndDataSize, IndFile);
				Ind = indexer->IndexFactory(*version, IndData);
			}
			if (IndFile != NULL) fclose(IndFile);
			if (indexer != NULL) delete indexer;
			return Ind;
		}
		else if (Odometer == Ind->odometer)
		{
			if (IndFile != NULL) fclose(IndFile);
			if (indexer != NULL) delete indexer;
			return Ind;
		}
		//std::cout << Ind->odometer << "-----" << Ind->byteOffset << "-----" << Ind->filePart << "-----" << std::endl;
		if (!feof(IndFile))
			free(Ind);
		n++;
	}
	if (IndFile != NULL) fclose(IndFile);
	if (indexer != NULL) delete indexer;
	return Ind;

}


void ReadVDObyBlock(const char *input_dir, const char *CamID, int odo_start, int odo_end,
	signed char **VD, int *odos, int *row, int *col)
{
	// This is a c wrapper for the c++ function
	std::vector<Video_d_s> RangeVideoData;
	std::vector<infelHd_s> RangeHeaderData;
	std::vector<std::vector<char>> VideoData;
	std::string input_dir_str(input_dir), CamID_str(CamID), saverange;
	std::ostringstream range;
	int OutputOption = 1; bool save_pano_img(false), save_csv_info(false);
	double Uncertainty = .5;
	range << CamID << "(" << odo_start << ", " << odo_end << ")";
	saverange = range.str();
	GetMetadataFromIntCnt(input_dir_str, saverange,
		&RangeVideoData, &RangeHeaderData, &VideoData, OutputOption, save_pano_img, save_csv_info, Uncertainty);
	// copy value to VD

	*row = (int)VideoData.size();
	for (int i = 0; i < *row; ++i)
	{
		*(col + i) = (int)VideoData.at(i).size();
		odos[i] = RangeVideoData.at(i).St.Odom;
		for (int j = 0; j < *(col + i); ++j)
		{
			VD[i][j] = VideoData.at(i).at(j);
		}
	}

	VideoData.clear();
	RangeVideoData.clear();
	RangeHeaderData.clear();

}

void ReadVDOInit(const char *input_dir, const char *CamID, long int &odo_min, long int &odo_max)
{
	std::string input_dir_str(input_dir), CamID_str(CamID);
	getOdoRange(input_dir_str, CamID_str, odo_min, odo_max);
}

int OutputExtCnt_FNumfromVDO(std::string VDOFiles)
{
	char * l_HeaderData = NULL;
	char * l_HDataTem = NULL;
	char * l_VDataTem = NULL; // Save video data at the end of the file and concatenate the next file
	char * l_VideoData = NULL;
	FILE * l_VideoFile = NULL;
	int frameIdx;
	int l_VRSize;
	int l_totlen; // l_Header->totlen in the previous vdo file
	int l_HRSize; // Size of read header in previous vdo file
	bool BreakinHeader = false; // to check whether a break in header for different vdo files
	bool BreakinData = false;
	size_t l_HSizeTem = sizeof(infelHd_ss);
	l_HDataTem = (char*)malloc(l_HSizeTem);
	l_VDataTem = (char*)malloc(0x400000); // about 4 Mb
	bool HDataTemused;
	// The start and end of internal counter, range to save the images
	long int StartInern, EndIntern;

	SVec Filelist;
	std::ofstream VdoDscr, LogFile;
	SVec DirplusFile;

	std::string filename, SID = "";
	std::string directory, f;
	SVec FileSelected;
	std::vector<size_t> eraseIdx;
	size_t tag;
	int numAsterisk;
	fs::path full_path(fs::initial_path<fs::path>());

	filename = VDOFiles;

	full_path = fs::system_complete(fs::path(filename));

    // get SID (camera ID)
    if (!fs::exists(full_path))
	{
		// Command argument is directory + file name
		const size_t last_slash_idx = filename.find_last_of("\\/");
		if (std::string::npos != last_slash_idx)
		{
			f = filename.substr(last_slash_idx + 1, filename.size() - last_slash_idx - 1); // Get the file name
																						   //filename.erase(0, last_slash_idx + 1); // Get the file name
		}
        // Check * existance
		if (existAsterisk(f) && Filelist.size() != 0)
		{
			numAsterisk = countAsterisk(f);
			if (numAsterisk == 1)
			{
				// find * and .
				int ast_pos = f.find_first_of("*");
				int last_dot = f.find_last_of(".");
				SID = f.substr(ast_pos + 1, last_dot - ast_pos - 1);
            }
            else if (numAsterisk == 2)
			{
				SVec subStrings = Clear2Asterisk(f);
				SID = subStrings.at(0);
            }
        }
    }
    
    getFilelist(filename, SID, directory, Filelist);
    
    // Put files in Filelist into different catalogs
	// Select different camera IDs and put them into the corresponding catalog
	std::vector<SVec> FCatalog;
	bool Dir_created = false;
	std::string dir_path, log_path;
	ConstructFCatalog(&FCatalog);
	CatalogFile(&FCatalog, Filelist);
	SortCatalog(&FCatalog);

	// Log file output and create directory
	std::ostringstream LogFileName;
	if (Filelist.size() != 0)
	{
		const size_t first_dot = Filelist.at(0).find_first_of('.');
		log_path = Filelist.at(0).substr(0, first_dot);
	}
	else
	{
		std::cout << "No vdo files found!" << std::endl;
		system("PAUSE");
		return 0;
	}
	LogFileName << log_path << "/" << "Log.txt";
	fs::path logdir(log_path);
	if (fs::create_directories(logdir))
		Dir_created = true;
	LogFile.open(LogFileName.str().c_str(), std::ofstream::out);
	//double perc; int round = 1;
	// Iterate over vdo files by camera stations
	for (auto itt = FCatalog.begin(); itt != FCatalog.end(); ++itt)
	{
		int totsize = 0;
		size_t LastBlen = 0, LastBtotlen = 0;
		std::ostringstream OutFileName, Out;
		bool OutVideoDscr = true; // Switch to turn on writing file
		bool l_Initialized(false);
		locogio_s l_CompressionConfig;
		unsigned char * l_VideoBuffer;
		l_VideoBuffer = NULL;
		static int ImType, ImWidth; bool ImaproGet = false;
		cv::Mat image;
		static int NumBlocks = 0;
		bool Jdir_created = false; // JPEG directory creation tag
		bool ImSaveFinished = false; // Tag to show whether image has been saved
		bool ImSplit = false;
		std::string CamID;
		int ImEndIntern;


		if (itt->size() != 0)
		{
			// Get camera ID 
			size_t first_dot = itt->at(0).find_first_of('.');
			size_t second_dot = itt->at(0).find_first_of('.', first_dot + 1);
			size_t third_dot = itt->at(0).find_first_of('.', second_dot + 1);
			CamID = itt->at(0).substr(second_dot + 1, third_dot - second_dot - 1);

			OutFileName << "VdoDscr_" << itt->at(0) << ".csv";
			if (OutVideoDscr)
			{
				if (!Dir_created)
				{
					const size_t first_dot = itt->at(0).find_first_of('.');
					dir_path = itt->at(0).substr(0, first_dot);
					fs::path dir(dir_path);
					if (fs::create_directories(dir))
						Dir_created = true;
				}
				Out << log_path << "/" << OutFileName.str();
				VdoDscr.open(Out.str().c_str(), std::ofstream::out);
				VdoDscr << "sep=," << std::endl; // Open with excel with columns
				VdoDscr << "Odometer:" << ',' << "FrameNum:" << std::endl;
			}
		}
		else
			OutVideoDscr = false;

		// Iterate over vdo files for the same camera station
		for (size_t it = 0; it < itt->size(); ++it)
		{
			//int Endianness = 0; // Endianness determination
			//CheckEndian(&Endianness); // Check Endianness if needed
			//int OutLsize = 25; // For aligning output txt file
			size_t l_TotalDataRead = 0;

			l_VideoFile = fopen((directory + '\\' + itt->at(it)).c_str(), "rb");
			if (l_VideoFile == NULL)
			{
				printf("Error opening the entered file, does it exist?\n");
				goto usage;
			}


			{
				size_t l_HeaderSize = sizeof(infelHd_s);
				size_t l_VideoDataSize = 0;
				size_t l_DataReadSize = 0;

				l_HeaderData = (char*)malloc(l_HeaderSize);
				l_VideoData = (char*)malloc(0x400000); //about 4MB

				infelHd_s * l_Header = NULL;
				Video_d_s *l_Video = NULL;

				if (LastBtotlen - LastBlen != 0)
				{
					if (BreakinData)
					{
						fread(l_VDataTem + l_VRSize, 1, LastBtotlen - LastBlen, l_VideoFile);
						l_Video = (Video_d_s *)l_VDataTem;
						//fseek(l_VideoFile, LastBtotlen - LastBlen, SEEK_CUR);
						BreakinData = false;
					}
					// Shift the file handle
					else
						fseek(l_VideoFile, (long)(LastBtotlen - LastBlen), SEEK_SET);
					LastBtotlen = 0; LastBlen = 0; // set back to zero in order not to effect next files
				}

				while (feof(l_VideoFile) == 0)
				{
					//if (NumBlocks == 195698) // for 74, reading error occurs in 002.74.vdo
					//	std::cout << "terminate" << std::endl;
					bool turn = false;
					if (BreakinHeader) // If the header is split in two different vdo files
					{
						HDataTemused = true;
						// Use a temporary buffer to save the header information in the second vdo file
						l_DataReadSize = fread(l_HDataTem + l_HRSize, 1, l_HeaderSize - l_HRSize, l_VideoFile);
					}
					else
					{
						HDataTemused = false;
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
					}
					BreakinHeader = false;
					if (l_DataReadSize != l_HeaderSize)
					{
						if (feof(l_VideoFile) != 0) // If to the end of the file
						{
							l_HRSize = (int)l_DataReadSize;
							// Save part of header information in the first vdo file to a temporary buffer
							memcpy(l_HDataTem, l_HeaderData, l_HRSize);
							BreakinHeader = true;
						}
						if (feof(l_VideoFile) == 0 && l_DataReadSize != l_HeaderSize - l_HRSize)
						{
							printf("Read unexpected amount of data for the header\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_HeaderSize);
							goto exit;
						}
						if (BreakinHeader)
						{
							l_TotalDataRead += l_DataReadSize;
							goto exit;
						}
					}
					l_TotalDataRead += l_DataReadSize;

					if (!HDataTemused)
						l_Header = (infelHd_s *)l_HeaderData;
					else
						l_Header = (infelHd_s *)l_HDataTem;

					// Some notes:
					// If l_Header->infid is not "divD", search till the next "divD" is found and continue processing
					if (l_Header->infid != VIDEO_FIF) // When this condition is satisfied, there probably be something wrong with the data.
					{
						std::cout << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						std::cout << "The previous frame idx is " << frameIdx << std::endl;
						LogFile << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						LogFile << "The previous frame idx is " << frameIdx << std::endl;
						int offset = -(int(l_DataReadSize) + l_VRSize);
						int pos1 = ftell(l_VideoFile);
						//fpos_t pos1;
						//fgetpos(l_VideoFile, &pos1);
						if (pos1 < -offset) // Make sure that the file handle is not out of the file boundary
							fseek(l_VideoFile, 0, SEEK_SET);
					}

					// Search for the next "divD" if the header is not correctly stored in l_Header
					while (l_Header->infid != VIDEO_FIF)
					{
						unsigned char c; // note: int, not char, required to handle EOF
						turn = true;
						while ((c = std::fgetc(l_VideoFile)) != 'd' && feof(l_VideoFile) == 0)
						{ // standard C I/O file reading loop
						}
						if (feof(l_VideoFile) != 0)
							break;
						fseek(l_VideoFile, -1, SEEK_CUR);
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
						l_Header = (infelHd_s *)l_HeaderData;
					}
					if (feof(l_VideoFile) != 0)
						break;
					///////////////////////////////////////////////////////

					l_totlen = l_Header->totlen;
					l_VideoDataSize = l_totlen - l_HeaderSize;

					l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, l_VideoFile);
					l_VRSize = int(l_DataReadSize);
					//fseek(l_VideoFile, l_VideoDataSize, SEEK_CUR);
					/*if (ferror (l_VideoFile))
					std::cout << "Error occurred while reading file!" << std::endl;*/
					if (l_DataReadSize != l_VideoDataSize)
					{
						if (feof(l_VideoFile) == 0)
						{
							printf("Read unexpected amount of data for the video packet\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_VideoDataSize);
							goto exit;
						}
						// It means here is the end of the file
						if (l_Header->infid == VIDEO_FIF)
						{
							memcpy(l_VDataTem, l_VideoData, l_VRSize); // Copy the data from the previous file
							BreakinData = true;
							l_totlen = l_Header->totlen;
						}
						LastBtotlen = l_VideoDataSize; LastBlen = l_DataReadSize; // Exclude length of header
																				  // Add the read data size when the last block is not complete --Shulin
						l_TotalDataRead += l_DataReadSize;
						goto exit;
					}
					l_TotalDataRead += l_DataReadSize;

					if (l_Header->infid == VIDEO_FIF)
					{
						//l_Video = (Video_d_s *) ::operator new (l_DataReadSize); // Commented out for just output vdo detail
						l_Video = (Video_d_s *)l_VideoData;
						if (!ImaproGet)
						{
							ImType = l_Video->image_type;
							ImWidth = l_Video->width;
							ImaproGet = true;
						}
						frameIdx = l_Video->frameCnt;
						if (turn == true)
						{
							std::cout << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
							LogFile << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
						}
						// Write Vdo description
						if (OutVideoDscr)
						{
							VdoDscr << l_Video->St.Odom << ',' << l_Video->frameCnt << std::endl;
						}
						//OutVideoDscr = false;
					}
				}

				goto exit;
			}

		usage:
			ShowUsage3();

		exit:
			if (!BreakinHeader)
				if (l_HeaderData != NULL) free(l_HeaderData);
			if (l_VideoData != NULL) free(l_VideoData);
			if (l_VideoFile != NULL)
			{
				fclose(l_VideoFile);
				printf("File read without problems!\n");
				LogFile << "File read without problems!" << std::endl;
			}
			printf("Read %Iu bytes\n", l_TotalDataRead);
			LogFile << "Read " << l_TotalDataRead << " bytes" << std::endl;
			//round ++;
			//system("PAUSE");
		}
		if (OutVideoDscr)
		{
			std::cout << OutFileName.str() << "  generated!" << std::endl;
			LogFile << OutFileName.str() << "  generated!" << std::endl;
		}
		OutVideoDscr = false;
		VdoDscr.close();
	}

	LogFile.close();
	return 0;
}


// show images of vdo data
int ReadVDO(std::string input_dir, std::string CamID, int Odometer)
{
	std::string dir = input_dir + "/*" + CamID + "*.vdo";
	std::string in_dir = input_dir + "/", idx_file;
	SVec idx_file_list;
	Indexer_s *indexer = NULL;
	if (Odometer != 0) // default Odometer value
	{
		GetFileInDir(in_dir, &idx_file_list);
		elimVDOs(&idx_file_list);
		GetIdxFilefromNonVdoFile(&idx_file_list, CamID);
		if (idx_file_list.size() == 1)
			idx_file = in_dir + idx_file_list.at(0);
		else
		{
			std::cout << "number of idx file exceeds 1!" << std::endl;
			return -1;
		}
		// read idx file
		indexer = get_indexer_from_given_odo(Odometer, idx_file, 1);
	}
	else
		indexer = new Indexer_s();
	char * l_HeaderData = NULL;
	char * l_HDataTem = NULL;
	char * l_VDataTem = NULL; // Save video data at the end of the file and concatenate the next file
	char * l_VideoData = NULL;
	// Save the header data if video data is separated in two vdo files in order to save it back to std vector and then python list
	char * l_HDataTemFBreak = NULL;
	FILE * l_VideoFile = NULL;
	int frameIdx;
	int l_VRSize;
	int l_totlen; // l_Header->totlen in the previous vdo file
	int l_HRSize; // Size of read header in previous vdo file
	bool BreakinHeader = false; // to check whether a break in header for different vdo files
	bool BreakinData = false;
	bool RangeExists = false; // Whether the rail range exists
	size_t l_HSizeTem = sizeof(infelHd_ss);
	l_HDataTem = (char*)malloc(l_HSizeTem);
	l_VDataTem = (char*)malloc(0x400000); // about 4 Mb
	l_HDataTemFBreak = (char*)malloc(l_HSizeTem);
	bool HDataTemused;
	// The start and end of internal counter, range to save the images
	long int StartInern, EndIntern;
	bool pano_all_export = false;
	int OutputOption = 1;
	bool save_pano_img = false;
	double Uncertainty = 0.5;

	SVec Filelist;
	std::string directory;
	// record the internal counter and frame number of exported pano images
	std::ofstream pano_csv;

    getFilelist(dir, CamID, directory, Filelist);

	// Put files in Filelist into different catalogs
	// Select different camera IDs and put them into the corresponding catalog
	std::vector<SVec> FCatalog;
	bool Dir_created = false;
	std::string dir_path, log_path;
	ConstructFCatalog(&FCatalog);
	CatalogFile(&FCatalog, Filelist);
	SortCatalog(&FCatalog);

	// Log file output and create directory
	if (Filelist.size() != 0)
	{
		const size_t first_dot = Filelist.at(0).find_first_of('.');
		log_path = Filelist.at(0).substr(0, first_dot);
	}
	else
	{
		std::cout << "No vdo files found!" << std::endl;
		return 0;
	}
	//double perc; int round = 1;
	// Iterate over vdo files by camera stations
	for (auto itt = FCatalog.begin(); itt != FCatalog.end(); ++itt)
	{
		size_t LastBlen = 0, LastBtotlen = 0, first_dot, second_dot, third_dot;
		bool l_Initialized(false);
		locogio_s l_CompressionConfig;
		//l_CompressionConfig = (locogio_s*)malloc(sizeof(locogio_s));

		static int ImType, ImWidth; bool ImaproGet = false;
		cv::Mat img_show;
		int NumBlocks = 0, jump_line = 5;
		bool Jdir_created = false; // JPEG directory creation tag
		bool ImSaveFinished = false; // Tag to show whether image has been saved
		bool ImSplit = false;
		std::string CamID, path_csv;
		int ImEndIntern, file_part;

		if (itt->size() != 0)
		{
			// Get camera ID and file_part
			first_dot = itt->at(0).find_first_of('.');
			second_dot = itt->at(0).find_first_of('.', first_dot + 1);
			third_dot = itt->at(0).find_first_of('.', second_dot + 1);
			CamID = itt->at(0).substr(second_dot + 1, third_dot - second_dot - 1);
			// erase redundant vdo files from the file list
     		file_part = atoi(itt->at(0).substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			while (file_part < indexer->filePart)
			{
				itt->erase(itt->begin());
				file_part = atoi(itt->at(0).substr(first_dot + 1, second_dot - first_dot - 1).c_str());
			}
		}

		if (CamID == "c50" || CamID == "c51")
		{
			if (!Jdir_created)
			{
				fs::path jpegdir(log_path + '/' + CamID);
				fs::create_directories(jpegdir);
				Jdir_created = true;
			}
			// This file is for GPS exportation
			path_csv = log_path + '/' + CamID + '/' + log_path + '_' + CamID + "_IntCntFrNum.csv";
			pano_csv.open(path_csv.c_str(), std::ofstream::out);
			pano_csv << "sep=," << std::endl; // Open with excel with columns
			pano_csv << "Odometer:" << ',' << "FrameNum:" << std::endl;
		}

		// Iterate over vdo files for the same camera station
		for (size_t it = 0; it < itt->size(); ++it)
		{
			//int Endianness = 0; // Endianness determination
			//CheckEndian(&Endianness); // Check Endianness if needed
			//int OutLsize = 25; // For aligning output txt file
			size_t l_TotalDataRead = 0;
			unsigned char * l_VideoBuffer;
			l_VideoBuffer = NULL;
			l_VideoFile = fopen((directory + '\\' + itt->at(it)).c_str(), "rb");
			// shift the FILE pointer by indexer->byteOffset
			if (it == 0)
			    fseek(l_VideoFile, indexer->byteOffset, SEEK_CUR);
			if (l_VideoFile == NULL)
			{
				printf("Error opening the entered file, does it exist?\n");
				goto usage;
			}


			{
				size_t l_HeaderSize = sizeof(infelHd_s);
				size_t l_VideoDataSize = 0;
				size_t l_DataReadSize = 0;

				l_HeaderData = (char*)malloc(l_HeaderSize);
				l_VideoData = (char*)malloc(0x400000); //about 4MB
				l_VideoBuffer = ((unsigned char *)l_VideoData + sizeof(Video_d_s) - 1);
				infelHd_s * l_Header = NULL;
				Video_d_s *l_Video = NULL;

				if (LastBtotlen - LastBlen != 0)
				{
					if (BreakinData)
					{
						fread(l_VDataTem + l_VRSize, 1, LastBtotlen - LastBlen, l_VideoFile);
						l_Video = (Video_d_s *)l_VDataTem;

						// It seems that BreakinData for c50 does not exist!
						if ((CamID == "c50") || (CamID == "c51"))
						{

							//infelHd_s * l_HeaderTemFBreak = NULL;
							//l_HeaderTemFBreak = (infelHd_s *)l_HDataTemFBreak;
							//(*RangeHeaderData).push_back(*l_HeaderTemFBreak);
							//(*RangeVideoData).push_back(*l_Video);
							size_t l_VDataTemSize = l_VRSize + LastBtotlen - LastBlen;
							//unsigned char *l_VDataTemUchar = NULL;
							//l_VDataTemUchar = (unsigned char *)l_VDataTem;
							//(*VideoData).push_back(std::vector<int>(l_VDataTemUchar + sizeof(Video_d_s) - 1, l_VDataTemUchar + l_VDataTemSize));

							/*// Output Image when processing panorama cameras -- this output all panorama images
							SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VDataTemSize);
							NumBlocks++;*/

							// Output panorama image with internal counter in a certain range -- since the internal counter has been corrected
							if (save_pano_img)
								SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VDataTemSize, l_Video->St.Odom);
							else
								ShowFB(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
							pano_csv << l_Video->St.Odom << ',' << l_Video->frameCnt << std::endl;
							NumBlocks++;


						}

#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& CamID != "c50")
							{
								int re = LinearCamDecompImgShow(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VDataTem, l_totlen,
									CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, img_show, OutputOption, jump_line, l_Video->St.Odom);
								if (re == -1)
								{
									cv::destroyAllWindows();
									return -1;
								}

							}
						}
#endif
						BreakinData = false;
					}
					// Shift the file handle
					else
						fseek(l_VideoFile, (long)(LastBtotlen - LastBlen), SEEK_SET);
					LastBtotlen = 0; LastBlen = 0; // set back to zero in order not to effect next files
				}

				while (feof(l_VideoFile) == 0)
				{
					bool turn = false;
					if (BreakinHeader) // If the header is split in two different vdo files
					{
						HDataTemused = true;
						// Use a temporary buffer to save the header information in the second vdo file
						l_DataReadSize = fread(l_HDataTem + l_HRSize, 1, l_HeaderSize - l_HRSize, l_VideoFile);
					}
					else
					{
						HDataTemused = false;
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
					}
					BreakinHeader = false;
					if (l_DataReadSize != l_HeaderSize)
					{
						if (feof(l_VideoFile) != 0) // If to the end of the file
						{
							l_HRSize = (int)l_DataReadSize;
							// Save part of header information in the first vdo file to a temporary buffer
							memcpy(l_HDataTem, l_HeaderData, l_HRSize);
							BreakinHeader = true;
						}
						if (feof(l_VideoFile) == 0 && l_DataReadSize != l_HeaderSize - l_HRSize)
						{
							printf("Read unexpected amount of data for the header\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_HeaderSize);
							goto exit;
						}
						if (BreakinHeader)
						{
							l_TotalDataRead += l_DataReadSize;
							goto exit;
						}
					}
					l_TotalDataRead += l_DataReadSize;

					if (!HDataTemused)
					{
						l_Header = (infelHd_s *)l_HeaderData;
					}
					else
					{
						l_Header = (infelHd_s *)l_HDataTem;
					}
					// Some notes:
					// If l_Header->infid is not "divD", search till the next "divD" is found and continue processing
					if (l_Header->infid != VIDEO_FIF) // When this condition is satisfied, there probably be something wrong with the data.
					{
						std::cout << "No Dvid in the header! Search next \"divD\"!" << std::endl;
						std::cout << "The previous frame idx is " << frameIdx << std::endl;
						int offset = -(int(l_DataReadSize) + l_VRSize);
						//fpos_t pos1;
						//fgetpos(l_VideoFile, &pos1);
						int pos1 = ftell(l_VideoFile);
						if (pos1 < -offset) // Make sure that the file handle is not out of the file boundary
							fseek(l_VideoFile, 0, SEEK_SET);
					}

					// Search for the next "divD" if the header is not correctly stored in l_Header
					while (l_Header->infid != VIDEO_FIF)
					{
						unsigned char c; // note: int, not char, required to handle EOF
						turn = true;
						while ((c = std::fgetc(l_VideoFile)) != 'd' && feof(l_VideoFile) == 0)
						{ // standard C I/O file reading loop
						}
						if (feof(l_VideoFile) != 0)
							break;
						fseek(l_VideoFile, -1, SEEK_CUR);
						l_DataReadSize = fread(l_HeaderData, 1, l_HeaderSize, l_VideoFile);
						l_Header = (infelHd_s *)l_HeaderData;
					}
					if (feof(l_VideoFile) != 0)
						break;
					///////////////////////////////////////////////////////

					l_totlen = l_Header->totlen;
					l_VideoDataSize = l_totlen - l_HeaderSize;

					l_DataReadSize = fread(l_VideoData, 1, l_VideoDataSize, l_VideoFile);
					l_VRSize = int(l_DataReadSize);
					//fseek(l_VideoFile, l_VideoDataSize, SEEK_CUR);
					/*if (ferror (l_VideoFile))
					std::cout << "Error occurred while reading file!" << std::endl;*/
					if (l_DataReadSize != l_VideoDataSize)
					{
						if (feof(l_VideoFile) == 0)
						{
							printf("Read unexpected amount of data for the video packet\n");
							printf("Read %Iu bytes instead of %Iu bytes!\n", l_DataReadSize, l_VideoDataSize);
							goto exit;
						}
						// It means here is the end of the file
						if (l_Header->infid == VIDEO_FIF)
						{
							memcpy(l_VDataTem, l_VideoData, l_VRSize); // Copy the data from the previous file
							BreakinData = true;
							// Copy memory to l_HDataTemFBreak and save to std vector in the next iteration. Header data is complete if video data is split
							memcpy(l_HDataTemFBreak, l_HeaderData, l_HeaderSize);
							l_totlen = l_Header->totlen;
						}
						LastBtotlen = l_VideoDataSize; LastBlen = l_DataReadSize; // Exclude length of header
																				  // Add the read data size when the last block is not complete --Shulin
						l_TotalDataRead += l_DataReadSize;
						goto exit;
					}
					l_TotalDataRead += l_DataReadSize;

					if (l_Header->infid == VIDEO_FIF)
					{
						l_Video = (Video_d_s *)l_VideoData;
						if (!ImaproGet)
						{
							ImType = l_Video->image_type;
							ImWidth = l_Video->width;
							ImaproGet = true;
						}
						frameIdx = l_Video->frameCnt;
						if (turn == true)
						{
							std::cout << "the next frame idx after searching for 'divD' is " << frameIdx << std::endl;
						}

						// save jpeg files for camera c50
						if ((CamID == "c50") || (CamID == "c51"))
						{
							//(*RangeHeaderData).push_back(*l_Header);
							//(*RangeVideoData).push_back(*l_Video);
							//unsigned char *l_VideoDataUchar = NULL;
							//l_VideoDataUchar = (unsigned char *)l_VideoData;
							//(*VideoData).push_back(std::vector<int>(l_VideoDataUchar + sizeof(Video_d_s) - 1, l_VideoDataUchar + l_VideoDataSize));

							/*// Output Image when processing panorama cameras -- this output all panorama images
							SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
							NumBlocks++;*/

							// Output panorama image with internal counter in a certain range -- since the internal counter has been corrected
							if (save_pano_img)
							{
								// Output panorama image
								SaveJPEG_fb(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
							}
							else
							{
								// 
								ShowFB(Jdir_created, CamID, log_path, NumBlocks, l_Video, l_VideoDataSize, l_Video->St.Odom);
							}
							pano_csv << l_Video->St.Odom << ',' << l_Video->frameCnt << std::endl;
							NumBlocks++;

						}

						// Decompress					
#ifdef DECOMPRESS
						if (!NoDecomp)
						{
							if ((l_Video->image_type == IMAGE_GDM_LINEAR_COLOR || l_Video->image_type == IMAGE_GDM_LINEAR_BW)
								&& CamID != "c50")
							{
								// Output decompressed video data
								std::cout << "Odometer = " << l_Video->St.Odom << std::endl;
								int re = LinearCamDecompImgShow(&l_Initialized, &l_CompressionConfig, ImType, ImWidth, l_VideoBuffer, l_VideoData, l_totlen,
									CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, img_show, OutputOption, jump_line, l_Video->St.Odom);
								if (re == -1)
								{
									cv::destroyAllWindows();
									return -1;
								}

							}
						}
#endif

					}
				}

				goto exit;
			}

		usage:
			ShowUsage2();

		exit:
			//if (l_VideoBuffer != NULL) free(l_VideoBuffer);
			/*if (l_Initialized)
			{
			//free(l_CompressionConfig->dif);
			//free(l_CompressionConfig->yuv);
			free(l_CompressionConfig.dif);
			free(l_CompressionConfig.yuv);
			}*/

			if (!HDataTemused)
			{
				if (l_HeaderData != NULL) free(l_HeaderData);
			}
			else
			{
				free(l_HDataTem);
			}
			if (l_VideoData != NULL) free(l_VideoData);
			if (l_VideoFile != NULL)
			{
				fclose(l_VideoFile);
				printf("File read without problems!\n");
			}
			printf("Read %Iu bytes\n", l_TotalDataRead);

		}

	}

	//free(l_HDataTem);
	free(l_VDataTem);
	free(l_HDataTemFBreak);
	return 0;
}

int locogio_decompress_line_imshow(locogio_s *a_Loco, unsigned char *a_Cline, unsigned char* a_Out, int a_CompressSize,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created, bool DecompandSaveIm, int ImType, cv::Mat &img_show,
	int OutputOption, int &jump_line, int Odometer)
{
	int l_Y, l_Cr, l_Cb;
	int l_Yo = 0, l_Cro = 0, l_Cbo = 0;
	const char ESC_KEY = 27;
	cv::Mat img_line;
	std::string Odo = std::to_string(Odometer);
	std::string Text = "Odometer = " + Odo;
	if (ImType == IMAGE_GDM_LINEAR_COLOR)
		img_line.create(1, a_Loco->length, CV_8UC3);
	else if (ImType == IMAGE_GDM_LINEAR_BW)
		img_line.create(1, a_Loco->length, CV_8UC1);
	
	int imlen = 800;
	a_Loco->cbuffer = a_Cline;
	a_Loco->compress_size = a_CompressSize;
	a_Loco->cbuffer_bit_ptr = 0;
	a_Loco->cbuffer_ptr = 0;
	// DECOMPRESSION
	decompress(a_Loco, a_CompressSize);

	// Restore diffs
	for (unsigned int x = 0; x<a_Loco->length; x++)
	{
		l_Y = a_Loco->dif[x].dy + l_Yo;
		l_Cr = a_Loco->dif[x].du + l_Cro;
		l_Cb = a_Loco->dif[x].dv + l_Cbo;

		l_Yo = l_Y;
		l_Cro = l_Cr;
		l_Cbo = l_Cb;

		a_Loco->yuv[x].y = l_Y;
		a_Loco->yuv[x].cr = l_Cr;
		a_Loco->yuv[x].cb = l_Cb;
	}

	// YUV to RGB
	if (a_Loco->color)
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			int l_Y, l_Cr, l_Cb;
			int l_R, l_G, l_B;

			l_Y = a_Loco->yuv[x].y;
			l_Cr = a_Loco->yuv[x].cr;
			l_Cb = a_Loco->yuv[x].cb;

			l_G = l_Y - (77 * l_Cr + 25 * l_Cb) / 256;
			l_R = (l_Y + l_Cr);
			l_B = (l_Y + l_Cb);

			a_Out[x * 3] = CLAMP(l_R);
			if (a_Loco->color)
			{
				a_Out[x * 3 + 1] = CLAMP(l_G);
				a_Out[x * 3 + 2] = CLAMP(l_B);
			}
			img_line.at<cv::Vec3b>(0, x)[0] = a_Out[x * 3 + 2];
			img_line.at<cv::Vec3b>(0, x)[1] = a_Out[x * 3 + 1];
			img_line.at<cv::Vec3b>(0, x)[2] = a_Out[x * 3];

		}
		if (img_show.rows < imlen)
			img_show.push_back(img_line);
		else
		{
			cv::imshow(CamID, img_show);
			if (img_first_show)
			{
				cv::waitKey(0);
			    img_first_show = false;
			}
			if (cv::waitKey(1) == ESC_KEY)
				return -1;
			if (cv::waitKey(1) == 'i')
				if (jump_line < 200)
				    jump_line += 10;
			if (cv::waitKey(1) == 'd')
				if (jump_line > 10)
					jump_line -= 10;
				else
					jump_line = 1;
			if (cv::waitKey(1) == ' ')
				cv::waitKey(0);
			img_show.push_back(img_line);
			img_show = img_show.rowRange(jump_line, imlen + 1);
		}

	}

	else
	{
		for (unsigned int x = 0; x<a_Loco->length; x++)
		{
			a_Out[x] = CLAMP(a_Loco->yuv[x].y);
			img_line.at<unsigned char>(0, x) = a_Out[x];
		}
		if (img_show.rows < imlen)
			img_show.push_back(img_line);
		else
		{
			cv::imshow(CamID, img_show);
			if (img_first_show)
			{
				cv::waitKey(0);
				img_first_show = false;
			}
			if (cv::waitKey(1) == ESC_KEY)
				return -1;
			if (cv::waitKey(1) == 'i')
				if (jump_line < 200)
					jump_line += 10;
			if (cv::waitKey(1) == 'd')
				if (jump_line > 10)
					jump_line -= 10;
				else
					jump_line = 1;
			if (cv::waitKey(1) == ' ')
				cv::waitKey(0);
			img_show.push_back(img_line);
			img_show = img_show.rowRange(jump_line, imlen + 1);
		}

	}

	return 0;
}

int LinearCamDecompImgShow(bool *l_Initialized, locogio_s *l_CompressionConfig, int ImType, int ImWidth,
	unsigned char * l_VideoBuffer, char * l_VideoData, int l_totlen,
	std::string CamID, std::string log_path, int &NumBlocks, bool &Jdir_created,
	bool DecompandSaveIm, cv::Mat &img_show, int OutputOption, int &jump_line, int Odometer)
{
	if (!*l_Initialized)
	{
		*l_Initialized =
			locogio_init(l_CompressionConfig, ImWidth, ImType == IMAGE_GDM_LINEAR_COLOR);
	}

	if (*l_Initialized)
	{
		//l_VideoBuffer = ( (unsigned char *)l_VideoData + sizeof(Video_d_s) - 1);
		//l_VideoBuffer_out = (unsigned char *)malloc(0x400000);
		int re = locogio_decompress_line_imshow(l_CompressionConfig, l_VideoBuffer, l_VideoBuffer, (l_totlen - sizeof(Video_i_s)) * 8,
			CamID, log_path, NumBlocks, Jdir_created, DecompandSaveIm, ImType, img_show, OutputOption, jump_line, Odometer);
		if (re == -1)
			return -1;

	}
}

void ShowFB(bool Jdir_created, std::string CamID, std::string log_path,
	int NumFrame, Video_d_s *l_Video, size_t l_VideoDataSize, int Odo)
{
	// save jpeg images for front & back cameras
	std::ostringstream jname;
	/*if (fs::is_directory(log_path + '/' + CamID))
	Jdir_created = true;  -- can be written outside of this function */
	if (!Jdir_created)
	{
		fs::path jpegdir(log_path + '/' + CamID);
		fs::create_directories(jpegdir);
		Jdir_created = true;
	}
	if (CamID == "c50") // front camera
		jname << log_path << '/' << CamID << '/' << std::setfill('0') << std::setw(6) << NumFrame << "_Frame[" << l_Video->frameCnt << "]_IntCnt[" << Odo << "]_1.jpg";
	else // rear camera
		jname << log_path << '/' << CamID << '/' << std::setfill('0') << std::setw(6) << NumFrame << "_Frame[" << l_Video->frameCnt << "]_IntCnt[" << Odo << "]_2.jpg";
	std::ofstream jpeg(jname.str(), std::ios::out | std::ios::binary);//l_VideoDataSize - sizeof(Video_d_ss) + 1
	jpeg.write((const char *)l_Video->px, 2); // Omit 4 Bytes after FF D8
	jpeg.write((const char *)l_Video->px + 6, l_VideoDataSize - sizeof(Video_d_ss) - 5);
	jpeg.close();
}

void WriteTextOnImg(cv::Mat &Image, std::string Text)
{
	int imgW, imgH;
	int fontFace = cv::FONT_HERSHEY_COMPLEX_SMALL;
	imgW = Image.cols;
	imgH = Image.rows;
	double fontScale = 1.5;
	int thickness = 2;
	cv::Point textOrg(imgW / 5, imgH / 1.2);
	cv::putText(Image, Text, textOrg, fontFace, fontScale, cv::Scalar::all(255), thickness, 8);
}

int FillDisWin(std::vector<std::vector<int>> &dis_img, cv::Mat &img,
	size_t height, std::vector<std::vector<int>> &VideoData, std::string CamID, bool &init)
{
	cv::Mat vd_img;
	// fill the display window with VideoData
	if (dis_img.size() < height && img.rows < height)
	{
		if (!init)
		    dis_img.insert(dis_img.end(), VideoData.begin(), VideoData.end());
		else
		{
			// append on img
			Vec2Mat(VideoData, vd_img, CamID);
			img.push_back(vd_img);
		}
		return 0;
	}
	else
	{
		if (!init)
		{
			Vec2Mat(dis_img, img, CamID);
			dis_img.clear();
			init = true;
		}
		return -1;
	}
}