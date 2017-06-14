#pragma once

#define KEEP_ALIVE_INTERVAL_SECONDS	40

class Robot;
class ChatAuth
{
public:
	ChatAuth(Robot *const robot, int rid, char *host, int port, Json::Value cookie);
	~ChatAuth();

	SOCKET getDouyuSocket();
	int login();
	//int logout();
	int sendBarrage(string barrage);
	int close();
	int receivePacket(Packet packet);

private:
	Robot *m_robot;
	int m_rid;
	char m_host[16];
	int m_port;
	Json::Value m_cookie;
	SOCKET m_douyuSocket;

	int sendText(string text);
	int sendJson(Json::Value json);
};