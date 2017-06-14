#pragma once

#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <string>
using namespace std;
#include "utils.h"

#define MESSAGE_TYPE_FROM_CLIENT	689
#define MESSAGE_TYPE_FROM_SERVER	690

#pragma pack(1)
union PACK {
	char buff[20000+12];
	struct DOUYU_PROTOCOL {
		unsigned long msg_len;
		unsigned long msg_len_bak;
		unsigned short msg_type;
		unsigned char encrypt;
		unsigned char reserved;
		char data[20000];
	} protocol;
};

class Packet
{
public:
	Packet(string buff);
	Packet(char *buff);
	~Packet();

	char * to_raw();
	int size();
	Json::Value getJson();
	string getString();
	string attr(string attrName);
	//static Packet sniff(string buff);

private:
	union PACK m_pack;
	Json::Value m_json;
};
