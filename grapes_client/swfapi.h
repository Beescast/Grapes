#pragma once
#include "jsoncpp-src-0.5.0\include\json\json.h"
#include <time.h>
#include <string>
#include <WinSock2.h>
#include "config.h"
#include "utils.h"
using namespace std;

#ifdef _DEBUG
//#define SWFAPI_IP	"127.0.0.1"
#define SWFAPI_IP	"123.56.239.203"
#else
#define SWFAPI_IP	"123.56.239.203"
#endif
#define SWFAPI_PORT	12306

class Swfapi
{
public:
	Swfapi();
	~Swfapi();

	static Json::Value xxSwfApi(Json::Value req);

private:
	
};
