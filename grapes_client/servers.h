#pragma once

struct DouYuServer{
	char ip[16];
	int port;
};

//#define DERVER_NUM	(sizeof(douyuServers)/sizeof(douyuServers[0]))
#define DERVER_NUM	70

extern struct DouYuServer douyuServers[];