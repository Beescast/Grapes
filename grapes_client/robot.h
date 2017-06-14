#pragma once

class Robot
{
public:
	Robot(int rid, Json::Value cookie, bool status, int freq);
	~Robot();

	int setSpeak(bool status);
	int setFreq(int freq);
	int sendBarrage(string barrage);
	void setSocketServer(SOCKET socketServer);
	int callback(Json::Value value);

	int getUid();
	//int run();
	int loopBarrage();
	int close();

private:
	int m_rid;
	int m_uid;
	bool m_speak;
	int m_freq;
	ChatAuth *m_auth;
	bool m_isRunning;
	SOCKET m_socketServer;
	int m_sendCount;
	int m_sendMax;
};